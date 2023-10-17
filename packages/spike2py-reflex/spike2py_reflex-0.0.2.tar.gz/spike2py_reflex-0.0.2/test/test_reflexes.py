import spike2py_reflex as s2pr


def test_reflex_extract_hreflex_doubles(info_data_hreflex):
    info, data = info_data_hreflex
    section = s2pr.reflexes.extract(info, data)
    assert section.info.section == 'hreflex'
    assert list(section.reflexes.keys())[0] == 'Fdi'
    assert len(section.reflexes['Fdi'].reflexes) == 7
    assert len(section.reflexes['Fdi'].reflexes[0].waveform) == 794
    assert len(section.reflexes['Fdi'].reflexes[0].reflex1.waveform) == 109
    assert len(section.reflexes['Fdi'].reflexes[0].reflex2.waveform) == 109
    assert len(section.reflexes['Fdi'].x_axis_extract) == 794
    assert len(section.reflexes['Fdi'].x_axis_singles) == 109


def test_reflex_extract_ramp_singles(info_data_ramp):
    info, data = info_data_ramp
    section = s2pr.reflexes.extract(info, data)
    assert section.info.section == 'ramp'
    assert list(section.reflexes.keys())[0] == 'Fdi'
    assert len(section.reflexes['Fdi'].reflexes) == 1661
    assert len(section.reflexes['Fdi'].reflexes[0].waveform) == 90
    assert len(section.reflexes['Fdi'].x_axis_extract) == 90


def test_reflex_extract_mmax_singles(info_data_mmax):
    info, data = info_data_mmax
    section = s2pr.reflexes.extract(info, data)
    assert section.info.section == 'mmax'
    assert list(section.reflexes.keys())[0] == 'Fdi'
    assert len(section.reflexes['Fdi'].reflexes) == 6
    assert len(section.reflexes['Fdi'].reflexes[0].waveform) == 694
    assert len(section.reflexes['Fdi'].x_axis_extract) == 694
