import requests
from requests_toolbelt import MultipartEncoderMonitor
import json
from .ReturnTypes import APIJob
from .Job import Job
from .JobOptions import AudioJobOptions
from typing import List
from time import time, sleep
import mimetypes
import logging

SATUS_BASE_URL = "https://api.satus.dev/"

class SatusClient():
    
    JOBS_ENDPOINT = SATUS_BASE_URL + "jobs"
    AUDIO_FILE_ENDPOINT = SATUS_BASE_URL + "submit/audio/file"

    def __init__(self, api_key: str):
        """
        Initializes a new instance of the SatusClient class.

        Args:
            api_key (str): The API key to use for authentication.
        """
        self.api_key = api_key

    def all_jobs(self, filter : str = None) -> List[Job]:
            """
            Returns a list of all jobs available on the Satus API, optionally filtered by a string.

            Args:
                filter (str, optional): A string to filter the jobs by. Defaults to None.

            Returns:
                List[Job]: A list of Job objects representing the jobs returned by the API.
            """
            _current_url = self.JOBS_ENDPOINT

            if filter != None:
                _current_url += "?filter=" + filter

            response = requests.get(
                _current_url,
                headers = {
                    "x-satus-key": self.api_key,
                    "Accept": "application/json"
                }
            )
            
            parsed_response = json.loads(response.text)

            if response.status_code == 200 and parsed_response["status"] == "success" and parsed_response["jobs"] != None:
                    return [Job._from_all_jobs(APIJob.model_validate(job)) for job in parsed_response["jobs"]]
            else:
                if "message" in parsed_response:
                    raise Exception(parsed_response["message"])
                else:
                    raise Exception("Unknown error")
            
    def get_job(self, id : str) -> Job:
            """
            Retrieves a job with the specified ID from the Satus API.

            Args:
                id (str): The ID of the job to retrieve.

            Returns:
                Job: The job with the specified ID.

            Raises:
                Exception: If an error occurs while fetching the job.
            """

            _current_url = self.JOBS_ENDPOINT + "/" + id

            response = requests.get(
                _current_url,
                headers = {
                    "x-satus-key": self.api_key,
                    "Accept": "application/json"
                }
            )
            
            parsed_response = json.loads(response.text)

            if response.status_code == 200 and parsed_response["status"] == "success" and parsed_response["job"] != None:
                    return Job._from_jobs(APIJob.model_validate(parsed_response["job"]))
            else:
                if "message" in parsed_response:
                    raise Exception(parsed_response["message"])
                else:
                    raise Exception("Unknown error occured while fetching job")
            
    def await_result(self, id : str, timeout : int = 300, polling_interval : int = 10) -> Job:
            """
            Waits for a job with the given ID to complete, and returns the resulting Job object.

            Args:
                id (str): The ID of the job to wait for.
                timeout (int, optional): The maximum number of seconds to wait for the job to complete. Defaults to 300.
                polling_interval (int, optional): The number of seconds to wait between polling for job status updates. Defaults to 10.

            Raises:
                Exception: If the job fails or the timeout is exceeded.

            Returns:
                Job: The Job object representing the completed job, including results.
            """
            start = time()

            if polling_interval < 2:
                polling_interval = 2
                logging.warning("Polling interval too low, setting to minimal value of 2 seconds")
            
            while True:
                if time() - start > timeout:
                    raise Exception(f"Timeout of {timeout} seconds exceeded")
                try:
                    job = self.get_job(id)
                except Exception as e:
                    raise e
                
                if job.status == "completed":
                    return job
                elif job.status == "failed":
                    raise Exception(f"Job with ID {id} failed at step {job.step}")
                else:
                    sleep(polling_interval)

    def submit_audio(self, audio : str, options : AudioJobOptions = AudioJobOptions()) -> str:
            """
            Submits an audio file to the Satus API for transcription.

            Args:
                audio (str): The path to the audio file to submit.
                options (AudioJobOptions, optional): The options for the job. Defaults to AudioJobOptions().

            Raises:
                Exception: If an error occurs while submitting the job.

            Returns:
                str: The ID of the submitted job.
            """
            mime_type = mimetypes.guess_type(audio)[0]

            fields_dict = options.model_dump()
            
            for key, value in fields_dict.items():
                if type(value) == bool:
                    fields_dict[key] = str(value).lower()

            fields_dict["file"] = (audio, open(audio, 'rb'), mime_type)

            m = MultipartEncoderMonitor.from_fields(
                fields=fields_dict,
            )

            response = requests.post(
                self.AUDIO_FILE_ENDPOINT,
                headers = {
                    "x-satus-key": self.api_key,
                    "Accept": "application/json",
                    "Content-Type": m.content_type
                },
                data = m
            )

            parsed_response = json.loads(response.text)

            if response.status_code == 200 and parsed_response["status"] == "success" and parsed_response["jobId"] != None:
                return parsed_response['jobId']
            else:
                if "message" in parsed_response:
                    raise Exception(parsed_response["message"])
                else:
                    raise Exception("Unknown error")

