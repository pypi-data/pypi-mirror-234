import os
from typing import IO, List, Optional
from solar_api.classes.api_responses.single_detection_result import SingleDetectionResult
from solar_api.classes.generator_config import GeneratorConfig
from solar_api.classes.httpclient import HttpClient
from solar_api.classes.api_responses.redaction_response import RedactionResponse
from solar_api.enums.pii_state import PiiState
from solar_api.services.dataset import DatasetService
from solar_api.services.datasetfile import DatasetFileService
from solar_api.classes.dataset import Dataset
from solar_api.classes.datasetfile import DatasetFile
from solar_api.classes.solarexception import DatasetNameAlreadyExists
from solar_api.util.upload_helper import upload
from urllib.parse import urlencode
import requests;

class SolarApi:
    '''Wrapper class for invoking Solar API

    Parameters
    ----------
    base_url : str
        The url to your Tonic instance. Do not include trailing backslashes
    api_key : str
        Your api token, this argument is optional.  It is recommended instead that you provide your api key by setting SOLAR_API_KEY in your environment

    Examples
    --------
    >>> SolarApi("http://localhost:3000")
    '''
    def __init__(self, base_url : str, api_key: Optional[str] = None):
        if api_key is None:
            api_key = os.environ.get("SOLAR_API_KEY")
            if api_key is None:
                raise Exception("No api key provided.  Please provide an api key or set SOLAR_API_KEY environment variable.")
        self.api_key = api_key
        self.client = HttpClient(base_url, self.api_key)
        self.dataset_service = DatasetService(self.client)
        self.datasetfile_service = DatasetFileService(self.client)

    def create_dataset(self, dataset_name:str):
        """Create a dataset, which is a collection of 1 or more files.

        Parameters
        -----
        dataset_name : str
            The name of the dataset.  Dataset names must be unique.


        Returns
        -------
        Dataset
            The newly created dataset


        Raises
        ------

        DatasetNameAlreadyExists
            If a dataset with the same name already exists

        """
        try:
            self.client.http_post("/api/dataset", data={"name": dataset_name})
        except requests.exceptions.HTTPError as e:
            if e.response.status_code==409:
                raise DatasetNameAlreadyExists(e)

        return self.get_dataset(dataset_name)

    def delete_dataset(self, dataset_name: str):
        params = { "datasetName": dataset_name}
        self.client.http_delete("/api/dataset/delete_dataset_by_name?" + urlencode(params))


    def upload_file(self, file_path: str, file_name: str) -> DatasetFile:
        """Upload file to Solar

        Parameters
        --------
        file_path : str
            Absolute path to file to be uploaded
        file_name : str
            Desired name of file once saved to Solar

        Returns
        -------
        DatasetFile
        A DatasetFile object represented the just uploaded file


        Raises
        ------

        DatasetFileMatchesExistingFile
            If the contents of the file matches an existing file


        Examples
        --------
        >>> with open('<path to file>','r') as f:
                solar.upload_file(f, '<file name>')
        """

        return upload(file_path, file_name, self.client)



    def get_dataset(self, dataset_name : str) -> Dataset:
        '''Get instance of Workspace class with specified workspace_id.

        Parameters
        ----------
        dataset_name : str
            The name for your dataset

        Returns
        -------
        Dataset

        Examples
        --------
        >>> dataset = tonic.get_dataset("llama_2_chatbot_finetune_v5")
        '''
        return self.dataset_service.get_dataset(dataset_name)

    def get_files(self) -> List[DatasetFile]:
        """
        Gets all files

        Returns
        ------
        List[DatasetFile]
        A list of all files
        """
        return self.datasetfile_service.get_files()
      
    def unredact_bulk(self, redacted_strings: List[str]) -> List[str]:
            """Un-redacts a list of strings.
            
            Parameters
            ----------
            redacted_strings : List[str]
                The list of redacted strings you want to un-redact.
    
            Returns
            -------
            List[str]
                The list of un-redacted strings.
            """
            
            response = self.client.http_post("/api/unredact", data=redacted_strings)            
            return response
    
    def unredact(self, redacted_string: str) -> str:
            """Un-redacts a string.
            
            Parameters
            ----------
            redacted_string : str
                The redacted string you want to un-redact.
    
            Returns
            -------
            str
                The un-redacted string
            """
            
            response = self.client.http_post("/api/unredact", data=[redacted_string])            
            return response
    
    def redact(self, string: str, generatorConfig: GeneratorConfig = dict()) -> RedactionResponse:
            """Redacts a string.
            
            Parameters
            ----------
            string : str
                The string to redact
            
            generatorConfig: GeneratorConfig
                A dictionary of PII entities with
    
            Returns
            -------
            RedactionResponse
                The redacted string along with ancillary information.
            """
            
            invalid_pii_states = [v for v in list(generatorConfig.values()) if v not in PiiState._member_names_]
            if(len(invalid_pii_states)>0):
                 raise Exception("Invalid generator config.  Possible values are Off, Synthesis, and Redaction.")                 

            endpoint = "/api/redact"
            response = self.client.http_post(endpoint, data={"text": string, "generatorConfig": generatorConfig})
            
            de_id_results = [SingleDetectionResult(x["start"], x["end"], x["label"], x["text"], x["score"]) for x in list(response["deIdentifyResults"])]

            return RedactionResponse(response["originalText"], response["redactedText"], response["usage"], de_id_results)