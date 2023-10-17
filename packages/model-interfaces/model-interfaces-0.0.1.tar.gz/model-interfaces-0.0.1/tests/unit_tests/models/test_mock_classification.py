from unittest.mock import Mock
from aixplain.model_interfaces.schemas.function_input import ClassificationInput
from aixplain.model_interfaces.schemas.function_output import Label, ClassificationOutput
from aixplain.model_interfaces.interfaces.function_models import ClassificationModel
from typing import Dict, List

class TestMockClassification():
    def test_predict(self):
        data = "What a good day!"
        supplier = "mockClass"
        function = "sentiment-analysis"
        version = ""
        language = "English"

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

        assert output_dict["data"] == "positive"
        assert output_dict["predicted_labels"][0]["label"] == "positive"
        assert output_dict["predicted_labels"][0]["confidence"] == 0.7

class MockModel(ClassificationModel):
    def run_model(self, api_input: Dict[str, List[ClassificationInput]]) -> Dict[str, List[ClassificationOutput]]:
        instances = api_input["instances"]
        predictions_list = []
        # There's only 1 instance in this case.
        for instance in instances:
            instance_data = instance.dict()
            model_instance = Mock()
            model_instance.process_data.return_value = ("positive", 0.7)
            result, confidence = model_instance.process_data(instance_data["data"])
            model_instance.delete()
            
            # Map back onto DiacritizationOutput
            data = result
            labels = [Label(label= result, confidence=confidence)]

            output_dict = {
                "data": data,
                "predicted_labels": labels
            }
            speech_recognition_output = ClassificationOutput(**output_dict)
            predictions_list.append(speech_recognition_output)
        predict_output = {"predictions": predictions_list}
        return predict_output