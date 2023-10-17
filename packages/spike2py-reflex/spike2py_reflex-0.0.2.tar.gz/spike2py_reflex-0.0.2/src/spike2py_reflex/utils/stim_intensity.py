from spike2py_preprocess.trial_sections import find_nearest_time_index


def get_stim_intensity(info, data) -> list:
    ch = _get_stim_intensity_channel(info, data)
    intensities = list()
    for trigger in info.triggers.extract:
        intensity_value = None
        if ch is not None:
            idx = find_nearest_time_index(ch.times, trigger)
            intensity_value = round(ch.values[idx])
        intensities.append(intensity_value)
    return intensities


def _get_stim_intensity_channel(info, data):
    stim_intensity = None
    try:
        stim_intensity = getattr(data, info.channels.stim_intensity)
    except AttributeError:
        print(f'\t\tstudy: {info.study}; '
              f'trial: {info.trial}; '
              f'section: {info.section} --> no `stim_intensity` channel.')
    return stim_intensity
