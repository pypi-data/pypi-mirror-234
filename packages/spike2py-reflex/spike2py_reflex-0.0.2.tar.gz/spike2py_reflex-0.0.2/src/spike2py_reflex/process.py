from pathlib import Path
from typing import Union
import pickle

import spike2py as s2p
import spike2py_reflex as s2pr
import spike2py_preprocess as s2pp


def study(study_path: Path, plot=False):
    """Extract reflexes for all trials of all subject for a study

    Parameters
    ----------
    study_path: Path to study folder. Folder is to be structured as indicated in spike2py_preprocess docs
    plot: Flag indicating whether to generate plots
    """
    info = s2pr.info.Info(study_path, plot)
    for subject_ in info.subjects:
        subject(subject_, info=info, from_command_line=False)


def subject(subject_: str,
            info: Union[s2pr.info.Info, None] = None,
            study_path: Union[str, Path, None] = None,
            plot: bool = False,
            from_command_line: bool = False):
    """Process all trials and their sections for a given subject

    Parameters
    ----------
    subject_: Subject id, which also has to be the name of their folder
    study_path: Path to study folder; required if called via __main__ interface
    info: Study-related details; required if called internally
    plot: Whether to generate plots
    from_command_line: Whether function being called via __main__ interface

    """
    if from_command_line:
        study_path = Path(study_path)
        info = s2pr.info.Info(study_path, plot)
    info.clear_subject()
    info.init_subject(subject_)

    # Iterate over each trial for the subject
    for trial_, sections in info.trials_sections.trials_sections.items():
        trial(trial_=trial_, info=info, sections=sections)

    if plot:
        study_path = Path(study_path)
        subject_path = study_path / subject_ / 'figures' / 'reflexes'
        s2pp.utils.merge_pdfs(subject_path)


def trial(trial_: str,
          subject_: Union[str, None] = None,
          info: Union[s2pr.info.Info, None] = None,
          sections: Union[list, None] = None,
          study_path: Union[str, Path, None] = None,
          plot: bool = False,
          from_command_line: bool = False
          ):
    """ Process a given trial and its various sections

    Parameters
    ----------
    trial_: name of trial, as indicated in the associated .pkl file
    subject_: subject id; required when processing indivdual trial
    info: info related to study/subject; if not provided because processing a single trial,
          then it will be created.
    section: sections that need to be extracted and processed in given trial 
    study_path: absolute path to top-level study folder; required when processing a 
                single trial 
    plot: flag to determine whether or not to generate plots
    from_command_line: flag indentifying whether processing single trial (from command line
                       usually)
    """

    if from_command_line:
        study_path = Path(study_path)
        info = s2pr.info.Info(study_path, plot)
        info.clear_subject()
        info.init_subject(subject_)

    info.trial = trial_

    for section_ in sections:
        try:
            info.clear_section()
            info.init_section(section_)
            print(f'\tProcessing: {info.trial}-{section_}')
            print('\t\t', info.section_pkl)
            data = s2p.trial.load(info.section_pkl)
            info.triggers = s2pr.utils.Triggers(info, data)

            section = s2pr.reflexes.extract(info, data)
            section = s2pr.outcomes.calculate(section)

            if info.plot:
                s2pr.plot.reflexes(section)
                s2pr.plot.outcomes(section)

            _save_section_reflexes(section)
        except FileNotFoundError:
            print('\t\t Does not exists! Make sure this is expected.')


def _save_section_reflexes(section):
    section_pkl = section.info.section_pkl
    file_name = section_pkl.name
    file_name_parts = file_name.split('.')
    section_reflex_pkl_file_name = file_name_parts[0]+'_reflexes.' + file_name_parts[1]
    section_reflex_pkl = section_pkl.parent / section_reflex_pkl_file_name
    with open(section_reflex_pkl, "wb") as output:
        pickle.dump(section, output, pickle.HIGHEST_PROTOCOL)
