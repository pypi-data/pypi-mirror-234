import spike2py_reflex as s2pr


def test_init(study1_path):
    info = s2pr.info.Info(study1_path)
    assert info.subjects == ["sub01"]
    assert info.trial == None
    assert info.study_name == 'TSS_H-reflex'


def test_init_subject_section_with_no_reflex_file(study1_path):
    info = s2pr.info.Info(study1_path)
    info.init_subject('sub01')
    info.trial = 'biphasic_high_fq'
    info.init_section('ramp')
    assert info.subject == 'sub01'
    assert info.section == 'ramp'
    assert info.stim_params.train_fq == 21
    assert info.windows._section.ms.sd == [-205, -5]
    expected = {"biphasic_high_fq": ["mmax", "ramp", "hreflex"]}
    assert info.trials_sections.trials_sections == expected


def test_init_subject_section_with_reflex_file(study1_path):
    info = s2pr.info.Info(study1_path)
    info.init_subject('sub01')
    info.trial = 'biphasic_high_fq'
    info.init_section('mmax')
    assert info.subject == 'sub01'
    assert info.section == 'mmax'
    assert info.stim_params.train_fq == 66
    assert info.windows._section.ms.sd == [-102, -7]
    expected = {"biphasic_high_fq": ["mmax", "ramp", "hreflex"]}
    assert info.trials_sections.trials_sections == expected


def test_init_subject_section_with_reflex_file_and_not(study1_path):
    info = s2pr.info.Info(study1_path)
    info.init_subject('sub01')
    info.trial = 'biphasic_high_fq'
    info.init_section('mmax')
    assert info.subject == 'sub01'
    assert info.section == 'mmax'
    assert info.stim_params.train_fq == 66
    assert info.windows._section.ms.sd == [-102, -7]
    info.clear_section()
    info.init_section('ramp')
    assert info.stim_params.train_fq == 21
    assert info.windows._section.ms.sd == [-205, -5]
