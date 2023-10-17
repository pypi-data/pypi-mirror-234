import pytest
import spike2py_reflex as s2pr


@pytest.mark.plot
def test_plot_mmax_outcomes(info_data_mmax):
    info, data = info_data_mmax
    section = s2pr.reflexes.extract(info, data)
    section = s2pr.outcomes.calculate(section)
    s2pr.plot.single_outcomes(section)


@pytest.mark.plot
def test_plot_mmax_outcomes_two_muscles(info_data_mmax):
    info, data = info_data_mmax
    section = s2pr.reflexes.extract(info, data)
    section = s2pr.outcomes.calculate(section)
    section.reflexes['Adm'] = section.reflexes['Fdi']
    section.info.windows.ms_reflexes['Adm'] = section.info.windows.ms_reflexes[
        'Fdi']
    section.info.section = section.info.section + '_2'
    s2pr.plot.single_outcomes(section)


@pytest.mark.plot
def test_plot_mmax_outcomes_two_muscles_three_intensities(info_data_mmax):
    info, data = info_data_mmax
    section = s2pr.reflexes.extract(info, data)
    section = s2pr.outcomes.calculate(section)
    section.reflexes['Fdi'].avg_waveform[32] = \
    section.reflexes['Fdi'].avg_waveform[1]
    section.reflexes['Fdi'].avg_waveform[35] = \
    section.reflexes['Fdi'].avg_waveform[1]
    section.reflexes['Fdi'].reflexes[3].stim_intensity = 32
    section.reflexes['Fdi'].reflexes[2].stim_intensity = 32
    section.reflexes['Fdi'].reflexes[4].stim_intensity = 35
    section.reflexes['Fdi'].reflexes[5].stim_intensity = 35
    section.reflexes['Adm'] = section.reflexes['Fdi']
    section.info.windows.ms_reflexes['Adm'] = section.info.windows.ms_reflexes[
        'Fdi']
    section.info.section = section.info.section + '_3'
    s2pr.plot.single_outcomes(section)


@pytest.mark.plot
def test_plot_outcomes_ramp_singles(info_data_ramp):
    info, data = info_data_ramp
    section = s2pr.reflexes.extract(info, data)
    section = s2pr.outcomes.calculate(section)
    s2pr.plot.train_outcomes(section)


@pytest.mark.plot
def test_plot_outcomes_ramp_singles_two_muscles(info_data_ramp):
    info, data = info_data_ramp
    section = s2pr.reflexes.extract(info, data)
    section = s2pr.outcomes.calculate(section)
    section.reflexes['Adm'] = section.reflexes['Fdi']
    section.info.windows.ms_reflexes['Adm'] = section.info.windows.ms_reflexes['Fdi']
    section.info.section = section.info.section + '_2'
    s2pr.plot.train_outcomes(section)


@pytest.mark.plot
def test_plot_outcomes_hreflex_doubles(info_data_hreflex):
    info, data = info_data_hreflex
    section = s2pr.reflexes.extract(info, data)
    section = s2pr.outcomes.calculate(section)
    s2pr.plot.double_outcomes(section)


@pytest.mark.plot
def test_plot_outocmes_hreflex_doubles_two_muscles(info_data_hreflex):
    info, data = info_data_hreflex
    section = s2pr.reflexes.extract(info, data)
    section = s2pr.outcomes.calculate(section)
    section.reflexes['Adm'] = section.reflexes['Fdi']
    section.info.windows.ms_reflexes['Adm'] = section.info.windows.ms_reflexes['Fdi']
    section.info.section = section.info.section + '_2'
    s2pr.plot.double_outcomes(section)



@pytest.mark.plot
def test_plot_outcomes_hreflex_doubles_two_muscles_three_intensities(info_data_hreflex):
    info, data = info_data_hreflex
    section = s2pr.reflexes.extract(info, data)
    section = s2pr.outcomes.calculate(section)
    section.reflexes['Fdi'].avg_waveform[25] = section.reflexes['Fdi'].avg_waveform[19]
    section.reflexes['Fdi'].avg_waveform[35] = section.reflexes['Fdi'].avg_waveform[19]
    section.reflexes['Fdi'].reflexes[3].stim_intensity = 25
    section.reflexes['Fdi'].reflexes[2].stim_intensity = 25
    section.reflexes['Fdi'].reflexes[4].stim_intensity = 35
    section.reflexes['Fdi'].reflexes[5].stim_intensity = 35
    section.reflexes['Fdi'].avg_reflex1[25] = section.reflexes['Fdi'].avg_reflex1[19]
    section.reflexes['Fdi'].avg_reflex1[35] = section.reflexes['Fdi'].avg_reflex1[19]
    section.reflexes['Fdi'].avg_reflex2[25] = section.reflexes['Fdi'].avg_reflex2[19]
    section.reflexes['Fdi'].avg_reflex2[35] = section.reflexes['Fdi'].avg_reflex2[19]
    section.reflexes['Adm'] = section.reflexes['Fdi']
    section.info.windows.ms_reflexes['Adm'] = section.info.windows.ms_reflexes['Fdi']
    section.info.section = section.info.section + '_3'
    s2pr.plot.double_outcomes(section)
