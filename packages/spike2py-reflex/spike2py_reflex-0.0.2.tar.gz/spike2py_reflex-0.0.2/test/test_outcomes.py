import spike2py_reflex as s2pr
import pytest


def test_reflex_outcomes_hreflex_doubles_individual_reflexes(info_data_hreflex):
    info, data = info_data_hreflex
    section = s2pr.reflexes.extract(info, data)
    section = s2pr.outcomes.calculate_for_individual_reflexes(section)
    assert section.reflexes['Fdi'].reflexes[0].reflex1.outcomes['hreflex'].onset == pytest.approx(0.015625)
    assert section.reflexes['Fdi'].reflexes[0].reflex2.outcomes['hreflex'].peak_to_peak == pytest.approx(-0.005965828180407999)


def test_reflex_outcomes_ramp_doubles_individual_reflexes(info_data_ramp):
    info, data = info_data_ramp
    section = s2pr.reflexes.extract(info, data)
    section = s2pr.outcomes.calculate_for_individual_reflexes(section)
    assert section.reflexes['Fdi'].reflexes[0].outcomes['cool_reflex'].peak_to_peak == pytest.approx(-0.005139612876265053)
    assert section.reflexes['Fdi'].reflexes[0].outcomes['cool_reflex'].area == pytest.approx(0.15115431510702879)
    assert section.reflexes['Fdi'].reflexes[0].outcomes['cool_reflex'].onset is None


def test_reflex_outcomes_mmax_doubles_individual_reflexes(info_data_mmax):
    info, data = info_data_mmax
    section = s2pr.reflexes.extract(info, data)
    section = s2pr.outcomes.calculate_for_individual_reflexes(section)
    print(section.reflexes['Fdi'].reflexes[0].outcomes)
    assert section.reflexes['Fdi'].reflexes[0].outcomes['mmax'].peak_to_peak == pytest.approx(-0.0036865157257219843)
    assert section.reflexes['Fdi'].reflexes[0].outcomes['mmax'].area == pytest.approx(67.80426369321032)
    assert section.reflexes['Fdi'].reflexes[0].outcomes['hreflex'].onset == pytest.approx(0.020161290322580645)


def test_reflex_outcomes_hreflex_doubles_avg(info_data_hreflex):
    info, data = info_data_hreflex
    section = s2pr.reflexes.extract(info, data)
    section = s2pr.outcomes.calculate_for_individual_reflexes(section)
    section = s2pr.outcomes.calculate_outcomes_of_avg(section)
    assert len(section.reflexes['Fdi'].avg_reflex1[19].waveform) == 109
    assert section.reflexes['Fdi'].avg_reflex1[19].outcomes[
               'hreflex'].peak_to_peak == pytest.approx(-0.0003608836017132724)
    assert section.reflexes['Fdi'].avg_reflex2[19].outcomes[
               'hreflex'].area == pytest.approx(0.06735172606086091)


def test_reflex_outcomes_ramp_singles_avg(info_data_ramp):
    info, data = info_data_ramp
    section = s2pr.reflexes.extract(info, data)
    section = s2pr.outcomes.calculate_for_individual_reflexes(section)
    section = s2pr.outcomes.calculate_outcomes_of_avg(section)
    assert len(section.reflexes['Fdi'].avg_waveform) == 3
    assert len(section.reflexes['Fdi'].avg_waveform[10].waveform) == 90
    assert len(section.reflexes['Fdi'].avg_waveform[24].waveform) == 90
    assert section.reflexes['Fdi'].avg_waveform[10].outcomes['cool_reflex'].peak_to_peak == pytest.approx(0.012636357578906982)
    assert section.reflexes['Fdi'].avg_waveform[10].outcomes[
               'cool_reflex'].area == pytest.approx(0.06081335857846465)



