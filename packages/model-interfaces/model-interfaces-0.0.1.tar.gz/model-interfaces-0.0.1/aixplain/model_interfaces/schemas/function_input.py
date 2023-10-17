from enum import Enum
from http import HTTPStatus
from typing import Optional, Any

from pydantic import BaseModel, validator
import tornado.web

from aixplain.model_interfaces.utils import serialize

class APIInput(BaseModel):
    """The standardized schema of the aiXplain's API input.
    
    :param data:
        Input data to the model.
    :type data:
        Any
    :param supplier:
        Supplier name.
    :type supplier:
        str
    :param function:
        The aixplain function name for the model. 
    :type function:
        str 
    :param version:
        The version number of the model if the supplier has multiple 
        models with the same function. Optional.  
    :type version:
        str
    :param language:
        The language the model processes (if relevant). Optional.
    :type language:
        str
    """
    data: Any
    supplier: Optional[str] = ""
    function: Optional[str] = ""
    version: Optional[str] = ""
    language: Optional[str] = ""

class AudioEncoding(Enum):
    """
    All supported audio encoding formats by the interface are
    enlisted in this enum. 
    """
    
    WAV = "wav" # 16 bit Linear PCM default wav format

class AudioConfig(BaseModel):
    """The standardized schema of the aiXplain's audio serialized data config.
    :param audio_encoding:
        Audio format of the audio data before base64 encoding.
        Chosen from the supported types in the enum AudioEncoding
        Supported encoding(s): wav
    :type audio_encoding:
        AudioEncoding
    :param sampling_rate:
        Sampling rate in hertz for the audio data. Optional.
    :type sampling_rate:
        int
    """
    audio_encoding: AudioEncoding
    sampling_rate: Optional[int]

class TranslationInputSchema(APIInput):
    """The standardized schema of the aiXplain's Translation API input.
    
    :param data:
        Input data to the model.
    :type data:
        Any
    :param supplier:
        Supplier name.
    :type supplier:
        str
    :param function:
        The aixplain function name for the model. 
    :type function:
        str 
    :param version:
        The version number of the model if the supplier has multiple 
        models with the same function. Optional.  
    :type version:
        str
    :param source_language:
        The source language the model processes for translation.
    :type source_language:
        str
    :param source_dialect:
        The source dialect the model processes (if specified) for translation.
        Optional.
    :type source_dialect:
        str
    :param target_language:
        The target language the model processes for translation.
    :type target_language:
        str
    """
    source_language: str
    source_dialect: Optional[str] = ""
    target_language: str
    target_dialect: Optional[str] = ""

class TranslationInput(TranslationInputSchema):
    def __init__(self, **input):
        super().__init__(**input)
        try:
            super().__init__(**input)
        except ValueError:
            raise tornado.web.HTTPError(
                    status_code=HTTPStatus.BAD_REQUEST,
                    reason="Incorrect types passed into TranslationInput."
                )

class SpeechRecognitionInputSchema(APIInput):
    """The standardized schema of the aiXplain's Speech Recognition API input.
    
    :param data:
        Input data to the model.
        Serialized base 64 encoded audio data in the audio encoding defined
        by the audio_config parameter.
    :type data:
        str
    :param audio_config:
        Configuration specifying the audio encoding parameters of the provided
        input.
    :type audio_config:
        AudioConfig
    :param supplier:
        Supplier name.
    :type supplier:
        str
    :param function:
        The aixplain function name for the model. 
    :type function:
        str 
    :param version:
        The version number of the model if the supplier has multiple 
        models with the same function. Optional.
    :type version:
        str
    :param language:
        The source language the model processes for Speech Recognition.
    :type language:
        str
    :param dialect:
        The source dialect the model processes (if specified) for Speech Recognition.
        Optional.
    :type dialect:
        str
    """
    data: str
    audio_config: AudioConfig
    language: str
    dialect: Optional[str] = ""

    @validator('data')
    def decode_data(cls, v):
        decoded = serialize.decode(v)
        return decoded

class SpeechRecognitionInput(SpeechRecognitionInputSchema):
    def __init__(self, **input):
        super().__init__(**input)
        try:
            super().__init__(**input)
        except ValueError:
            raise tornado.web.HTTPError(
                    status_code=HTTPStatus.BAD_REQUEST,
                    reason="Incorrect types passed into SpeechRecognitionInput."
                )

class DiacritizationInputSchema(APIInput):
    """The standardized schema of the aiXplain's diacritization API input.
    
    :param data:
        Input data to the model.
    :type data:
        Any
    :param supplier:
        Supplier name.
    :type supplier:
        str
    :param function:
        The aixplain function name for the model. 
    :type function:
        str 
    :param version:
        The version number of the model if the supplier has multiple 
        models with the same function. Optional.
    :type version:
        str
    :param language:
        The source language the model processes for diarization.
    :type language:
        str
    :param dialect:
        The source dialect the model processes (if specified) for diarization.
        Optional.
    :type dialect:
        str
    """
    language: str
    dialect: Optional[str] = ""

