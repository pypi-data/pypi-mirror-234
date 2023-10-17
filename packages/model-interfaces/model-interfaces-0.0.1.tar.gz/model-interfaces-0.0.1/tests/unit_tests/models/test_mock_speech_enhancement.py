from unittest.mock import Mock
from aixplain.model_interfaces.schemas.function_input import SpeechEnhancementInput, AudioEncoding
from aixplain.model_interfaces.schemas.function_output import SpeechEnhancementOutput 
from aixplain.model_interfaces.interfaces.function_models import SpeechEnhancementModel
from typing import Dict, List

from aixplain.model_interfaces.utils.serialize import (
    encode
)

class TestMockSpeechEnhancement():
    def test_predict(self):
        data = encode(b"mock audio data")
        supplier = "mockVoice"
        function = "speech-enhancement"
        version = ""
        language = "English"
        audio_config = {
            "sampling_rate": 16000,
            "audio_encoding": AudioEncoding.WAV
        }

        speech_enhancement_input = {
            "data": data,
            "supplier": supplier,
            "function": function,
            "version": version,
            "language": language,
            "audio_config": audio_config
        }

        predict_input = {"instances": [speech_enhancement_input]}
        
        mock_model = MockModel("Mock")
        predict_output = mock_model.predict(predict_input)
        output_dict = predict_output["predictions"][0]

        assert output_dict["data"] == "VGhpcyBpcyBhbiBhdWRpbyBvdXRwdXQ="

class MockModel(SpeechEnhancementModel):
    def run_model(self, api_input: Dict[str, List[SpeechEnhancementInput]]) -> Dict[str, List[SpeechEnhancementOutput]]:
        instances = api_input["instances"]
        predictions_list = []
        # There's only 1 instance in this case.
        for instance in instances:
            instance_data = instance.dict()
            model_instance = Mock()
            model_instance.process_data.return_value = encode(b"This is an audio output")
            data = model_instance.process_data(instance_data["data"])
            model_instance.delete()
            
            audio_config = {
                "sampling_rate": 16000,
                "audio_encoding": AudioEncoding.WAV
            }
            output_dict = {
                "data": data,
                "audio_config": audio_config
            }
            speech_recognition_output = SpeechEnhancementOutput(**output_dict)
            predictions_list.append(speech_recognition_output)
        predict_output = {"predictions": predictions_list}
        return predict_output