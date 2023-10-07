from .ReturnTypes import Word, APIJob, Chapters

class Job():
    """
    Represents a job object that contains basic job information and results.

    Attributes:
        id (str): The job ID.
        step (str): The current step of the job.
        status (str): The status of the job.
        raw_duration (int): The raw duration of the job.
        language_code (str): The language code of the job.
        speech_duration (int): The speech duration of the job.
        sentences (list[list[Word]]): The list of sentences of the job.
        summary (str): The summary of the job.
        chapters (Chapters): The chapters of the job.
    """

    id: str = None
    step: str = None
    status: str = None
    raw_duration: int = None


    # results
    language_code: str = None
    speech_duration: int = None
    sentences: list[list[Word]] = None
    summary: str = None
    chapters: Chapters = None

    def __init__(self, id : str, step : str, status : str, raw_duration : int, language_code : str = None, speech_duration : int = None, sentences : list[list[Word]] = None, summary : str = None, chapters : Chapters = None):
        self.id = id
        self.step = step
        self.status = status
        self.raw_duration = raw_duration
        self.language_code = language_code
        self.speech_duration = speech_duration
        self.sentences = sentences
        self.summary = summary
        self.chapters = chapters

    def __str__(self):
        return f"Job {self.id}: {self.status} ({self.step})"
    
    @staticmethod
    def _from_all_jobs(job : APIJob):
        return Job(
            id = job.id,
            step = job.step,
            status = job.status,
            raw_duration = job.raw_duration
        )
    
    @staticmethod
    def _from_jobs(job : APIJob):
        return Job(
            id = job.id,
            step = job.step,
            status = job.status,
            raw_duration = job.raw_duration,
            language_code = job.language_code,
            speech_duration = job.speech_duration,
            sentences = job.sentences,
            summary = job.summary,
            chapters = job.chapters
        )
        