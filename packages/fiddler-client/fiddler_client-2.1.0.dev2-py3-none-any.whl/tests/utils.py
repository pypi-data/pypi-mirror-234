from typing import Dict


class MockResponse:
    def __init__(self, response: Dict, status_code: int = 200) -> None:
        self.response = response
        self.status_code = status_code
        self.content = response

    def json(self) -> Dict:
        return self.response
