from ..classes.datasetfile import DatasetFile
from urllib.parse import urlencode
from typing import List
import requests

class DatasetFileService:
    def __init__(self, client):
        self.client = client

    def get_files(self) -> List[DatasetFile]:
        with requests.Session() as session:
            files = self.client.http_get("/api/datasetfiles", session=session)
            return [DatasetFile(f['fileId'],f['fileName'],f.get('numRows'),f['numColumns'], f['processingStatus'], f.get('processingError')) for f in files]
