from pathlib import Path
from typing import List

import spike2py_preprocess as s2pp
import spike2py_reflex as s2pr


class Info:
    """Information and functionality to required to process study data.

    Attributes
    ----------
    study_path : Path
        Path to study folder. Folder is to be structured as indicated in spike2py_preprocess docs.
    plot: Bool
        Flag indicating whether to generate plots.
    subjects: list
        List of subject IDs. Need to also be the name of the folder containing the subjects' data.
    channels: info.Channels
        Contains listing of relevant channels: emg, triggers, stim_intensity
    stim_params: info.StimParams
        Contains details related to transcutaneous spinal stimulation: kHz_fq, train_fq, double_isi
    trials_sections: info.TrialsSections
        Specifies trials and associated sections
    study_name: str
        Name of study, used in figures, numerical output, etc
    windows: info.Windows
    subject:
    trial:
    section:
    section_type:
    rejected_trig_windows:
    section_pkl:
    triggers:
    fs:
    """

    def __init__(self, study_path, plot=False):
        """
        Parameters
        ----------
        study_path: Path to study folder.
        plot: Flag indicating whether to generate plots
        """

        # Study
        self.study_path: Path = Path(study_path)
        self.plot: bool = plot

        study_info, reflex_info = self._get_study_info()

        self.subjects = study_info["subjects"]
        self.channels = s2pr.info.Channels(reflex_info["channels"])
        self.stim_params = s2pr.info.StimParams(reflex_info["stim_params"])
        self.trials_sections = s2pr.info.TrialsSections(reflex_info["trials_sections"])
        self.study_name: str = study_info["name"]
        self.windows = s2pr.info.Windows(reflex_info["windows"])
        self.windows.double_isi = self.stim_params.double_isi

        # Subject
        self.subject = None

        # Trial
        self.trial = None

        # Section
        self.section = None
        self.section_type = None
        self.rejected_trig_windows: List[list] = None
        self.section_pkl = None
        self.triggers = None

    @property
    def fs(self):
        return self.fs

    @fs.setter
    def fs(self, emg_fs):
        self.windows.fs = emg_fs

    def _get_study_info(self):
        study_info = s2pp.utils.read_json(self.study_path / s2pr.utils.STUDY_INFO_FILE)
        reflex_info = s2pp.utils.read_json(self.study_path / s2pr.utils.REFLEX_FILE)
        return study_info, reflex_info

    def clear_section(self):
        self.section = None
        self.section_type = None
        self.rejected_trigger_windows = None
        self.triggers = None
        self.channels.clear_section()
        self.windows.clear_section()
        self.trials_sections.clear_section()
        self.stim_params.clear_section()

    def clear_trial(self):
        self.trial = None

    def clear_subject(self):
        self.subject = None
        self.channels.clear_subject()
        self.windows.clear_subject()
        self.trials_sections.clear_subject()
        self.stim_params.clear_subject()

    def init_subject(self, sub_id):
        """Initilise subject

        Parameters
        ----------
        sub_id: str
            subject id, which should also be the name of the subject folder

            """
        self.subject = sub_id

        subject_reflex_info = None

        try:
            path = self.study_path / sub_id / s2pr.utils.SUBJECT_REFLEX_FILE
            subject_reflex_info = s2pp.utils.read_json(path, strict=False)
        except FileNotFoundError:
            print(f'subject {sub_id} does not have a reflex_info.json file')

        if subject_reflex_info is not None:
            if "channels" in subject_reflex_info:
                self.channels.add_subject(subject_reflex_info["channels"])
            else:
                self.channels.add_subject()
            if "windows" in subject_reflex_info:
                self.windows.add_subject(subject_reflex_info["windows"])
            else:
                self.windows.add_subject()
            if "trials_sections" in subject_reflex_info:
                self.trials_sections.add_subject(subject_reflex_info["trials_sections"])
            else:
                self.trials_sections.add_subject()
            if "stim_params" in subject_reflex_info:
                self.stim_params.add_subject(subject_reflex_info["stim_params"])
            else:
                self.stim_params.add_subject()

        elif subject_reflex_info is None:
            self.channels.add_subject()
            self.windows.add_subject()
            self.trials_sections.add_subject()
            self.stim_params.add_subject()

    def init_section(self, section_id):
        """Initialise a section
        
        Parameters
        ----------
        section_id: str
            Specificy the name of the section to process.
            Section has to be one of the TextMark sections from Spike2 file.

        """
        self.section = section_id

        pkl = self.trial + "_" + self.section + ".pkl"
        self.section_pkl = self.study_path / self.subject / "proc" / pkl

        section_reflex_info = None
        try:
            json = self.trial + "_" + self.section + "_reflex.json"
            path = self.study_path / self.subject / "proc" / json
            section_reflex_info = s2pp.utils.read_json(path, strict=False)
        except FileNotFoundError:
            print(f'{json} does not exist')

        if section_reflex_info is not None:
            if "channels" in section_reflex_info:
                self.channels.add_section(section_reflex_info["channels"])
            else:
                self.channels.add_section()

            if "windows" in section_reflex_info:
                self.windows.add_section(section_reflex_info["windows"])
            else:
                self.windows.add_section()

            if "trials_sections" in section_reflex_info:
                self.trials_sections.add_section(section_reflex_info["trials_sections"])
            else:
                self.trials_sections.add_section()

            if "stim_params" in section_reflex_info:
                self.stim_params.add_section(section_reflex_info["stim_params"])
            else:
                self.trials_sections.add_section()

            if "rejected_trigger_windows" in section_reflex_info:
                self._section_rejected_trigger_windows = section_reflex_info[
                    "rejected_trigger_windows"
                ]

        elif section_reflex_info is None:
            self.channels.add_section()
            self.windows.add_section()
            self.trials_sections.add_section()
            self.stim_params.add_section()
