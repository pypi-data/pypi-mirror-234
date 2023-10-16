import json

class SingleDetectionResult(dict):
    def __init__(self, start: int, end: int, label: str, text: str, score: float):
        self.start = start
        self.end = end
        self.label = label
        self.text = text
        self.score = score
        dict.__init__(self, start=start, end=end, label=label, text=text, score=score)

    def describe(self):
        print(json.dumps(self))