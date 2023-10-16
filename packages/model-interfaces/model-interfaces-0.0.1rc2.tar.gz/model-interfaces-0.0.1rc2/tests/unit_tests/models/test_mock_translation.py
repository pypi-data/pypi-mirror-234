from unittest.mock import Mock
from aixplain.model_interfaces.schemas.function_input import TranslationInput
from aixplain.model_interfaces.schemas.function_output import TextSegmentDetails, TranslationOutput 
from aixplain.model_interfaces.interfaces.function_models import TranslationModel
from typing import Dict, List

class TestMockTranslation():
    def test_predict(self):
        data = "Hello, how are you?"
        supplier = "mockVoice"
        function = "machine-translation"
        version = ""
        language = ""
        source_language = "English"
        source_dialect = ""
        target_language = "Spanish"
        target_dialect = ""

        translation_input = {
            "data": data,
            "supplier": supplier,
            "function": function,
            "version": version,
            "language": language,
            "source_language": source_language,
            "source_dialect": source_dialect,
            "target_language": target_language,
            "target_dialect": target_dialect
        }

        predict_input = {"instances": [translation_input]}
        
        mock_model = MockModel("Mock")
        predict_output = mock_model.predict(predict_input)
        translation_output_dict = predict_output["predictions"][0]

        assert translation_output_dict["data"] == "Hola, como estas?"
        assert translation_output_dict["details"]["text"] == "Hola, como estas?"
        assert translation_output_dict["details"]["confidence"] == 0.7

class MockModel(TranslationModel):
    def run_model(self, api_input: Dict[str, List[TranslationInput]]) -> Dict[str, List[TranslationOutput]]:
        instances = api_input["instances"]
        predictions_list = []
        # There's only 1 instance in this case.
        for instance in instances:
            instance_data = instance.dict()
            model_instance = Mock()
            model_instance.process_data.return_value = ("Hola, como estas?", 0.7)
            result, confidence = model_instance.process_data(instance_data["data"])
            model_instance.delete()
            
            # Map back onto TranslationOutput
            data = result
            details = {"text": result, "confidence": confidence}

            output_dict = {
                "data": data,
                "details": TextSegmentDetails(**details)
            }
            translation_output = TranslationOutput(**output_dict)
            predictions_list.append(translation_output)
        predict_output = {"predictions": predictions_list}
        return predict_output