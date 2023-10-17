import spike2py_reflex as s2pr


def test_init():
    ts = s2pr.info.TrialsSections()
    assert ts._study is None
    assert ts._subject is None
    assert ts._section is None


def test_get_attributes_simple(demo_study_reflex):
    study_ts_info = demo_study_reflex['trials_sections']
    ts = s2pr.info.TrialsSections(study_ts_info)
    ts.add_subject()
    ts.add_section()
    assert ts.trials_sections == {'biphasic_conv': ['mmax', 'ramp', 'hreflex'],
 'biphasic_high_fq': ['mmax', 'ramp', 'hreflex'],
 'monophasic_conv': ['mmax', 'ramp', 'hreflex'],
 'monophasic_high_fq': ['mmax', 'ramp', 'hreflex']}


def test_get_attributes_complex1(demo_study_reflex):
    study_ts_info = demo_study_reflex['trials_sections']
    ts = s2pr.info.TrialsSections(study_ts_info)
    sub_ts = {'a': ['mmax', 'ramp', 'hreflex'],
                                  'b': ['mmax', 'ramp', 'hreflex'],
                                  'c': ['mmax', 'ramp', 'hreflex'],
                                  'd': ['mmax']}
    ts.add_subject(sub_ts)
    ts.add_section()
    assert ts.trials_sections == sub_ts


def test_get_attributes_complex2(demo_study_reflex):
    study_ts_info = demo_study_reflex['trials_sections']
    ts = s2pr.info.TrialsSections(study_ts_info)

    ts.add_subject()
    sec_ts = {'1': ['mmfax', 'ramhp', 'hrneflex'],
              '2': ['mbmax', 'rnamp', 'hdreflex'],
              '3': ['mmaix', 'raymp', 'hre4flex'],
              '4': ['m5max']}
    ts.add_section(sec_ts)
    assert ts.trials_sections == sec_ts