class DiacritizationInput(DiacritizationInputSchema):
    def __init__(self, **input):
        super().__init__(**input)
        try:
            super().__init__(**input)
        except ValueError:
            raise tornado.web.HTTPError(
                    status_code=HTTPStatus.BAD_REQUEST,
                    reason="Incorrect types passed into DiacritizationInput."
                )

class ClassificationInputSchema(APIInput):
    """The standardized schema of the aiXplain's classification API input.
    
    :param data:
        Input data to the model.
    :type data:
        Any
    :param supplier:
        Supplier name.
    :type supplier:
        str
    :param function:
        The aixplain function name for the model. 
    :type function:
        str 
    :param version:
        The version number of the model if the supplier has multiple 
        models with the same function. Optional.
    :type version:
        str
    :param language:
        The source language the model processes for classification.
    :type language:
        str
    :param dialect:
        The source dialect the model processes (if specified) for classification.
        Optional.
    :type dialect:
        str
    """
    language: Optional[str] = ""
    dialect: Optional[str] = ""

class ClassificationInput(ClassificationInputSchema):
    def __init__(self, **input):
        super().__init__(**input)
        try:
            super().__init__(**input)
        except ValueError:
            raise tornado.web.HTTPError(
                    status_code=HTTPStatus.BAD_REQUEST,
                    reason="Incorrect types passed into DiarizationInput."
                )

class SpeechEnhancementInputSchema(APIInput):
    """The standardized schema of the aiXplain's Speech Enhancement API input.
    
    :param data:
        Input data to the model.
        Serialized base 64 encoded audio data in the audio encoding defined
        by the audio_config parameter.
    :type data:
        str
    :param audio_config:
        Configuration specifying the audio encoding parameters of the provided
        input.
    :type audio_config:
        AudioConfig
    :param supplier:
        Supplier name.
    :type supplier:
        str
    :param function:
        The aixplain function name for the model. 
    :type function:
        str 
    :param version:
        The version number of the model if the supplier has multiple 
        models with the same function. Optional.
    :type version:
        str
    :param language:
        The source language the model processes for Speech Recognition.
    :type language:
        str
    :param dialect:
        The source dialect the model processes (if specified) for Speech Recognition.
        Optional.
    :type dialect:
        str
    """
    data: str
    audio_config: AudioConfig
    language: str
    dialect: Optional[str] = ""

    @validator('data')
    def decode_data(cls, v):
        decoded = serialize.decode(v)
        return decoded

class SpeechEnhancementInput(SpeechEnhancementInputSchema):
    def __init__(self, **input):
        super().__init__(**input)
        try:
            super().__init__(**input)
        except ValueError:
            raise tornado.web.HTTPError(
                    status_code=HTTPStatus.BAD_REQUEST,
                    reason="Incorrect types passed into SpeechRecognitionInput."
                )

class SpeechSynthesisInputSchema(BaseModel):
    """The standardized schema of the aiXplain's Speech Synthesis input.
    
    :param audio:
        Input audio to the model.
        Serialized base 64 encoded audio data in the audio encoding defined
        by the audio_config parameter.
        or a link to the audio file
    :type audio:
        str
    :param text:
        Input text to synthesize into audio.
    :type text:
        str
    :param language:
        Supplier name.
    :type language:
        str
    :param audio_config:
        Configuration specifying the audio encoding parameters of the provided
    :type audio_config:
        AudioConfig
    """
    speaker_id: str
    data: Optional[str] = ""
    audio: str = ""
    text: str
    text_language: str = "en"
    audio_config: AudioConfig = AudioConfig(audio_encoding = AudioEncoding.WAV)

class SpeechSynthesisInput(SpeechSynthesisInputSchema):
    def __init__(self, **input):
        data = input.get('data')
        if data == "":
            super().__init__(**input)
            try:
                super().__init__(**input)
            except ValueError:
                raise tornado.web.HTTPError(
                        status_code=HTTPStatus.BAD_REQUEST,
                        reason="Incorrect types passed into SpeechSynthesisInput."
                    )
        else:
            raise tornado.web.HTTPError(
                        status_code=HTTPStatus.BAD_REQUEST,
                        reason="Incorrect types passed into SpeechSynthesisInput. data field shouldn't be pass, and the data for audio file should be passed in field with the name [audio]"
                    )

class TextToImageGenerationInputSchema(BaseModel):
    """The standardized schema of the aiXplain's Text-based Image Generation API input.
    
    :param data:
        Input data to the model.
        Prompt for image generation
    :type data:
        str
    """
    data: str

class TextToImageGenerationInput(TextToImageGenerationInputSchema):
    def __init__(self, **input):
        super().__init__(**input)
        try:
            super().__init__(**input)
        except ValueError:
            raise tornado.web.HTTPError(
                    status_code=HTTPStatus.BAD_REQUEST,
                    reason="Incorrect type passed into TextToImageGenerationInput."
                )