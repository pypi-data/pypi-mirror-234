from dataclasses import dataclass


@dataclass
class StimParamsInfo:
#    kHz_fq: float
    train_fq: int
    double_isi: float


class StimParams:
    def __init__(self, study_stim_params_info=None):
        self._study = None
        self._subject = None
        self._section = None
        if study_stim_params_info is not None:
            self._study = StimParamsInfo(**study_stim_params_info)

    def add_subject(self, subject_stim_params_info=None):
        if subject_stim_params_info is not None:
            self._subject = StimParamsInfo(**subject_stim_params_info)
        elif subject_stim_params_info is None:
            self._subject = self._study

    def add_section(self, section_stim_params_info=None):
        if section_stim_params_info is not None:
            self._section = StimParamsInfo(**section_stim_params_info)
        elif section_stim_params_info is None:
            self._section = self._subject

    def clear_subject(self):
        self._subject = None

    def clear_section(self):
        self._section = None

    @property
    def kHz_fq(self):
        if self._section is not None:
            return self._section.kHz_fq
        elif self._subject is not None:
            return self._subject.kHz_fq
        elif self._study is not None:
            return self._study.kHz_fq
        else:
            return None

    @property
    def train_fq(self):
        if self._section is not None:
            return self._section.train_fq
        elif self._subject is not None:
            return self._subject.train_fq
        elif self._study is not None:
            return self._study.train_fq
        else:
            return None

    @property
    def double_isi(self):
        if self._section is not None:
            return self._section.double_isi
        elif self._subject is not None:
            return self._subject.double_isi
        elif self._study is not None:
            return self._study.double_isi
        else:
            return None
