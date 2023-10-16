# Created by msinghal at 09/10/23

import os
from pathlib import Path
import pytest
import pickle
from langchain.embeddings.elasticsearch import ElasticsearchEmbeddings
from singulr_client.singulr_tracer import SingulrTracer
from langchain.callbacks.tracers.schemas import Run


# @pytest.fixture
def load_run_examples() -> Run:
    file_path = str(Path(__file__).parents[2] / "examples/run_object_anonymize_chain.pkl")
    with open(file_path, 'r') as f:
        run = pickle.load(f)
    return run


def test_singulr_trace_generation() -> None:
    pass
