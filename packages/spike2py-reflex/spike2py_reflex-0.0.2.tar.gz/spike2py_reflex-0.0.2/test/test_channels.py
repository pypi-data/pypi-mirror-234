import spike2py_reflex as s2pr


def test_init():
    chan = s2pr.info.Channels()
    assert chan._study is None
    assert chan._subject is None
    assert chan._section is None


def test_add_channels(demo_study_reflex):
    study_channel_info = demo_study_reflex['channels']
    chan = s2pr.info.Channels(study_channel_info)
    assert chan._study.emg == ['Fdi']
    assert chan._study.stim_intensity == 'Stim'
    expected = {'hreflex': {'channels': 'Ds8', 'type': 'double'},
 'mmax': {'channels': 'Mmax', 'type': 'single'},
 'ramp': {'channels': 'Ds8', 'type': 'single'}}
    assert chan._study.triggers == expected


def test_add_subject_no_channels(demo_study_reflex):
    study_channel_info = demo_study_reflex['channels']
    chan = s2pr.info.Channels(study_channel_info)
    chan.add_subject()
    assert chan._subject.emg == ['Fdi']
    assert chan._subject.stim_intensity == 'Stim'
    expected = {'hreflex': {'channels': 'Ds8', 'type': 'double'},
                'mmax': {'channels': 'Mmax', 'type': 'single'},
                'ramp': {'channels': 'Ds8', 'type': 'single'}}
    assert chan._subject.triggers == expected


def test_add_subject_channels(demo_study_reflex, subject_channels):
    study_channel_info = demo_study_reflex['channels']
    chan = s2pr.info.Channels(study_channel_info)
    chan.add_subject(subject_channels)
    assert chan._study.emg == ['Fdi']
    assert chan._subject.emg == ['MG']
    assert chan._study.stim_intensity == 'Stim'
    assert chan._subject.stim_intensity == 'zap'


def test_add_section_no_channels(demo_study_reflex):
    study_channel_info = demo_study_reflex['channels']
    chan = s2pr.info.Channels(study_channel_info)
    chan.add_subject()
    chan.add_section()
    assert chan._section.emg == ['Fdi']
    assert chan._section.stim_intensity == 'Stim'
    expected = {'hreflex': {'channels': 'Ds8', 'type': 'double'},
                'mmax': {'channels': 'Mmax', 'type': 'single'},
                'ramp': {'channels': 'Ds8', 'type': 'single'}}
    assert chan._section.triggers == expected


def test_add_section_channels(demo_study_reflex, subject_channels, section_channels):
    study_channel_info = demo_study_reflex['channels']
    chan = s2pr.info.Channels(study_channel_info)
    chan.add_subject(subject_channels)
    chan.add_section(section_channels)
    assert chan._section.emg == ['hh']
    assert chan._section.stim_intensity == 'zapzap'
    expected = {'H_reflex': {'channels': 'trig3', 'type': 'double'},
 'Mmax': {'channels': 'trig1', 'type': 'double'},
 'rRamp': {'channels': 'trig2', 'type': 'single'}}
    assert chan._section.triggers == expected

def test_clear(demo_study_reflex, subject_channels, section_channels):
    study_channel_info = demo_study_reflex['channels']
    chan = s2pr.info.Channels(study_channel_info)
    chan.add_subject(subject_channels)
    chan.add_section(section_channels)
    chan.clear_section()
    assert chan._section == None
    chan.clear_subject()
    assert chan._subject == None


def test_get_attributes_simple(demo_study_reflex):
    study_channel_info = demo_study_reflex['channels']
    chan = s2pr.info.Channels(study_channel_info)
    chan.add_subject()
    chan.add_section()
    assert chan.emg == ['Fdi']
    assert chan.stim_intensity == 'Stim'
    expected = {'hreflex': {'channels': 'Ds8', 'type': 'double'},
                'mmax': {'channels': 'Mmax', 'type': 'single'},
                'ramp': {'channels': 'Ds8', 'type': 'single'}}
    assert chan.triggers == expected


def test_get_attributes_complex(demo_study_reflex, subject_channels, section_channels):
    study_channel_info = demo_study_reflex['channels']
    chan = s2pr.info.Channels(study_channel_info)
    chan.add_subject(subject_channels)
    chan.add_section(section_channels)
    assert chan.emg == ['hh']
    assert chan.stim_intensity == 'zapzap'
    expected = {'H_reflex': {'channels': 'trig3', 'type': 'double'},
 'Mmax': {'channels': 'trig1', 'type': 'double'},
 'rRamp': {'channels': 'trig2', 'type': 'single'}}
    assert chan.triggers == expected