def test_reflex_outcomes_mmax_singles_avg(info_data_mmax):
    info, data = info_data_mmax
    section = s2pr.reflexes.extract(info, data)
    section = s2pr.outcomes.calculate_for_individual_reflexes(section)
    section = s2pr.outcomes.calculate_outcomes_of_avg(section)
    assert len(section.reflexes['Fdi'].avg_waveform) == 1
    assert len(section.reflexes['Fdi'].avg_waveform[1].waveform) == 694
    assert section.reflexes['Fdi'].avg_waveform[1].outcomes['mmax'].peak_to_peak == pytest.approx(0.000937179558910316)
    assert section.reflexes['Fdi'].avg_waveform[1].outcomes[
               'hreflex'].peak_to_peak == pytest.approx(0.001988228210304802)


def test_reflex_outcomes_hreflex_doubles_mean(info_data_hreflex):
    info, data = info_data_hreflex
    section = s2pr.reflexes.extract(info, data)
    section = s2pr.outcomes.calculate_for_individual_reflexes(section)
    section = s2pr.outcomes.calculate_mean_outcomes(section)
    assert section.reflexes['Fdi'].mean_outcomes_reflex1['hreflex'][19]['outcomes'].peak_to_peak == pytest.approx(-0.00013157086170218784)
    assert section.reflexes['Fdi'].mean_outcomes_reflex1['hreflex'][19]['missing_outcomes'].peak_to_peak == 0
    assert section.reflexes['Fdi'].mean_outcomes_reflex1['hreflex'][19][
        'missing_outcomes'].onset == 0
    assert section.reflexes['Fdi'].mean_outcomes_reflex1['hreflex'][19][
        'present_outcomes'].onset == 7
    assert section.reflexes['Fdi'].mean_ratio['hreflex'][19]['ratio'] == pytest.approx(-1.0970691361542422)
    assert section.reflexes['Fdi'].mean_ratio['hreflex'][19]['missing_ratio'] == 0
    assert section.reflexes['Fdi'].mean_ratio['hreflex'][19]['present_ratio'] == 7


def test_reflex_outcomes_ramp_train_mean(info_data_ramp):
    info, data = info_data_ramp
    section = s2pr.reflexes.extract(info, data)
    section = s2pr.outcomes.calculate_for_individual_reflexes(section)
    section = s2pr.outcomes.calculate_mean_outcomes(section)
    assert section.reflexes['Fdi'].mean_outcomes['cool_reflex'][10]['outcomes'].peak_to_peak == pytest.approx(0.0010047763859973992)
    assert section.reflexes['Fdi'].mean_outcomes['cool_reflex'][10]['missing_outcomes'].peak_to_peak == 0
    assert section.reflexes['Fdi'].mean_outcomes['cool_reflex'][10]['missing_outcomes'].onset == 19
    assert section.reflexes['Fdi'].mean_outcomes['cool_reflex'][24][
               'missing_outcomes'].peak_to_peak == 0


def test_reflex_outcomes_mmax_single_mean(info_data_mmax):
    info, data = info_data_mmax
    section = s2pr.reflexes.extract(info, data)
    section = s2pr.outcomes.calculate_for_individual_reflexes(section)
    section = s2pr.outcomes.calculate_mean_outcomes(section)
    assert section.reflexes['Fdi'].mean_outcomes['mmax'][1]['outcomes'].peak_to_peak == pytest.approx(-0.0001343032256506074)
    assert section.reflexes['Fdi'].mean_outcomes['hreflex'][1]['missing_outcomes'].peak_to_peak == 0


def test_reflex_outcomes_mmax_single_mean_second_muscle(info_data_mmax):
    info, data = info_data_mmax
    section = s2pr.reflexes.extract(info, data)
    section.reflexes['Adm'] = section.reflexes['Fdi']
    section = s2pr.outcomes.calculate_for_individual_reflexes(section)
    section = s2pr.outcomes.calculate_mean_outcomes(section)
    assert section.reflexes['Adm'].mean_outcomes['mmax'][1]['outcomes'].peak_to_peak == pytest.approx(-0.0001343032256506074)
    assert section.reflexes['Adm'].mean_outcomes['hreflex'][1]['missing_outcomes'].peak_to_peak == 0
