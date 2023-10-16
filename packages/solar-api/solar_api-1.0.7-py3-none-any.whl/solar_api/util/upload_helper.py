import os
import json
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper
from ..classes.httpclient import HttpClient
from ..classes.datasetfile import DatasetFile
from solar_api.classes.solarexception import DatasetFileMatchesExistingFile
import requests.exceptions;


def upload(file_path: str, file_name: str, client: HttpClient) -> DatasetFile:
    file_size = os.path.getsize(file_path)
    with open(file_path, 'rb') as f:
        with tqdm(desc=f"[INFO] Uploading", total=file_size, unit="B", unit_scale=True, unit_divisor=1024) as t:
            reader_wrapper = CallbackIOWrapper(t.update, f, "read")

            files = {
                'document': (None, json.dumps({"fileName": file_name, "csvConfig":{}}), 'application/json'),
                'file': reader_wrapper
            }

            try:
                file = client.http_post("/api/datasetfiles/upload_local_file", files=files)
                #numRows is null when a file is first uploaded
                return DatasetFile(file["fileId"], file["fileName"], file.get("numRows"), file["numColumns"], file['processingStatus'], file.get('processingError'))
            except requests.exceptions.HTTPError as e:
                if e.response.status_code==409:
                    raise DatasetFileMatchesExistingFile(e)
                else:
                    raise e