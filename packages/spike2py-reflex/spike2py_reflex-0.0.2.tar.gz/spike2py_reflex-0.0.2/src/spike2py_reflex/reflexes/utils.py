from dataclasses import dataclass
from typing import Literal, Union

import numpy as np


@dataclass
class Outcomes:
    peak_to_peak: Union[float, None] = None
    area: Union[float, None] = None
    onset: Union[float, None] = None


@dataclass
class Single:
    waveform: np.array = None
    outcomes: Union[dict, None] = None
    background_sd: float = None
    stim_intensity: int = None
    extract_indexes: tuple = None


@dataclass
class Singles:
    x_axis_extract: np.array = None
    reflexes: list[Single] = None
    avg_waveform: dict = None
    mean_outcomes: Union[list, None] = None
    type: Literal["single", "double", "train"] = None
    sd_window_idx: list = None
    reflex_windows_idx: dict = None
    sd_window_ms: list = None
    reflex_windows_ms: dict = None


@dataclass
class Double:
    waveform: np.array = None
    reflex1: Single = None
    reflex2: Single = None
    ratio: Union[dict, None] = None
    stim_intensity: int = None
    extract_indexes: tuple = None


@dataclass
class Doubles:
    x_axis_extract: np.array = None
    x_axis_singles: np.array = None
    reflexes: list[Double] = None
    avg_reflex1: Single = None
    avg_reflex2: Single = None
    avg_waveform = None
    mean_outcomes_reflex1: Union[list, None] = None
    mean_outcomes_reflex2: Union[list, None] = None
    mean_ratio: float = None
    type: Literal["single", "double", "train"] = None
    sd_window_idx: list = None
    reflex_windows_idx: dict = None
    sd_window_ms: list = None
    reflex_windows_ms: dict = None


class SectionReflexes:
    def __init__(self, info, reflexes):
        self.info = info
        self.reflexes: dict = reflexes
