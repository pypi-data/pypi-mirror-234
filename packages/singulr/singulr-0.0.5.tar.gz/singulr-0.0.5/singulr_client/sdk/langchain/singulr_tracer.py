# Created by msinghal at 12/09/23
from typing import Any, List, Optional, Union
from uuid import UUID
import json
from langchain.callbacks.tracers.langchain import LangChainTracer
from singulr_client.sdk.langchain.lc_run_persister import LCRunPersister
from singulr_client.data_contracts.trace.trace import TraceTree
from singulr_client.common.utils import generate_trace_id
from langchain.callbacks.tracers.schemas import Run
from singulr_client.client.singulr_ingestion_client import SingulrClient
from singulr_client.sdk.langchain.mapper.env_generator import EnvironmentGenerator
from singulr_client.sdk.langchain.mapper.span_generator import SpanGenerator
from singulr_client.data_contracts.ingestion.payload_message import PayloadMessage
from singulr_client.common.env_utils import get_runtime_environment

from typing import (
    Any,
    List,
    Optional,
    Union,
    cast,
)


def _get_client() -> LCRunPersister:
    """Get the client."""
    return LCRunPersister()


class SingulrTracer(LangChainTracer):
    def __init__(
            self,
            example_id: Optional[Union[UUID, str]] = None,
            project_name: Optional[str] = None,
            client: Optional[LCRunPersister] = None,
            tags: Optional[List[str]] = None,
            use_threading: bool = True,
            **kwargs: Any,
    ) -> None:
        super().__init__(example_id=example_id,
                         project_name=project_name,
                         client=client or _get_client(),
                         tags=tags,
                         use_threading=use_threading,
                         **kwargs)

    def _log_trace_from_run(self, run: Run) -> None:
        model_dict = SpanGenerator().process_model(run)
        trace_id = generate_trace_id(model_dict)
        environment = EnvironmentGenerator().process_environments(run)
        root_span = SpanGenerator().process_span(run, trace_id)

        if root_span is None:
            return

        model_trace = TraceTree(trace_id=trace_id,
                                environment=environment,
                                root_span=root_span)

        trace = model_trace.to_json()
        # json_string = json.dumps(trace)

        ingestion_payload = PayloadMessage(trace_id, trace)
        print("sending traces to ingestion service {}".format(json.dumps(ingestion_payload.to_dict())))
        try:
            response = SingulrClient().ingest_payload(ingestion_payload.to_dict())
        except:
            import traceback
            print("exception while tracing {}".format(traceback.print_exc()))
            return None

        if response.status_code == 200:
            print("payload sent to singulr ingestion pipeline successfully")
        else:
            print(response.status_code)

    def _persist_run(self, run: Run) -> None:
        """Persist a run."""
        runtime_env = get_runtime_environment()
        run.extra["runtime"] = runtime_env
        self._log_trace_from_run(run)
