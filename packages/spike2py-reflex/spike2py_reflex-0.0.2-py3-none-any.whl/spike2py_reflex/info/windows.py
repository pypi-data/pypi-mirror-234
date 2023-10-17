import copy
from typing import Union
from dataclasses import dataclass

import numpy as np
from spike2py_preprocess.trial_sections import find_nearest_time_index

import spike2py_reflex as s2pr


@dataclass
class Window:
    single: Union[list, None] = None
    double: Union[list, None] = None
    double_single_pulse: Union[list, None] = None
    train_single_pulse: Union[list, None] = None


@dataclass
class WindowTypes:
    extract: Union[Window, None] = None
    plotting: Union[Window, None] = None
    reflexes: Union[dict, None] = None
    sd: Union[list, None] = None

    def clear(self):
        self.extract = Window()
        self.plotting = Window()
        self.reflexes = None
        self.sd = None


class GroupedWindows:
    """
    Windows and related info required to process data 

    Windows are defined in .json files, in ms. When the 
    sampling frequency and `double_isi` are provided, the
    various required indexes are computed.
    
    Attributes
    ----------
    fs: Union[float, int]
        data sampling rate
    x_axes: Window
        Computed x-axes for the various specified windows, 
        used for plotting and data extraction
    ms:
    idx
    double_isi
    idx_exists: bool
        Flag to track if idx have been computed


    """
    def __init__(self, win_info=None):
        """

        Parameters
        ----------
        win_info: dict 
            Info about windows provided in a .json file for the 
            study, subject or trial
        """
        self.fs = None
        self.x_axes = Window()
        self.ms = WindowTypes()
        self.ms.clear()  # To initialise
        self.idx = WindowTypes()
        self.idx.clear()  # To initialise
        self.double_isi = None

        self._idx_exists = False
        self._x_axis = None

        if win_info is not None:
            self.update(win_info)

    def clear(self):
        self.ms.clear()
        self.idx.clear()
        self._idx_exists = False
        self.x_axes = Window()

    def update(self, win_info):
        if "extract" in win_info:
            self.ms.extract = Window(**win_info["extract"])
        if "plotting" in win_info:
            self.ms.plotting = Window(**win_info["plotting"])
        if "reflexes" in win_info:
            self.ms.reflexes = win_info["reflexes"]
        if "sd" in win_info:
            self.ms.sd = win_info["sd"]

        if self.fs is not None:
            self._compute_idx_and_x_axes()

    def add_fs(self, fs):
        old_fs = self.fs
        self.fs = fs
        if old_fs != fs:
            self._get_x_axis()
            self._compute_idx_and_x_axes()

    def add_double_isi(self, double_isi):
        self.double_isi = double_isi

    def _compute_idx_and_x_axes(self):
        # TODO: see if this could be broken up into a few smaller methods
        # extract
        idx, x_axis = self._get_extract_idx_and_x_axis(self.ms.extract.single)
        self.idx.extract.single = idx
        self.x_axes.single = x_axis

        idx, x_axis = self._get_extract_idx_and_x_axis(self.ms.extract.double)
        self.idx.extract.double = idx
        self.x_axes.double = x_axis

        idx, x_axis = self._get_extract_idx_and_x_axis(self.ms.extract.double_single_pulse)
        self.idx.extract.double_single_pulse = idx
        self.x_axes.double_single_pulse = x_axis

        idx, x_axis = self._get_extract_idx_and_x_axis(self.ms.extract.train_single_pulse)
        self.idx.extract.train_single_pulse = idx
        self.x_axes.train_single_pulse = x_axis

        # reflexes
        self.idx.reflexes = dict()
        for emg_name, section_reflexes_windows in self.ms.reflexes.items():

            section_reflexes_with_window_idx = dict()

            for section, reflexes_windows in section_reflexes_windows.items():

                reflexes_with_window_idx = dict()
                for reflex_type_, reflex_ms in reflexes_windows.items():

                    idx1_single = find_nearest_time_index(self.x_axes.single, reflex_ms[0] * s2pr.utils.CONVERT_MS_TO_S)
                    idx2_single = find_nearest_time_index(self.x_axes.single, reflex_ms[1] * s2pr.utils.CONVERT_MS_TO_S)

                    idx1_double = find_nearest_time_index(self.x_axes.double, reflex_ms[0] * s2pr.utils.CONVERT_MS_TO_S)
                    idx2_double = find_nearest_time_index(self.x_axes.double, reflex_ms[1] * s2pr.utils.CONVERT_MS_TO_S)

                    try:
                        idx3_double = find_nearest_time_index(self.x_axes.double, (reflex_ms[0] + self.double_isi) * s2pr.utils.CONVERT_MS_TO_S)
                        idx4_double = find_nearest_time_index(self.x_axes.double, (reflex_ms[1] + self.double_isi) * s2pr.utils.CONVERT_MS_TO_S)
                    except TypeError:
                        print('Unable to compute double idx windows because double_isi not added to GroupWindows')
                        idx3_double = None
                        idx4_double = None

                    idx1_train = find_nearest_time_index(self.x_axes.train_single_pulse, reflex_ms[0] * s2pr.utils.CONVERT_MS_TO_S)
                    idx2_train = find_nearest_time_index(self.x_axes.train_single_pulse, reflex_ms[1] * s2pr.utils.CONVERT_MS_TO_S)

                    idx_for_reflex = {'single': [idx1_single, idx2_single],
                                      'double': [[idx1_double, idx2_double], [idx3_double, idx4_double]],
                                      'train': [idx1_train, idx2_train],
                                      }
                    reflexes_with_window_idx[reflex_type_] = idx_for_reflex
                section_reflexes_with_window_idx[section] = reflexes_with_window_idx
            self.idx.reflexes[emg_name] = section_reflexes_with_window_idx

        # sd
        self.idx.sd = dict()
        idx1_single = find_nearest_time_index(self.x_axes.single, self.ms.sd[0] * s2pr.utils.CONVERT_MS_TO_S)
        idx2_single = find_nearest_time_index(self.x_axes.single, self.ms.sd[1] * s2pr.utils.CONVERT_MS_TO_S)
        self.idx.sd['single'] = [idx1_single, idx2_single]
        self.idx.sd['double'] = None
        if self.double_isi is not None:
            idx1_double = find_nearest_time_index(self.x_axes.double, self.ms.sd[0] * s2pr.utils.CONVERT_MS_TO_S)
            idx2_double = find_nearest_time_index(self.x_axes.double, self.ms.sd[1] * s2pr.utils.CONVERT_MS_TO_S)
            self.idx.sd['double'] = [idx1_double, idx2_double]

        self._idx_exists = True

    def _get_extract_idx_and_x_axis(self, win: list):
        """Get indexes, relative to trig times (i.e. zero).

        Given the index of a trig time, apply the provided indexes to determine the indexes associated
        with the desired windows.

        Example: window for [-250ms , 50ms]
                 index of 0ms is 0
                 indexes for window are [-500, 100] # for a sampling of 2kHz
                 Thus, given the index of a trigger time (e.g. 1435) apply the window index
                 to determine data to extract (1435 + (-500), 1435 + 100)
         """
        zero_idx = find_nearest_time_index(self._x_axis, 0)
        lower_idx = find_nearest_time_index(self._x_axis, win[0] * s2pr.utils.CONVERT_MS_TO_S)
        upper_idx = find_nearest_time_index(self._x_axis, win[1] * s2pr.utils.CONVERT_MS_TO_S)
        idx = [lower_idx - zero_idx, upper_idx - zero_idx]
        x_axis = self._x_axis[lower_idx:upper_idx]
        return idx, x_axis

    def _get_x_axis(self):
        start = 1/self.fs
        stop = 1
        step = 1/self.fs
        positive_half_x_axis = np.arange(start, stop, step)
        negative_half_x_axis = -1 * (np.flip(positive_half_x_axis))
        middle = np.array([0])
        self._x_axis = np.concatenate([negative_half_x_axis, middle, positive_half_x_axis])


