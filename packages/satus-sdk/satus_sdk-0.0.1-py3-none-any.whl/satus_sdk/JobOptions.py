from pydantic import BaseModel, Field
from typing import Union

class AudioJobOptions(BaseModel):
    """
    AudioJobOptions represents the options for an audio job.

    Args:
        language (str, optional): The language of the audio. Defaults to "auto".
        context_prompt (str, optional): The context prompt of the audio. Defaults to "".
        diarization (Union[bool, int], optional): The diarization of the audio. Defaults to False (or 0). If set to True (or 1), the diarization will be done automatically. If set to an integer >= 2, the diarization will be done with the given number of speakers.
        chapterize (bool, optional): The chapterization of the audio. Defaults to False.
        summarize (bool, optional): The summarization of the audio. Defaults to False.
        disfluency (bool, optional): The disfluency of the audio. Defaults to False.
        profanity (bool, optional): The profanity of the audio. Defaults to False.
        webhook (str, optional): The webhook of the audio. Defaults to None.
        share (bool, optional): The share of the audio. Defaults to False.
    """
    language : str = Field("auto")
    context_prompt : str = Field("")
    diarization : Union[bool, int] = Field(False)
    chapterize : bool = Field(False)
    summarize : bool = Field(False)
    disfluency : bool = Field(False)
    profanity : bool = Field(False)
    webhook : str = Field(None)
    share : bool = Field(False)
