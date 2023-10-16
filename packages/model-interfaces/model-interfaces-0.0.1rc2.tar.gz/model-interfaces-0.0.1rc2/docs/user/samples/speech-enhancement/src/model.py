import os, io
from typing import Dict, List

from aixplain.model_interfaces.interfaces.aixplain_model_server import AixplainModelServer
from aixplain.model_interfaces.interfaces.asset_resolver import AssetResolver
from aixplain.model_interfaces.schemas.function_input import AudioEncoding, SpeechEnhancementInput
from aixplain.model_interfaces.schemas.function_output import SpeechEnhancementOutput
from aixplain.model_interfaces.interfaces.function_models import SpeechEnhancementModel
from aixplain.model_interfaces.utils import serialize

import soundfile as sf, numpy as np, tensorflow as tf

MODEL_NOT_FOUND_ERROR = f"""
    Download model files using command:
        wget https://aixplain-kserve-models-dev.s3.amazonaws.com/serving-models/sample-models/speech-enhancement/dtln/dtln/saved_model.pb
        wget https://aixplain-kserve-models-dev.s3.amazonaws.com/serving-models/sample-models/speech-enhancement/dtln/dtln/variables/variables.data-00000-of-00001
        wget https://aixplain-kserve-models-dev.s3.amazonaws.com/serving-models/sample-models/speech-enhancement/dtln/dtln/variables/variables.index

        Save these in a folder called `dtln`
        dtln
        | - saved_model.pb
        | - variables
            | - variables.data-00000-of-00001
            | - variables.index
    """
SAMPLING_RATE = 16000

class SpeechEnhancer(SpeechEnhancementModel):

    def load(self):
        model_path = AssetResolver.resolve_path()
        if not os.path.exists(model_path):
            error_msg = f"Model not found in path: {model_path}\n" + MODEL_NOT_FOUND_ERROR
            raise ValueError(error_msg)
        self.model = tf.saved_model.load(model_path)
        self.infer = self.model.signatures['serving_default']
        self.ready = True

    def inference_processor(self, audio_file_handle):
        block_len = 512
        block_shift = 128
        audio, fs = sf.read(audio_file_handle)
        if fs != SAMPLING_RATE:
            raise ValueError('This model only supports 16k sampling rate.')
        out_file = np.zeros(len(audio))
        in_buffer = np.zeros(block_len)
        out_buffer = np.zeros(block_len)
        num_blocks = (audio.shape[0] - (block_len - block_shift)) // block_shift
        for idx in range(num_blocks):
            in_buffer[:-block_shift] = in_buffer[block_shift:]
            in_buffer[-block_shift:] = audio[idx * block_shift:idx * block_shift + block_shift]
            in_block = np.expand_dims(in_buffer, axis=0).astype('float32')
            out_block = self.infer(tf.constant(in_block))['conv1d_1']
            out_buffer[:-block_shift] = out_buffer[block_shift:]
            out_buffer[-block_shift:] = np.zeros(block_shift)
            out_buffer += np.squeeze(out_block)
            out_file[idx * block_shift:idx * block_shift + block_shift] = out_buffer[:block_shift]
        return out_file

    def run_model(self, api_input: Dict[(str, List[SpeechEnhancementInput])]) -> Dict[(str, List[SpeechEnhancementOutput])]:
        instances = api_input['instances']
        enhanced = []
        for instance in instances:
            file_handle = io.BytesIO()
            file_handle.write(instance.data)
            file_handle.seek(0)
            out_file = self.inference_processor(file_handle)
            model_output = io.BytesIO()
            sf.write(model_output, out_file, SAMPLING_RATE, format='wav')
            model_output.seek(0)
            enhanced.append(model_output.read())


        audio_config = {
            "sampling_rate": SAMPLING_RATE,
            "audio_encoding": AudioEncoding.WAV
        }
        predictions = []
        for enhanced_output in enhanced:
            output_dict = {
                # Convert output bytes to str using serialize.encode function
                "data": serialize.encode(enhanced_output),
                "audio_config": audio_config
            }
            speech_enhancement_output = SpeechEnhancementOutput(**output_dict)
            predictions.append(speech_enhancement_output)
            predict_output = {'predictions': predictions}

        return predict_output


if __name__ == '__main__':
    model = SpeechEnhancer(AssetResolver.asset_uri())
    model.load()
    AixplainModelServer(workers=1).start([model])
