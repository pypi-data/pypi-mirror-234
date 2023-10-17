from pathlib import Path

import spike2py_reflex as s2pr


def test_process_study():
    study_path = Path('/home/martin/Dropbox/Martin/sketchbook/python/projects/spike2py_reflex/test/data/study1')
    s2pr.process.study(study_path, plot=True)


def test_process_subject():
    study_path = Path('/home/martin/Dropbox/Martin/sketchbook/python/projects/spike2py_reflex/test/data/study1')
    subject_ = 'sub01'
    from_command_line = True
    s2pr.process.subject(subject_=subject_,
                         study_path=study_path,
                         plot=True,
                         from_command_line=from_command_line)


def test_process_trial():
    study_path = Path('/home/martin/Dropbox/Martin/sketchbook/python/projects/spike2py_reflex/test/data/study1')
    subject_ = 'sub01'
    from_command_line = True
    trial = 'biphasic_high_fq'
    section_ = ["mmax", "ramp", "hreflex"]
    s2pr.process.trial(trial_=trial,
                         sections=section_,
                         subject_=subject_,
                         study_path=study_path,
                         plot=True,
                         from_command_line=from_command_line)
