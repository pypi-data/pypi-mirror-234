# # Created by msinghal at 11/09/23
# import typing, dataclasses
# from singulr_client.span.span import Span
# from singulr_client.env.environment import Environment
# from singulr_client.utils import _safe_serialize, _hash_id
# from langchain.callbacks.tracers.schemas import Run
# from singulr_client.trace.trace import TraceTree
# from dataclasses import dataclass, field
#
#
#
# class SingulrTraceTree():
#     """Media object for trace tree data.
#
#     Arguments:
#         root_span (Span): The root span of the trace tree.
#         model_dict (dict, optional): A dictionary containing the model dump.
#             NOTE: model_dict is a completely-user-defined dict. The UI will render
#             a JSON viewer for this dict, giving special treatment to dictionaries
#             with a `_kind` key. This is because model vendors have such different
#             serialization formats that we need to be flexible here.
#     """
#
#     def __init__(
#             self,
#             root_span: Span,
#             model_dict: typing.Optional[dict] = None,
#             environment_info: Environment = None,
#             trace_id:str=None
#     ):
#         super().__init__()
#         self._root_span = root_span
#         self._model_dict = model_dict
#         self._environment_info = environment_info
#         self._trace_id = trace_id
#
#     def to_json(self) -> dict:
#
#         span_dict = self._root_span.to_dict()
#         env_dict = self._environment_info.to_dict()
#         environment = _safe_serialize(dataclasses.asdict(self._environment_info))
#         trace_tree = {"trace_id":  self._trace_id, "root_span": res["root_span_dumps"], "environment": environment}
#         print("trace_tree: \n {}".format(trace_tree))
#         return trace_tree
#
#     def is_bound(self) -> bool:
#         return True
#
#
