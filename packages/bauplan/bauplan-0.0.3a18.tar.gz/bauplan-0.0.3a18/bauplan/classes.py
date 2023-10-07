from dataclasses import dataclass
from typing import List


@dataclass
class Model:
    name: str
    columns: List[str]
