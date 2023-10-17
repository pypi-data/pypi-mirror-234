from aixplain.model_interfaces.interfaces.asset_resolver import AssetResolver
from aixplain.model_interfaces.schemas.function_input import AudioEncoding

from aixplain.model_interfaces.utils.serialize import (
    audio_file_handle,
    encode
)
from model import SpeechEnhancer

class TestDTLNSpeechenhancement():
    def test_predict(self):
        file_path = 'src/assets/test.mp3'
        source_format = 'mp3'
        audio_config = {
            "sampling_rate": 16000,
            "audio_encoding": AudioEncoding.WAV
        }
        with audio_file_handle(file_path, source_format, out_format='wav') as file_handle:
            encoded = encode(file_handle.read())
        supplier = "test-supplier"
        function = "speech-enhancement"
        language = "English"

        input_dict = {
            "data": encoded,
            "supplier": supplier,
            "function": function,
            "language": language,
            "audio_config": audio_config
        }

        predict_input = {"instances": [input_dict]}
        
        dtln_model = SpeechEnhancer(AssetResolver.asset_uri())
        dtln_model.load()
        predict_output = dtln_model.predict(predict_input)
        output_dict = predict_output["predictions"][0]

        with open('decoded_ref_content.txt', 'r') as decode_handle:
            decoded_ref = decode_handle.read()
        assert output_dict["data"] == decoded_ref