class Windows:
    """

    """

    def __init__(self, study_win_info):
        """

        Parameters
        ----------
        study_win_info
        fs
        """
        self._study = GroupedWindows(study_win_info)
        self._subject = GroupedWindows()
        self._subject_empty = True
        self._section = GroupedWindows()
        self._section_empty = True
        self.fs: Union[float, None] = None
        self.double_isi = None

    def add_subject(self, win_info=None):
        self._subject = copy.deepcopy(self._study)
        if win_info is not None:
            self._subject.update(win_info)
        self._subject_empty = False

    def add_section(self, win_info=None):
        self._section = copy.deepcopy(self._subject)
        if win_info is not None:
            self._section.update(win_info)
        self._section_empty = False

    def clear_subject(self):
        self._subject.clear()

    def clear_section(self):
        self._section.clear()

    @property
    def fs(self):
        return self.fs

    @fs.setter
    def fs(self, fs):
        self._study.add_fs(fs)
        if not self._subject_empty:
            self._subject.add_fs(fs)
        if not self._section_empty:
            self._section.add_fs(fs)

    @property
    def idx_sd(self):
        return self._section.idx.sd

    @property
    def idx_reflexes(self):
        return self._section.idx.reflexes

    @property
    def double_isi(self):
        if self._section.double_isi is not None:
            return self._section.double_isi
        if self._subject.double_isi is not None:
            return self._subject.double_isi
        if self._study.double_isi is not None:
            return self._study.double_isi
        else:
            return None

    @double_isi.setter
    def double_isi(self, double_isi):
        self._study.add_double_isi(double_isi)
        if not self._subject_empty:
            self._subject.add_double_isi(double_isi)
        if not self._section_empty:
            self._section.add_double_isi(double_isi)

    @property
    def idx_extract(self):
        return self._section.idx.extract

    @property
    def idx_plotting(self):
        return self._section.idx.plotting

    @property
    def x_axes(self):
        return self._section.x_axes

    @property
    def ms_sd(self):
        return self._section.ms.sd

    @property
    def ms_reflexes(self):
        return self._section.ms.reflexes

    @property
    def ms_extract(self):
        return self._section.ms.extract

    @property
    def ms_plotting(self):
        return self._section.ms.plotting
