from pydantic import BaseModel, validator
from typing import Any, Optional, List, Dict, Union
import tornado.web
from http import HTTPStatus

from aixplain.model_interfaces.schemas.function_input import AudioConfig, AudioEncoding
from aixplain.model_interfaces.utils import serialize

class APIOutput(BaseModel):
    """The standardized schema of the aiXplain's API Output.

    :param data:
        Processed output data from supplier model.
    :type data:
        Any
    :param details:
        Details of the output data. Optional.
    :type details:
        List[str] or Dict[str, str]
    """
    data: Any
    details: Optional[Union[List[str], Dict[str, str]]] = []

class WordDetails(BaseModel):
    """The standardized schema of the aiXplain's representation of word
    level details.
    
    :param word:
        A word from the text segment.
    :type word:
        string
    :param confidence:
        Confidence of prediction from the model.
    :type confidence:
        float
    :param details:
        A dictionary containing custom key and value pairs a to send the
        response of a model's additional word based outputs.
    :type details:
        Dict
    """
    word: str
    confidence: Optional[float]
    details: Optional[Dict[str, Any]]

class TextSegmentDetails(BaseModel):
    """The standardized schema of the aiXplain's representation of text
    segment level details.
    
    :param text:
        A text segment response from the model.
    :type text:
        string
    :param confidence:
        Confidence of prediction from the model.
    :type confidence:
        float
    :param word_details:
        A list of WordDetails.
    :type word_details:
        WordDetails
    """
    text: str
    confidence: Optional[float]
    word_details: Optional[List[WordDetails]]

class Label(BaseModel):
    """The standardized schema of the aiXplain's representation of label
    level details.
    
    :param label:
        A label associated with a predicted class.
    :type label:
        string
    :param confidence:
        Confidence of prediction from the model.
    :type confidence:
        float
    """
    label: str
    confidence: Optional[float]

class TranslationOutputSchema(APIOutput):
    """The standardized schema of the aiXplain's Translation Output.
    :param data:
        Processed output data from supplier model.
    :type data:
        Any
    :param details:
        Details of the text segments generated.
    :type details:
        TextSegmentDetails
    """ 
    details: TextSegmentDetails

class TranslationOutput(TranslationOutputSchema):
    def __init__(self, **input):
        try:
            super().__init__(**input)
        except ValueError:
             raise tornado.web.HTTPError(
                    status_code=HTTPStatus.BAD_REQUEST,
                    reason="Incorrect types passed into TranslationOutput"
                )  

class SpeechRecognitionOutputSchema(APIOutput):
    """The standardized schema of the aiXplain's Speech Recognition Output.
    :param data:
        Processed output data from supplier model.
    :type data:
        Any
    :param details:
        Details of the text segments generated.
    :type details:
        TextSegmentDetails
    """ 
    data: str
    details: TextSegmentDetails

class SpeechRecognitionOutput(SpeechRecognitionOutputSchema):
    def __init__(self, **input):
        try:
            super().__init__(**input)
        except ValueError:
             raise tornado.web.HTTPError(
                    status_code=HTTPStatus.BAD_REQUEST,
                    reason="Incorrect types passed into SpeechRecognitionOutput"
                )  

class DiacritizationOutputSchema(APIOutput):
    """The standardized schema of the aiXplain's Diacritization Output.
    :param data:
        Processed output data from supplier model.
    :type data:
        Any
    :param details:
        Details of the text segments generated.
    :type details:
        TextSegmentDetails
    """ 
    details: TextSegmentDetails

class DiacritizationOutput(DiacritizationOutputSchema):
    def __init__(self, **input):
        try:
            super().__init__(**input)
        except ValueError:
             raise tornado.web.HTTPError(
                    status_code=HTTPStatus.BAD_REQUEST,
                    reason="Incorrect types passed into DiacritizationOutput"
                )

class ClassificationOutput(APIOutput):
    """The standardized schema of the aiXplain's Classification Output.
    :param predicted_labels:
        A list of predicted labels by the model.
    :type predicted_labels:
        List[Label]
    :param all_labels:
        A list of all labels by the model, even if they were not considered as predicted.
        Optional.
    :type all_labels:
        List[Label]
    """ 
    predicted_labels: List[Label]
    all_labels: Optional[List[Label]]

class SpeechEnhancementOutputSchema(APIOutput):
    """The standardized schema of the aiXplain's Speech Enhancement Output.
    :param data:
        Output data string encoded in base64 encoding containing audio encoding
        defined by the audio_config parameter. 
        Use model_interfaces.utils.serialize.encode() function to encode audio data.

    :type data:
        str
    """ 
    data: str
    audio_config: AudioConfig

class SpeechEnhancementOutput(SpeechEnhancementOutputSchema):
    def __init__(self, **input):
        try:
            super().__init__(**input)
        except ValueError:
             raise tornado.web.HTTPError(
                    status_code=HTTPStatus.BAD_REQUEST,
                    reason="Incorrect types passed into SpeechRecognitionOutput"
                )

class SpeechSynthesisOutputSchema(BaseModel):
    """The standardized schema of the aiXplain's Speech Synthesis Output.
    :param data:
        Output data string encoded in base64 encoding containing audio encoding
        defined by the audio_config parameter. 
        Use model_interfaces.utils.serialize.encode() function to encode audio data.

    :type data:
        str
    """ 
    data: str
    audio_config: AudioConfig
    
class SpeechSynthesisOutput(SpeechSynthesisOutputSchema):
    def __init__(self, **input):
        try:
            super().__init__(**input)
        except ValueError:
             raise tornado.web.HTTPError(
                    status_code=HTTPStatus.BAD_REQUEST,
                    reason="Incorrect types passed into SpeechSynthesisOutput"
                )

class TextToImageGenerationOutputSchema(BaseModel):
    """The standardized schema of the aiXplain's Text-based Image Generation Output.
    :param data:
        Output image encoded in base64 encoding

    :type data:
        str
    """
    data: str

class TextToImageGenerationOutput(TextToImageGenerationOutputSchema):
    def __init__(self, **input):
        try:
            super().__init__(**input)
        except ValueError:
             raise tornado.web.HTTPError(
                    status_code=HTTPStatus.BAD_REQUEST,
                    reason="Incorrect types passed into TextToImageGenerationOutput"
                )