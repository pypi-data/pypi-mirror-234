__author__='thiagocastroferreira'

import aixplain.model_interfaces.utils.metric_utils as utils
import json
import pytest
import tempfile

from aixplain.model_interfaces.interfaces.metric_models import (
    ReferencelessTextGenerationMetric
)
from aixplain.model_interfaces.schemas.metric_input import ReferencelessTextGenerationMetricInput
import os

INPUTS_PATH="tests/unit_tests/metrics/referenceless_text_generation/inputs.json"
OUTPUTS_PATH="tests/unit_tests/metrics/referenceless_text_generation/outputs.json"

@pytest.fixture
def inputs():
    with open(INPUTS_PATH) as f:
        return json.load(f)


@pytest.fixture
def outputs():
    with open(OUTPUTS_PATH) as f:
        return json.load(f)


class MockReferencelessTextGenerationMetric(ReferencelessTextGenerationMetric):
    pass

def test_error_empty(inputs):
    scorer = MockReferencelessTextGenerationMetric("mock-metric")

    inp = inputs['empty']
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as hypotheses_path, tempfile.NamedTemporaryFile(suffix=".json", delete=False) as references_path:
        json.dump(inp['hypotheses'], open(hypotheses_path.name, 'w'))
        files_to_be_deleted = [hypotheses_path.name, references_path.name]
        inp = { 
            "hypotheses": hypotheses_path.name,
            "supplier": "aiXplain",
            "metric": "mock"
        }

        request = {
            'instances': [inp]
        }
        
        with pytest.raises(Exception) as exc_info:
            result = scorer.score(request)

    for filename in files_to_be_deleted:
        if os.path.exists(filename):
            os.remove(filename)
    assert str(exc_info.value) == "HTTP 400: List of hypotheses must not be empty."


def test_error_hypothesis_missing(inputs):
    scorer = MockReferencelessTextGenerationMetric("mock-metric")

    inp = inputs['preprocessing']
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as hypotheses_path, tempfile.NamedTemporaryFile(suffix=".json", delete=False) as references_path:
        json.dump(inp['hypotheses'], open(hypotheses_path.name, 'w'))
        files_to_be_deleted = [hypotheses_path.name, references_path.name]
        inp = { 
            "hypotheses": "asdas",
            "supplier": "aiXplain",
            "metric": "mock"
        }

        request = {
            'instances': [inp]
        }
        
        with pytest.raises(Exception) as exc_info:
            result = scorer.score(request)
    
    for filename in files_to_be_deleted:
        if os.path.exists(filename):
            os.remove(filename)
    assert str(exc_info.value) == "HTTP 400: Invalid hypotheses link. Error: [Errno 2] No such file or directory: \'asdas\'"

def test_error_references_present(inputs):
    scorer = MockReferencelessTextGenerationMetric("mock-metric")

    inp = inputs["reference_param"]
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as hypotheses_path, \
            tempfile.NamedTemporaryFile(suffix=".json", delete=False) as references_path, \
            tempfile.NamedTemporaryFile(suffix=".json", delete=False) as sources_path:
        json.dump(inp['hypotheses'], open(hypotheses_path.name, 'w'))
        json.dump(inp['references'], open(references_path.name, 'w'))
        json.dump(inp['sources'], open(sources_path.name, 'w'))
        files_to_be_deleted = [hypotheses_path.name, references_path.name, sources_path.name]
        inp = { 
            "hypotheses": hypotheses_path.name,
            "references": references_path.name,
            "sources": sources_path.name,
            "supplier": "aiXplain",
            "metric": "mock"
        }

        request = {
            'instances': [inp]
        }
        
        with pytest.raises(Exception) as exc_info:
            result = scorer.score(request)

    for filename in files_to_be_deleted:
        if os.path.exists(filename):
            os.remove(filename)
    assert str(exc_info.value) == "HTTP 400: The parameter 'references' should not be passed"