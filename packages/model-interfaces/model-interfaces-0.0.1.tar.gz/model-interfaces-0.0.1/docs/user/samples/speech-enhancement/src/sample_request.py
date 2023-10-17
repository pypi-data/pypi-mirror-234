import sys
import requests

from aixplain.model_interfaces.utils import serialize

HOST="localhost"
PORT=8080
MODEL_NAME="dtln"

url = f"http://{HOST}:{PORT}/v1/models/{MODEL_NAME}:predict"

file_path = 'src/assets/test.mp3'
source_format = 'mp3'
audio_config = {
    "sampling_rate": 16000,
    "audio_encoding": "wav"
}

with serialize.audio_file_handle(file_path, source_format, out_format="wav") as file_handle:
    audio_file_contents = file_handle.read()

encoded = serialize.encode(audio_file_contents)
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


response = requests.post(url, json=predict_input)

print(response.status_code)
print(response.json())