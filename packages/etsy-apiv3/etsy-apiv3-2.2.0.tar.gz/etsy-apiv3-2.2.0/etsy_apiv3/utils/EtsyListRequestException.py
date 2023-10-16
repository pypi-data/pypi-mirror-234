from dataclasses import dataclass
from typing import List

@dataclass
class EtsyListRequestException(BaseException):
    status_code: int
    errors: List[str]