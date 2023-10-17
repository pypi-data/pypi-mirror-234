__author__ = "ahmetgunduz"

import json
import pytest
import tempfile

from aixplain.model_interfaces.interfaces.metric_models import AudioGenerationMetric
from aixplain.model_interfaces.schemas.metric_input import AudioGenerationMetricInput

INPUTS_PATH = "tests/unit_tests/metrics/audio_generation/inputs.json"
OUTPUTS_PATH = "tests/unit_tests/metrics/audio_generation/outputs.json"


@pytest.fixture
def inputs():
    with open(INPUTS_PATH) as f:
        return json.load(f)


@pytest.fixture
def outputs():
    with open(OUTPUTS_PATH) as f:
        return json.load(f)


def test_input(inputs, outputs):
    inp_hyp = inputs["regular"]["hypotheses"]

    inp = AudioGenerationMetricInput(
        **{"hypotheses": inputs["regular"]["hypotheses"], "references": inputs["regular"]["references"], "supplier": "aiXplain", "metric": "test"}
    )

    assert inp.hypotheses == inputs["regular"]["hypotheses"]


class MockAudioGenerationMetric(AudioGenerationMetric):
    pass


def test_error_not_equal(inputs):
    scorer = MockAudioGenerationMetric("mock-metric")

    inp = inputs["not_equal"]
    with tempfile.NamedTemporaryFile() as hypotheses_path, tempfile.NamedTemporaryFile() as references_path:
        json.dump(inp["hypotheses"], open(hypotheses_path.name, "w"))
        json.dump(inp["references"], open(references_path.name, "w"))

        inp = {"hypotheses": hypotheses_path.name, "references": [references_path.name], "supplier": "aiXplain", "metric": "mock"}

        request = {"instances": [inp]}

        with pytest.raises(Exception) as exc_info:
            result = scorer.score(request)

        assert (
            str(exc_info.value)
            == "HTTP 400: Incorrect types passed into AudioGenerationMetricInput. Error: HTTP 400: Number of sources, hypotheses and references must be the same."
        )


def test_error_empty(inputs):
    scorer = MockAudioGenerationMetric("mock-metric")

    inp = inputs["empty"]
    with tempfile.NamedTemporaryFile() as hypotheses_path, tempfile.NamedTemporaryFile() as references_path:
        json.dump(inp["hypotheses"], open(hypotheses_path.name, "w"))
        json.dump(inp["references"], open(references_path.name, "w"))

        inp = {"hypotheses": hypotheses_path.name, "references": references_path.name, "supplier": "aiXplain", "metric": "mock"}

        request = {"instances": [inp]}

        with pytest.raises(Exception) as exc_info:
            result = scorer.score(request)

        assert str(exc_info.value) == "HTTP 400: Incorrect types passed into AudioGenerationMetricInput. Error: HTTP 400: List of hypotheses must not be empty."


def test_error_hypothesis_missing(inputs):
    scorer = MockAudioGenerationMetric("mock-metric")

    inp = inputs["regular"]
    with tempfile.NamedTemporaryFile() as hypotheses_path, tempfile.NamedTemporaryFile() as references_path:
        json.dump(inp["hypotheses"], open(hypotheses_path.name, "w"))
        json.dump(inp["references"], open(references_path.name, "w"))

        inp = {"hypotheses": "asdas", "references": references_path.name, "supplier": "aiXplain", "metric": "mock"}

        request = {"instances": [inp]}

        with pytest.raises(Exception) as exc_info:
            result = scorer.score(request)

        assert (
            str(exc_info.value)
            == "HTTP 400: Incorrect types passed into AudioGenerationMetricInput. Error: HTTP 400: Invalid hypotheses link. Error: [Errno 2] No such file or directory: 'asdas'"
        )
