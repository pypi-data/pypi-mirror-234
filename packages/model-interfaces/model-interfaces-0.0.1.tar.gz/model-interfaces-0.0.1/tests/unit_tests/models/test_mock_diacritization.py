from unittest.mock import Mock
from aixplain.model_interfaces.schemas.function_input import DiacritizationInput
from aixplain.model_interfaces.schemas.function_output import TextSegmentDetails, DiacritizationOutput
from aixplain.model_interfaces.interfaces.function_models import DiacritizationModel
from typing import Dict, List

class TestMockDiacritization():
    def test_predict(self):
        data = "السلام عليكم"
        supplier = "mockVoice"
        function = "diacritization"
        version = ""
        language = "Arabic"

        speech_recognition_input = {
            "data": data,
            "supplier": supplier,
            "function": function,
            "version": version,
            "language": language
        }

        predict_input = {"instances": [speech_recognition_input]}
        
        mock_model = MockModel("Mock")
        predict_output = mock_model.predict(predict_input)
        output_dict = predict_output["predictions"][0]

        assert output_dict["data"] == "السَّلَامُ عَلَيْكُمْ"
        assert output_dict["details"]["text"] == "السَّلَامُ عَلَيْكُمْ"
        assert output_dict["details"]["confidence"] == 0.7

class MockModel(DiacritizationModel):
    def run_model(self, api_input: Dict[str, List[DiacritizationInput]]) -> Dict[str, List[DiacritizationOutput]]:
        instances = api_input["instances"]
        predictions_list = []
        # There's only 1 instance in this case.
        for instance in instances:
            instance_data = instance.dict()
            model_instance = Mock()
            model_instance.process_data.return_value = ("السَّلَامُ عَلَيْكُمْ", 0.7)
            result, confidence = model_instance.process_data(instance_data["data"])
            model_instance.delete()
            
            # Map back onto DiacritizationOutput
            data = result
            details = {"text": result, "confidence": confidence}

            output_dict = {
                "data": data,
                "details": TextSegmentDetails(**details)
            }
            speech_recognition_output = DiacritizationOutput(**output_dict)
            predictions_list.append(speech_recognition_output)
        predict_output = {"predictions": predictions_list}
        return predict_output