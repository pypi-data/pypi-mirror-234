from typing import List

from solar_api.classes.api_responses.single_detection_result import SingleDetectionResult

class RedactionResponse(dict):
    def __init__(self, original_text: str, redacted_text: str, usage: int, de_identify_results: List[SingleDetectionResult]):
        self.original_text = original_text
        self.redacted_text = redacted_text
        self.usage = usage
        self.de_identify_results = de_identify_results
        dict.__init__(self, original_text=original_text, redacted_text=redacted_text, usage=usage, de_identify_results=de_identify_results)

    def describe(self):
        print(self.original_text)
        print("|")
        print("▼")
        print(self.redacted_text)
        print("usage: " + str(self.usage))
        
        for x in self.de_identify_results:
            print(x.describe())