import copy


class TrialsSections:
    def __init__(self, study_trials_sections=None):
        self._study = None
        self._subject = None
        self._section = None
        if study_trials_sections is not None:
            self._study = study_trials_sections

    def add_subject(self, subject_trials_sections=None):
        if subject_trials_sections is not None:
            self._subject = subject_trials_sections
        elif subject_trials_sections is None:
            self._subject = copy.deepcopy(self._study)

    def add_section(self, section_trials_sections=None):
        if section_trials_sections is not None:
            self._section = section_trials_sections
        elif section_trials_sections is None:
            self._section = copy.deepcopy(self._subject)

    def clear_subject(self):
        self._subject = None

    def clear_section(self):
        self._section = None

    @property
    def trials_sections(self):
        if self._section is not None:
            return self._section
        else:
            return self._subject
