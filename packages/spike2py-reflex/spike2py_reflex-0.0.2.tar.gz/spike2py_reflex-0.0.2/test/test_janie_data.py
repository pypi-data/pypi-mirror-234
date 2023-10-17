from pathlib import Path

import spike2py_reflex as s2pr


def test_5hkz_bi_tss_tss():
    trial_ = '5khz_bi_tss'
    subject_ = 'S4'
    from_command_line = True
    plot=True
    sections = ["mmax_pre", "mmax_post", "tss"]
    study_path = Path('/home/martin/Dropbox/Martin/sketchbook/python/projects/spike2py_reflex/test/data/study5')


def test_process_study():
    study_path = Path('/home/martin/Dropbox/Martin/sketchbook/python/projects/spike2py_reflex/test/data/study5')
    s2pr.process.study(study_path, plot=True)
