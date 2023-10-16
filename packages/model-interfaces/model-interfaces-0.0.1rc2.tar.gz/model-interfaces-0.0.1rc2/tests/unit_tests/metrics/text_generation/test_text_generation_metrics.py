__author__='thiagocastroferreira'

import aixplain.model_interfaces.utils.metric_utils as utils
import json
import pytest
import tempfile
import os
from aixplain.model_interfaces.interfaces.metric_models import (
    TextGenerationMetric
)
from aixplain.model_interfaces.schemas.metric_input import TextGenerationMetricInput

INPUTS_PATH="tests/unit_tests/metrics/text_generation/inputs.json"
OUTPUTS_PATH="tests/unit_tests/metrics/text_generation/outputs.json"

@pytest.fixture
def inputs():
    with open(INPUTS_PATH) as f:
        return json.load(f)


@pytest.fixture
def outputs():
    with open(OUTPUTS_PATH) as f:
        return json.load(f)


def test_input_processing(inputs, outputs):
    inp_hyp = inputs['preprocessing']['hypotheses']
    inp_refs = inputs['preprocessing']['references']

    out_hyp = outputs['preprocessing']['hypotheses']
    out_refs = outputs['preprocessing']['references']
    out_transposed_refs = outputs['preprocessing']['transposed_references']

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as hypotheses_path, tempfile.NamedTemporaryFile(suffix=".json", delete=False) as references_path:
        json.dump(inp_hyp, open(hypotheses_path.name, 'w'))
        json.dump(inp_refs, open(references_path.name, 'w'))

        inp = TextGenerationMetricInput(**{ 
            "hypotheses": hypotheses_path.name,
            "references": references_path.name,
            "supplier": "aiXplain",
            "metric": 'bleu'
        })
        transposed_references = utils.transpose(inp.references)

        assert out_hyp == inp.hypotheses
        assert out_refs == inp.references
        assert out_transposed_refs == transposed_references


class MockTextGenerationMetric(TextGenerationMetric):
    pass

def test_error_not_equal(inputs):
    scorer = MockTextGenerationMetric("mock-metric")

    inp = inputs['not_equal']
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as hypotheses_path, tempfile.NamedTemporaryFile(suffix=".json", delete=False) as references_path:
        json.dump(inp['hypotheses'], open(hypotheses_path.name, 'w'))
        json.dump(inp['references'], open(references_path.name, 'w'))
        files_to_be_deleted = [hypotheses_path.name, references_path.name]
        inp = { 
            "hypotheses": hypotheses_path.name,
            "references": references_path.name,
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
    assert str(exc_info.value) == "HTTP 400: Number of sources, hypotheses and references must be the same."


def test_error_empty(inputs):
    scorer = MockTextGenerationMetric("mock-metric")

    inp = inputs['empty']
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as hypotheses_path, tempfile.NamedTemporaryFile(suffix=".json", delete=False) as references_path:
        json.dump(inp['hypotheses'], open(hypotheses_path.name, 'w'))
        json.dump(inp['references'], open(references_path.name, 'w'))
        files_to_be_deleted = [hypotheses_path.name, references_path.name]
        inp = { 
            "hypotheses": hypotheses_path.name,
            "references": references_path.name,
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

def test_error_empty(inputs):
    scorer = MockTextGenerationMetric("mock-metric")

    inp = inputs['empty']
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as hypotheses_path, tempfile.NamedTemporaryFile(suffix=".json", delete=False) as references_path:
        json.dump(inp['hypotheses'], open(hypotheses_path.name, 'w'))
        files_to_be_deleted = [hypotheses_path.name, references_path.name]
        inp = { 
            "hypotheses": hypotheses_path.name,
            "references": references_path.name,
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
    scorer = MockTextGenerationMetric("mock-metric")

    inp = inputs['preprocessing']
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as hypotheses_path, tempfile.NamedTemporaryFile(suffix=".json", delete=False) as references_path:
        json.dump(inp['hypotheses'], open(hypotheses_path.name, 'w'))
        json.dump(inp['references'], open(references_path.name, 'w'))
        files_to_be_deleted = [hypotheses_path.name, references_path.name]

        inp = { 
            "hypotheses": "asdas",
            "references": references_path.name,
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