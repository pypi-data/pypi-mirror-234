# Created by msinghal at 12/09/23
import json
from langchain.callbacks.tracers.schemas import Run
from langchain.schema.messages import AIMessage
from typing import Optional, Tuple, Dict, Any, List
from singulr_client.common.utils import _serialize_io
from singulr_client.data_contracts.span.result import Result
from singulr_client.data_contracts.span.content import TextDocument, GenerationDocument, DocumentMetadata, GenerationInfo, ContentType
from singulr_client.data_contracts.span.primitive_attribute import IntAttribute, StringAttribute
from singulr_client.data_contracts.span.span import SpanType, Span, StatusCode



class SpanGenerator(object):
    """Handles the conversion of a LangChain Runs."""

    def process_span(self, run: Run, trace_id: str) -> Optional["Span"]:
        """Converts a LangChain Run into a Singulr Trace Span.
        :param run: The LangChain Run to convert.
        :return: The converted Singulr Trace Span.
        """
        try:
            span = self._convert_lc_run_to_sg_span(run, trace_id)
            return span
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            # TODO: handle exception and app centric error code generation
            return None

    def _convert_run_to_sg_span(self, run: Run, trace_id: str) -> "Span":
        """Base utility to create a span from a run.
        :param run: The run to convert.
        :return: The converted Span.
        """
        # attributes = {**run.extra} if run.extra else {}
        # attributes["execution_order"] = run.execution_order
        attribute = IntAttribute(key="execution_order", value=run.execution_order)
        return Span(
            span_id=str(run.id) if run.id is not None else None,
            name=run.name,
            start_time_millis=int(run.start_time.timestamp() * 1000),
            end_time_millis=int(run.end_time.timestamp() * 1000),
            status_code=StatusCode.SUCCESS
            if run.error is None
            else StatusCode.ERROR,
            status_message=run.error,
            attributes=[attribute],
            trace_id=trace_id
        )

    def _convert_llm_run_to_sg_span(self, run: Run, trace_id) -> "Span":
        """Converts a LangChain LLM Run into a Singulr Trace Span.
        :param run: The LangChain LLM Run to convert.
        :return: The converted Singulr Trace Span.
        """
        base_span = self._convert_run_to_sg_span(run, trace_id)

        # TODO: we will generic way to add attributes
        # if base_span.attributes is None:
        #     base_span.attributes = {}
        # base_span.attributes["llm_output"] = run.outputs.get("llm_output", {})

        for ndx, message in enumerate(run.inputs['messages'][0] or []):
            result = Result()
            content = message["kwargs"]['content']
            result.inputs = [TextDocument("prompt", content)]
            if (run.outputs is not None and len(run.outputs["generations"]) > ndx
                and len(run.outputs["generations"][ndx]) > 0):
                for g_i, gen in enumerate(run.outputs["generations"][ndx]):
                    gen_doc = GenerationDocument(f"gen_{g_i}", gen["text"])
                    if "generation_info" in gen:
                        gen_doc.generation_info = GenerationInfo(gen["generation_info"]['finish_reason'] if 'finish_reason' in gen else None)
                    else:
                        gen_doc.generation_info = GenerationInfo()
                    result.outputs.append(GenerationDocument(f"gen_{g_i}", gen["text"]))
            base_span.results.append(result)


        base_span.type = SpanType.LLM
        base_span.sub_type = run.name

        return base_span

    # if "input_documents" in run_inputs:
    #     docs = run_inputs["input_documents"]
    #     return {f"input_document_{i}": doc.json() for i, doc in enumerate(docs)}
    def _convert_chain_results_to_sg_results(self, run):
        result = Result()
        for key, input_data in run.inputs.items():
            if key == "input_documents":
                for i, doc in enumerate(input_data):
                    text_document = TextDocument(f"input_document_{i}", doc.page_content)
                    document_metadata = DocumentMetadata()
                    document_metadata.source = doc.metadata["source"] if 'metadata' in doc else None
                    document_metadata.pointer = doc.metadata["page"] if 'page' in doc else None
                    text_document.metadata = document_metadata
                    result.inputs.append(text_document)
            else:
                text_document = TextDocument(key, input_data)
                result.inputs.append(text_document)

        for key, output in run.outputs.items():
            if isinstance(output, AIMessage):
                output = output.content
            text_document = TextDocument(key, output)
            result.outputs.append(text_document)
        return [result]

    def _convert_chain_run_to_sg_span(self, run: Run, trace_id) -> "Span":
        """Converts a LangChain Chain Run into a Singulr Trace Span.
        :param run: The LangChain Chain Run to convert.
        :return: The converted Singulr Trace Span.
        """
        base_span = self._convert_run_to_sg_span(run, trace_id)
        base_span.results = self._convert_chain_results_to_sg_results(run)
        base_span.child_spans = [
            self._convert_lc_run_to_sg_span(child_run, trace_id) for child_run in run.child_runs
        ]
        base_span.type = (
            SpanType.AGENT
            if "agent" in run.name.lower()
            else SpanType.CHAIN
        )
        base_span.sub_type = run.name

        return base_span

    def _convert_tool_run_to_sg_span(self, run: Run, trace_id) -> "Span":
        """Converts a LangChain Tool Run into a Singulr Trace Span.
        :param run: The LangChain Tool Run to convert.
        :return: The converted Singulr Trace Span.
        """
        base_span = self._convert_run_to_sg_span(run, trace_id)
        base_span.results = self._convert_chain_results_to_sg_results(run)
        base_span.child_spans = [
            self._convert_lc_run_to_sg_span(child_run) for child_run in run.child_runs
        ]
        base_span.span_kind = SpanType.TOOL

        return base_span

    def _convert_lc_run_to_sg_span(self, run: Run, trace_id: str) -> "Span":
        """Utility to convert any generic LangChain Run into a Singulr Trace Span.
        :param run: The LangChain Run to convert.
        :return: The converted Singulr Trace Span.
        """
        if run.run_type == "llm":
            return self._convert_llm_run_to_sg_span(run, trace_id)
        elif run.run_type == "chain":
            return self._convert_chain_run_to_sg_span(run, trace_id)
        elif run.run_type == "tool":
            return self._convert_tool_run_to_sg_span(run, trace_id)
        else:
            return self._convert_run_to_sg_span(run, trace_id)

    def process_model(self, run: Run) -> Optional[Dict[str, Any]]:
        """Utility to process a run for Singulr model_dict serialization.
        :param run: The run to process.
        :return: The convert model_dict to pass to WBTraceTree.
        """
        try:
            data = json.loads(run.json())
            processed = self.flatten_run(data)
            keep_keys = (
                "id",
                "name",
                "serialized",
                "inputs",
                "outputs",
                "parent_run_id",
                "execution_order",
            )
            processed = self.truncate_run_iterative(processed, keep_keys=keep_keys)
            exact_keys, partial_keys = ("lc", "type"), ("api_key",)
            processed = self.modify_serialized_iterative(
                processed, exact_keys=exact_keys, partial_keys=partial_keys
            )
            output = self.build_tree(processed)
            return output
        except Exception as e:
            # TODO: handle exception
            return None

    def flatten_run(self, run: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Utility to flatten a nest run object into a list of runs.
        :param run: The base run to flatten.
        :return: The flattened list of runs.
        """

        def flatten(child_runs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
            """Utility to recursively flatten a list of child runs in a run.
            :param child_runs: The list of child runs to flatten.
            :return: The flattened list of runs.
            """
            if child_runs is None:
                return []

            result = []
            for item in child_runs:
                child_runs = item.pop("child_runs", [])
                result.append(item)
                result.extend(flatten(child_runs))

            return result

        return flatten([run])

    def truncate_run_iterative(
            self, runs: List[Dict[str, Any]], keep_keys: Tuple[str, ...] = ()
    ) -> List[Dict[str, Any]]:
        """Utility to truncate a list of runs dictionaries to only keep the specified
            keys in each run.
        :param runs: The list of runs to truncate.
        :param keep_keys: The keys to keep in each run.
        :return: The truncated list of runs.
        """

        def truncate_single(run: Dict[str, Any]) -> Dict[str, Any]:
            """Utility to truncate a single run dictionary to only keep the specified
                keys.
            :param run: The run dictionary to truncate.
            :return: The truncated run dictionary
            """
            new_dict = {}
            for key in run:
                if key in keep_keys:
                    new_dict[key] = run.get(key)
            return new_dict

        return list(map(truncate_single, runs))

    def modify_serialized_iterative(
            self,
            runs: List[Dict[str, Any]],
            exact_keys: Tuple[str, ...] = (),
            partial_keys: Tuple[str, ...] = (),
    ) -> List[Dict[str, Any]]:
        """Utility to modify the serialized field of a list of runs dictionaries.
        removes any keys that match the exact_keys and any keys that contain any of the
        partial_keys.
        recursively moves the dictionaries under the kwargs key to the top level.
        changes the "id" field to a string "_kind" field that tells WBTraceTree how to
        visualize the run. promotes the "serialized" field to the top level.

        :param runs: The list of runs to modify.
        :param exact_keys: A tuple of keys to remove from the serialized field.
        :param partial_keys: A tuple of partial keys to remove from the serialized
            field.
        :return: The modified list of runs.
        """

        def remove_exact_and_partial_keys(obj: Dict[str, Any]) -> Dict[str, Any]:
            """Recursively removes exact and partial keys from a dictionary.
            :param obj: The dictionary to remove keys from.
            :return: The modified dictionary.
            """
            if isinstance(obj, dict):
                obj = {
                    k: v
                    for k, v in obj.items()
                    if k not in exact_keys
                       and not any(partial in k for partial in partial_keys)
                }
                for k, v in obj.items():
                    obj[k] = remove_exact_and_partial_keys(v)
            elif isinstance(obj, list):
                obj = [remove_exact_and_partial_keys(x) for x in obj]
            return obj

        def handle_id_and_kwargs(
                obj: Dict[str, Any], root: bool = False
        ) -> Dict[str, Any]:
            """Recursively handles the id and kwargs fields of a dictionary.
            changes the id field to a string "_kind" field that tells WBTraceTree how
            to visualize the run. recursively moves the dictionaries under the kwargs
            key to the top level.
            :param obj: a run dictionary with id and kwargs fields.
            :param root: whether this is the root dictionary or the serialized
                dictionary.
            :return: The modified dictionary.
            """
            if isinstance(obj, dict):
                if ("id" in obj or "name" in obj) and not root:
                    _kind = obj.get("id")
                    if not _kind:
                        _kind = [obj.get("name")]
                    obj["_kind"] = _kind[-1]
                    obj.pop("id", None)
                    obj.pop("name", None)
                    if "kwargs" in obj:
                        kwargs = obj.pop("kwargs")
                        for k, v in kwargs.items():
                            obj[k] = v
                for k, v in obj.items():
                    obj[k] = handle_id_and_kwargs(v)
            elif isinstance(obj, list):
                obj = [handle_id_and_kwargs(x) for x in obj]
            return obj

        def transform_serialized(serialized: Dict[str, Any]) -> Dict[str, Any]:
            """Transforms the serialized field of a run dictionary to be compatible
                with WBTraceTree.
            :param serialized: The serialized field of a run dictionary.
            :return: The transformed serialized field.
            """
            serialized = handle_id_and_kwargs(serialized, root=True)
            serialized = remove_exact_and_partial_keys(serialized)
            return serialized

        def transform_run(run: Dict[str, Any]) -> Dict[str, Any]:
            """Transforms a run dictionary to be compatible with WBTraceTree.
            :param run: The run dictionary to transform.
            :return: The transformed run dictionary.
            """
            transformed_dict = transform_serialized(run)

            serialized = transformed_dict.pop("serialized")
            for k, v in serialized.items():
                transformed_dict[k] = v

            _kind = transformed_dict.get("_kind", None)
            name = transformed_dict.pop("name", None)
            exec_ord = transformed_dict.pop("execution_order", None)

            if not name:
                name = _kind

            output_dict = {
                f"{exec_ord}_{name}": transformed_dict,
            }
            return output_dict

        return list(map(transform_run, runs))

    def build_tree(self, runs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Builds a nested dictionary from a list of runs.
        :param runs: The list of runs to build the tree from.
        :return: The nested dictionary representing the langchain Run in a tree
            structure compatible with WBTraceTree.
        """
        id_to_data = {}
        child_to_parent = {}

        for entity in runs:
            for key, data in entity.items():
                id_val = data.pop("id", None)
                parent_run_id = data.pop("parent_run_id", None)
                id_to_data[id_val] = {key: data}
                if parent_run_id:
                    child_to_parent[id_val] = parent_run_id

        for child_id, parent_id in child_to_parent.items():
            parent_dict = id_to_data[parent_id]
            parent_dict[next(iter(parent_dict))][
                next(iter(id_to_data[child_id]))
            ] = id_to_data[child_id][next(iter(id_to_data[child_id]))]

        root_dict = next(
            data for id_val, data in id_to_data.items() if id_val not in child_to_parent
        )

        return root_dict
