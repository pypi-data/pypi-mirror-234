import pytest
import spike2py_reflex as s2pr


@pytest.mark.plot
def test_outcome_summary_mmax_singles(info_data_mmax):
    info, data = info_data_mmax
    section = s2pr.reflexes.extract(info, data)
    section = s2pr.outcomes.calculate(section)
    s2pr.outcomes.summary(section)


# TODO: fix how fake data built to allow test to run; has to do with looking for section called 'mmax_2' but it is not specified in reflex windows
@pytest.mark.plot
def test_outcome_summary_mmax_single_two_muscles(info_data_mmax):
    info, data = info_data_mmax
    section = s2pr.reflexes.extract(info, data)
    section = s2pr.outcomes.calculate(section)
    section.reflexes['Adm'] = section.reflexes['Fdi']
    section.info.windows.ms_reflexes['Adm'] = section.info.windows.ms_reflexes[
        'Fdi']
    section.info.section = section.info.section + '_2'
    s2pr.outcomes.summary(section)


# TODO: fix how fake data built to allow test to run; has to do with looking for section called 'mmax_2' but it is not specified in reflex windows
@pytest.mark.plot
def test_outcome_summary_mmax_single_two_muscles_three_intensities(info_data_mmax):
    info, data = info_data_mmax
    section = s2pr.reflexes.extract(info, data)
    section = s2pr.outcomes.calculate(section)
    section.reflexes['Fdi'].avg_waveform[32] = 1
    section.reflexes['Fdi'].avg_waveform[35] = 1
    section.reflexes['Fdi'].mean_outcomes['mmax'][32] = section.reflexes['Fdi'].mean_outcomes['mmax'][1]
    section.reflexes['Fdi'].mean_outcomes['mmax'][35] = section.reflexes['Fdi'].mean_outcomes['mmax'][1]
    section.reflexes['Fdi'].mean_outcomes['hreflex'][32] = section.reflexes['Fdi'].mean_outcomes['hreflex'][1]
    section.reflexes['Fdi'].mean_outcomes['hreflex'][35] = section.reflexes['Fdi'].mean_outcomes['hreflex'][1]
    section.reflexes['Fdi'].reflexes[3].stim_intensity = 32
    section.reflexes['Fdi'].reflexes[2].stim_intensity = 32
    section.reflexes['Fdi'].reflexes[4].stim_intensity = 35
    section.reflexes['Fdi'].reflexes[5].stim_intensity = 35
    section.reflexes['Adm'] = section.reflexes['Fdi']
    section.info.windows.ms_reflexes['Adm'] = section.info.windows.ms_reflexes[
        'Fdi']
    section.info.section = section.info.section + '_3'
    s2pr.outcomes.summary(section)


@pytest.mark.plot
def test_outcome_summary_hreflex_singles(info_data_hreflex):
    info, data = info_data_hreflex
    section = s2pr.reflexes.extract(info, data)
    section = s2pr.outcomes.calculate(section)
    s2pr.outcomes.summary(section)


# TODO: fix how fake data built to allow test to run; has to do with looking for section called 'mmax_2' but it is not specified in reflex windows
@pytest.mark.plot
def test_outcome_summary_hreflex_singles_two_muscles(info_data_hreflex):
    info, data = info_data_hreflex
    section = s2pr.reflexes.extract(info, data)
    section = s2pr.outcomes.calculate(section)
    section.reflexes['Adm'] = section.reflexes['Fdi']
    section.info.windows.ms_reflexes['Adm'] = section.info.windows.ms_reflexes['Fdi']
    section.info.section = section.info.section + '_2'
    s2pr.outcomes.summary(section)



@pytest.mark.plot
def test_outcome_summary_mmax_singles(info_data_ramp):
    info, data = info_data_ramp
    section = s2pr.reflexes.extract(info, data)
    section = s2pr.outcomes.calculate(section)
    s2pr.outcomes.summary(section)
