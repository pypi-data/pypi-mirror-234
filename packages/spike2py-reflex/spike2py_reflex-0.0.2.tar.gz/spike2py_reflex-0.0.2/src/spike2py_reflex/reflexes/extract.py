import spike2py_reflex as s2pr


def extract(info, data):
    """Extract reflexes for all muscles (emg) in section.

    Parameters
    ----------
    info: s2pr.Info
      Contains details about all aspects of the study and its processing
    data: spike2py.trial.Trial
      Data of trial section being analysed

    Returns
    -------
    s2pr.SectionReflexes, which contains the reflexes and supplementary details
    of the current setion.
    """
    stim_int = s2pr.utils.get_stim_intensity(info, data)
    extracted = dict()

    for emg_name in info.channels.emg:
        emg = getattr(data, emg_name)
        # specify sampling frequency to trigger computation of idx
        info.windows.fs = emg.info.sampling_frequency
        if info.triggers.type in [s2pr.utils.SINGLE, s2pr.utils.TRAIN]:
            muscle_reflexes = _extract_single_reflexes(
                emg_name, emg, stim_int, info
            )
        elif info.triggers.type == s2pr.utils.DOUBLE:
            muscle_reflexes = _extract_double_reflexes(
                emg_name, emg, stim_int, info
            )
        extracted[emg_name] = muscle_reflexes

    return s2pr.reflexes.SectionReflexes(info, extracted)


def _extract_single_reflexes(emg_name, emg, stim_intensities, info):
    """Extract reflexes from single or train stimulation"""

    extract_idxs = _get_extract_idx_singles(info)
    x_axis = _get_x_axis(info)
    reflexes = _get_single_reflexes(extract_idxs, stim_intensities, emg)

    muscle_reflexes = s2pr.reflexes.Singles(
        x_axis_extract=x_axis,
        reflexes=reflexes,
        type=info.triggers.type,
        sd_window_idx=info.windows.idx_sd,
        sd_window_ms=info.windows.ms_sd,
        reflex_windows_idx=info.windows.idx_reflexes[emg_name],
        reflex_windows_ms=info.windows.ms_reflexes[emg_name],
    )
    return muscle_reflexes



def _get_extract_idx_singles(info):
    """Get idx of each window from which to extract single reflexes"""

    extract_idxs = list()

    trigger_type = s2pr.utils.SINGLE
    if info.triggers.type == s2pr.utils.TRAIN:
        trigger_type = s2pr.utils.TRAIN_SINGLE_PULSE

    extract_idx = getattr(info.windows.idx_extract, trigger_type)

    for trigger_idx in info.triggers.extract:
        extract_idxs.append(_get_window(trigger_idx, extract_idx))
    if extract_idxs[0][0] < 0:
        extract_idxs.pop(0)

    return extract_idxs


def _get_window(trigger_idx, window_idx):
    """Get a pair of idx values to extract reflex from a trigger"""
    if trigger_idx is None:
        return [None, None]
    lower = trigger_idx + window_idx[0]
    upper = trigger_idx + window_idx[1]
    return [lower, upper]


def _get_x_axis(info):
    if info.triggers.type == s2pr.utils.SINGLE:
        x_axis = info.windows.x_axes.single
    elif info.triggers.type == s2pr.utils.TRAIN:
        x_axis = info.windows.x_axes.train_single_pulse
    return x_axis


def _get_single_reflexes(trigger_windows, stim_intensities, emg):
    """Extract reflexes based on window idx for each trigger"""
    reflexes = list()
    for (idx1_extract, idx2_extract), intensity in zip(
            trigger_windows, stim_intensities
    ):
        try:
            reflexes.append(
                s2pr.reflexes.Single(
                    waveform=emg.values[idx1_extract:idx2_extract],
                    extract_indexes=(emg.times[idx1_extract], emg.times[idx2_extract]),
                    stim_intensity=intensity,
                )
            )
        except IndexError:
            print(f'Dropped a reflex asking for idx1 {idx1_extract} and idx2 {idx2_extract},'
                  f'from signal with length {len(emg.times)}')
    return reflexes


def _extract_double_reflexes(emg_name, emg, stim_intensities, info):
    """Extract reflexes from double stimulations"""

    trigger_windows = _get_extract_idx_doubles(info)
    reflexes = _get_double_reflexes(trigger_windows, stim_intensities, emg)

    muscle_reflexes = s2pr.reflexes.Doubles(
        x_axis_extract=info.windows.x_axes.double,
        x_axis_singles=info.windows.x_axes.double_single_pulse,
        reflexes=reflexes,
        type=info.triggers.type,
        sd_window_idx=info.windows.idx_sd,
        sd_window_ms=info.windows.ms_sd,
        reflex_windows_idx=info.windows.idx_reflexes[emg_name],
        reflex_windows_ms=info.windows.ms_reflexes[emg_name],
    )
    return muscle_reflexes


def _get_extract_idx_doubles(info) -> list:
    """Get windows to extract double, and each reflex individually

    Returns
    -------

    List of lists. Each item in list represents one double. For each of these, there are three pairs of indexes.
    These are to extract 1) the entire double, 2) the first reflex, and 3) the second reflex.

    e.g. [[extract_start, extract_end], [reflex1_start, reflex1_end], [reflex2_start, reflex2_end]] , ...]
    """
    extract_idxs = list()
    extract_idx = getattr(info.windows.idx_extract, info.triggers.type)
    double_idx = getattr(info.windows.idx_extract, "double_single_pulse")
    for trigger_idx_extract, trigger_idx_double in zip(
        info.triggers.extract, info.triggers.double
    ):
        extract = _get_window(trigger_idx_extract, extract_idx)
        reflex1 = _get_window(trigger_idx_double[0], double_idx)
        reflex2 = _get_window(trigger_idx_double[1], double_idx)
        extract_idxs.append([extract, reflex1, reflex2])
    return extract_idxs


def _get_double_reflexes(trigger_windows, stim_intensities, emg):
    reflexes = list()

    for (
            (idx1_extract, idx2_extract),
            (idx1_reflex1, idx2_reflex1),
            (idx1_reflex2, idx2_reflex2),
    ), (intensity) in zip(trigger_windows, stim_intensities):

        reflex1 = s2pr.reflexes.Single(waveform=emg.values[idx1_reflex1:idx2_reflex1])

        reflex2 = None
        if idx1_reflex2 is not None:
            reflex2 = s2pr.reflexes.Single(
                waveform=emg.values[idx1_reflex2:idx2_reflex2])

        double = s2pr.reflexes.Double(
            waveform=emg.values[idx1_extract:idx2_extract],
            reflex1=reflex1,
            reflex2=reflex2,
            stim_intensity=intensity,
            extract_indexes=(idx1_extract, idx2_extract),
        )

        reflexes.append(double)

    return reflexes

