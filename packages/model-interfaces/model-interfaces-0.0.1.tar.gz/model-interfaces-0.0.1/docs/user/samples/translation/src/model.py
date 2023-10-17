import os
from typing import Dict, List

from transformers import MarianMTModel, MarianTokenizer

from aixplain.model_interfaces.interfaces.aixplain_model_server import AixplainModelServer
from aixplain.model_interfaces.interfaces.asset_resolver import AssetResolver
from aixplain.model_interfaces.schemas.function_input import TranslationInput
from aixplain.model_interfaces.schemas.function_output import TextSegmentDetails, TranslationOutput
from aixplain.model_interfaces.interfaces.function_models import TranslationModel

MODEL_NOT_FOUND_ERROR = """
    Download model file using command:
    # TODO (krishnadurai): Host this on a public URL
    aws s3 cp --recursive s3://aixplain-kserve-models-dev/serving-models/custom-models/onboarding-dev/helsinki-opus-mt-es-en .
"""


class MTModel(TranslationModel):
    def load(self):
        model_path = AssetResolver.resolve_path()
        if not os.path.exists(model_path):
            raise ValueError(MODEL_NOT_FOUND_ERROR)
        self.tokenizer = MarianTokenizer.from_pretrained(model_path)
        self.model = MarianMTModel.from_pretrained(model_path)
        self.ready = True

    def parse_inputs(self, inputs):
        parsed_inputs = []
        for inp in inputs:
            src_text = inp.data
            parsed_inputs.append(src_text)
        return parsed_inputs

    def run_model(self, api_input: Dict[str, List[TranslationInput]]) -> Dict[str, List[TranslationOutput]]:
        src_text = self.parse_inputs(api_input["instances"])

        translated = self.model.generate(
            **self.tokenizer(
                src_text, return_tensors="pt", padding=True
            )
        )

        predictions = []
        for t in translated:
            data = self.tokenizer.decode(t, skip_special_tokens=True)
            details = TextSegmentDetails(text=data)
            output_dict = {
                "data": data,
                "details": details
            }
            translation_output = TranslationOutput(**output_dict)
            predictions.append(translation_output)
            predict_output = {"predictions": predictions}
        return predict_output


if __name__ == "__main__":
    model = MTModel(AssetResolver.asset_uri())
    model.load()
    AixplainModelServer(workers=1).start([model])