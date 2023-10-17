import spike2py_reflex as s2pr


def test_init():
    sp = s2pr.info.StimParams()
    assert sp._study is None
    assert sp._subject is None
    assert sp._section is None


def test_get_attributes_simple(demo_study_reflex):
    study_sp_info = demo_study_reflex['stim_params']
    sp = s2pr.info.StimParams(study_sp_info)
    sp.add_subject()
    sp.add_section()
    assert sp.train_fq == 30
    assert sp.double_isi == 50
#    assert sp.kHz_fq == 10


def test_get_attributes_complex1(demo_study_reflex):
    study_sp_info = demo_study_reflex['stim_params']
    sp = s2pr.info.StimParams(study_sp_info)
    sub_sp = {"train_fq": 10, "double_isi": 75}

    sp.add_subject(sub_sp)
    sp.add_section()
    assert sp.train_fq == 10
    assert sp.double_isi == 75


def test_get_attributes_complex2(demo_study_reflex):
    study_sp_info = demo_study_reflex['stim_params']
    sp = s2pr.info.StimParams(study_sp_info)
    sp.add_subject()
    sec_sp = {"train_fq": 40, "double_isi": 25}
    sp.add_section(sec_sp)
    assert sp.train_fq == 40
    assert sp.double_isi == 25
