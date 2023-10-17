from dataclasses import dataclass
from typing import Union



@dataclass
class Outcomes:
    peak_to_peak: Union[float, None] = None
    area: Union[float, None] = None
    onset: Union[float, None] = None

