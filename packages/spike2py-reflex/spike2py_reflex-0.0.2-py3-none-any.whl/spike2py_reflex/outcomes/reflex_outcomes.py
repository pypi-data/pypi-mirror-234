import numpy as np

import spike2py_reflex as s2pr


def calculate(section):
    """Calculate outcomes of individual reflexes and all section reflexes

    For the summary outcomes, we calculate:
    1) The mean value of the outcomes from each reflex (or pairs of reflexes),
    2) Outcome value of the mean waveform.

    """
    section = calculate_for_individual_reflexes(section)
    section = s2pr.outcomes.calculate_mean_outcomes(section)
    section = s2pr.outcomes.calculate_outcomes_of_avg(section)
    return section


def calculate_for_individual_reflexes(section):
    """Calculate outcomes for each reflex of each muscle"""
    for muscle, reflexes in section.reflexes.items():
        if reflexes.type in [s2pr.utils.SINGLE, s2pr.utils.TRAIN]:
            section.reflexes[muscle] = _get_single_outcomes(reflexes, section.info.section)
        elif reflexes.type == s2pr.utils.DOUBLE:
            section.reflexes[muscle] = _get_double_outcomes(reflexes, section.info.section)
    return section


def _get_single_outcomes(reflexes, section_name):

    x_axis = reflexes.x_axis_extract
    sd_idx_all_stim_times = reflexes.sd_window_idx
    # Get idx windows of all reflexes types (e.g. H-reflex + mMax; or just mMax)
    reflex_win_idx_all = reflexes.reflex_windows_idx[section_name]


    for i in range(len(reflexes.reflexes)):
        waveform = reflexes.reflexes[i].waveform
        reflexes.reflexes[i].outcomes = dict()

        for reflex_type, reflex_idx_dict in reflex_win_idx_all.items():
            # Extract specific idx windows for current reflex type
            reflex_win_idx = reflex_idx_dict[reflexes.type]
            if reflexes.type == s2pr.utils.SINGLE:
                sd_idx = sd_idx_all_stim_times[reflexes.type]
            else:
                sd_idx = None

            outcomes, background_sd = get_outcomes_from(waveform, reflex_win_idx, sd_idx, x_axis)

            reflexes.reflexes[i].background_sd = background_sd
            reflexes.reflexes[i].outcomes[reflex_type] = outcomes

    return reflexes


def _get_double_outcomes(reflexes, section):

    x_axis = reflexes.x_axis_extract
    sd_idx_all_stim_times = reflexes.sd_window_idx
    reflex_win_idx_all = reflexes.reflex_windows_idx[section]

    for i in range(len(reflexes.reflexes)):
        reflexes.reflexes[i].reflex1.outcomes = dict()
        reflexes.reflexes[i].reflex2.outcomes = dict()
        reflexes.reflexes[i].ratio = dict()

        waveform = reflexes.reflexes[i].waveform

        for reflex_type, reflex_idx_dict in reflex_win_idx_all.items():
            reflex_win_idx = reflex_idx_dict[reflexes.type]
            sd_idx = sd_idx_all_stim_times[reflexes.type]

            # Reflex1
            reflex1_idx = reflex_win_idx[0]
            outcomes1, background_sd = get_outcomes_from(waveform, reflex1_idx, sd_idx, x_axis)
            reflexes.reflexes[i].reflex1.background_sd = background_sd
            reflexes.reflexes[i].reflex1.outcomes[reflex_type] = outcomes1

            # Reflex2
            if reflex_win_idx[1] is not None:
                reflex2_idx = reflex_win_idx[1]
                outcomes2, background_sd = get_outcomes_from(waveform, reflex2_idx, sd_idx, x_axis)
                reflexes.reflexes[i].reflex2.background_sd = background_sd
                reflexes.reflexes[i].reflex2.outcomes[reflex_type] = outcomes2
                if outcomes2.peak_to_peak is not None:
                    ratio = outcomes2.peak_to_peak / outcomes1.peak_to_peak
                else:
                    ratio = None
                reflexes.reflexes[i].ratio[reflex_type] = ratio
    return reflexes


def get_outcomes_from(waveform, reflex_idx, sd_win_idx, x_axis):
    onset = None
    background_sd = None
    amplitude = _get_amplitude(waveform, reflex_idx[0], reflex_idx[1])
    area = _get_area(waveform, reflex_idx[0], reflex_idx[1])
    if sd_win_idx is not None:
        onset_idx, background_sd = _get_onset(waveform, reflex_idx, sd_win_idx)
        if onset_idx is not None:
            onset = x_axis[onset_idx]
    outcomes = s2pr.outcomes.Outcomes(amplitude, area, onset)
    return outcomes, background_sd


def _get_amplitude(reflex_waveform, idx1, idx2):
    min_idx = np.argmin(reflex_waveform[idx1:idx2])
    max_idx = np.argmax(reflex_waveform[idx1:idx2])
    min_val = reflex_waveform[min_idx]
    max_val = reflex_waveform[max_idx]
    # Acccount for poor reflex window selection and both values are negative
    if max_val > 0:
        amplitude = max_val - min_val
    else:
        amplitude = max_val + min_val
    return amplitude


def _get_area(waveform, idx1, idx2):
    reflex_waveform = np.abs(waveform[idx1:idx2] - np.mean(waveform[idx1:idx2]))
    return np.trapz(reflex_waveform)


def _get_onset(waveform, reflex_idx, sd_win_idx):
    """Calculate onset of relex

    We use a threshold based on the amplitude of the background EMG activity
    and the s2pr.SD_MULTIPLIER (currently 3). However, the onset this is
    earlier than the point that crosses the threshold. It is the point where,
    going backwards from the crossing, the rectified EMG inflects back up.

    """
    abs_reflex = abs(waveform)
    abs_background_sd = np.std(abs_reflex[sd_win_idx[0]: sd_win_idx[1]])
    threshold = abs_background_sd * s2pr.utils.SD_MULTIPLIER

    # Determine if any value was greater than threshold
    threshold_crossed = sum(abs_reflex[reflex_idx[0]: reflex_idx[1]] > threshold)

    if threshold_crossed:
        crossing_idx = _get_crossing_idx(abs_reflex, reflex_idx, threshold)
        onset = _get_onset_idx(abs_reflex, crossing_idx)
        return onset, abs_background_sd
    else:
        return None, None


def _get_crossing_idx(abs_reflex, reflex_idx, threshold):
    for i in range(reflex_idx[0], reflex_idx[1]):
        if abs_reflex[i] > threshold:
            return i


def _get_onset_idx(abs_reflex, crossing_idx):
    for i in range(crossing_idx):
        if _inflexion_back_up(abs_reflex, crossing_idx):
            return crossing_idx - 1
        else:
            crossing_idx -= 1


def _inflexion_back_up(abs_reflex, crossing_idx):
    return abs_reflex[crossing_idx - 1] > abs_reflex[crossing_idx]
