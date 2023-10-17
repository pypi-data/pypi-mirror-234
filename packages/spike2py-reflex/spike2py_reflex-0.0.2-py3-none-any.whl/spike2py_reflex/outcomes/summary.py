import spike2py_reflex as s2pr


LINE = 80 * '-'
TRIGGER = 'trig'
MUSCLE = 'muscle'
REFLEX = 'reflex'
STIM = 'stim'
TIME1 = 'time1'
TIME2 = 'time2'
P2P = 'p2p'
AREA = 'area'
ONSET = 'onset'


def summary(section):

    muscles = list(section.reflexes.keys())
    if section.reflexes[muscles[0]].type == s2pr.utils.SINGLE:
        _single_summary(section)
    elif section.reflexes[muscles[0]].type == s2pr.utils.TRAIN:
        _train_summary(section)
    elif section.reflexes[muscles[0]].type == s2pr.utils.DOUBLE:
        _double_summary(section)


def _single_summary(section):
    summary = list()
    line = f'{section.info.trial.upper()} | {section.info.section.upper()}'
    summary = _add_header(summary, line)

    muscles, _, intensities, _ = s2pr.plot.get_muscles_and_intensities(section)
    section_name = section.info.section
    reflex_types = list(section.info.windows.ms_reflexes[muscles[0]][section_name].keys())

    line = (f'{TRIGGER:<5s}{MUSCLE:<8s}{REFLEX:<10s}{STIM:<8s}{TIME1:<10s}'
            f'{TIME2:<10s}{P2P:^8s}  {AREA:^8s}  {ONSET:^8s}')

    summary = _add_header(summary, line)

    for muscle in muscles:
        for reflex_type in reflex_types:
            for i, reflex in enumerate(section.reflexes[muscle].reflexes):
                summary = _add_single_reflex_outcomes(i, reflex, reflex_type, muscle, summary)
            summary.append(LINE)
    summary = _add_mean_single_reflex_outcomes(summary, section, muscles, intensities, reflex_types)
    _save_summary(summary, section)


def _add_header( summary, line):
    summary.append(LINE)
    summary.append(line)
    summary.append(LINE)
    return summary


def _add_single_reflex_outcomes(i, reflex, reflex_type, muscle, summary):
    if reflex.outcomes[reflex_type].onset is None:
        line = (f'{i:<5d}{muscle:<8s}{reflex_type:<10s}{reflex.stim_intensity:<8d}'
                f'{reflex.extract_indexes[0]:<10.2f}{reflex.extract_indexes[1]:<10.2f}'
                f'{reflex.outcomes[reflex_type].peak_to_peak:>8.4f}'
                f'  {reflex.outcomes[reflex_type].area:>8.4f}')
    else:
        line = (f'{i:<5d}{muscle:<8s}{reflex_type:<10s}{reflex.stim_intensity:<8d}'
                f'{reflex.extract_indexes[0]:<10.2f}{reflex.extract_indexes[1]:<10.2f}'
                f'{reflex.outcomes[reflex_type].peak_to_peak:>8.4f}'
                f'  {reflex.outcomes[reflex_type].area:>8.4f}'
                f'  {reflex.outcomes[reflex_type].onset:>8.4f}')

    summary.append(line)
    return summary


def _add_mean_single_reflex_outcomes(summary, section, muscles, intensities, reflex_types):
    if intensities is None:
        intensities = [0]
    i = ''
    summary.append('MEAN VALUES')
    summary.append(LINE)
    for muscle in muscles:
        for reflex_type in reflex_types:
            for intensity in intensities:
                p2p = section.reflexes[muscle].mean_outcomes[reflex_type][intensity]['outcomes'].peak_to_peak
                area = section.reflexes[muscle].mean_outcomes[reflex_type][intensity]['outcomes'].area
                onset = section.reflexes[muscle].mean_outcomes[reflex_type][intensity]['outcomes'].onset
                if onset is None:
                    line = (f'{i:<5s}{muscle:<8s}{reflex_type:<10s}{intensity:<28d}'
                            f'{p2p:>8.4f}'
                            f'  {area:>8.4f}')
                else:

                    line = (f'{i:<5s}{muscle:<8s}{reflex_type:<10s}{intensity:<28d}'
                            f'{p2p:>8.4f}'
                            f'  {area:>8.4f}'
                            f'  {onset:>8.4f}')
                summary.append(line)

                p2p_missing = section.reflexes[muscle].mean_outcomes[reflex_type][intensity]['missing_outcomes'].peak_to_peak
                p2p_present = section.reflexes[muscle].mean_outcomes[reflex_type][intensity]['present_outcomes'].peak_to_peak
                p2p_val = str(p2p_present) + '/' + str(p2p_present + p2p_missing)

                area_missing = section.reflexes[muscle].mean_outcomes[reflex_type][intensity]['missing_outcomes'].area
                area_present = section.reflexes[muscle].mean_outcomes[reflex_type][intensity]['present_outcomes'].area
                area_val = str(area_present) + '/' + str(area_present + area_missing)

                if onset is None:
                    onset_val = ""
                else:
                    onset_missing = section.reflexes[muscle].mean_outcomes[reflex_type][intensity]['missing_outcomes'].onset
                    onset_present = section.reflexes[muscle].mean_outcomes[reflex_type][intensity]['present_outcomes'].onset
                    onset_val = str(onset_present) + '/' + str(onset_present + onset_missing)
                line = (f'{p2p_val:>56s}'
                        f'  {area_val:>8s}'
                        f'  {onset_val:>8s}')
                summary.append(line)
                summary.append(LINE)
    return summary


def _save_summary(summary, section):
    file_name = f'{section.info.trial}_{section.info.section}_summary.txt'
    path = section.info.study_path / section.info.subject / 'numerical_outcomes' / 'summary'
    if not path.exists():
        path.mkdir(parents=True)
    with open(path / file_name, 'w') as f:
        for line in summary:
            f.write(line + '\n')


def _double_summary(section):
    summary = list()
    line = f'{section.info.trial.upper()} | {section.info.section.upper()}'
    summary = _add_header(summary, line)

    muscles, _, intensities, _ = s2pr.plot.get_muscles_and_intensities(section)
    section_name = section.info.section
    reflex_types = list(section.info.windows.ms_reflexes[muscles[0]][section_name].keys())

    line = (f'{TRIGGER:<5s}{MUSCLE:<8s}{REFLEX:<10s}{STIM:<8s}{TIME1:<10s}'
            f'{TIME2:<10s}{P2P:^8s}  {AREA:^8s}  {ONSET:^8s}')

    summary = _add_header(summary, line)

    for muscle in muscles:
        for reflex_type in reflex_types:
            for i, reflex in enumerate(section.reflexes[muscle].reflexes):
                summary = _add_double_reflex_outcomes(i, reflex, reflex_type, muscle, summary)
            summary.append(LINE)
    summary = _add_mean_double_reflex_outcomes(summary, section, muscles, intensities, reflex_types)
    _save_summary(summary, section)


def _add_double_reflex_outcomes(i, reflex, reflex_type, muscle, summary):
    i1 = str(i) + '-1'
    i2 = str(i) + '-2'

    if reflex.reflex1.outcomes[reflex_type].onset is None:
        line1 = (f'{i1:<5s}{muscle:<8s}{reflex_type:<10s}{reflex.stim_intensity:<8d}'
                f'{reflex.extract_indexes[0]:<10.2f}{reflex.extract_indexes[1]:<10.2f}'
                f'{reflex.reflex1.outcomes[reflex_type].peak_to_peak:>8.4f}'
                f'  {reflex.reflex1.outcomes[reflex_type].area:>8.4f}')
    else:
        line1 = (f'{i1:<5s}{muscle:<8s}{reflex_type:<10s}{reflex.stim_intensity:<8d}'
                f'{reflex.extract_indexes[0]:<10.2f}{reflex.extract_indexes[1]:<10.2f}'
                f'{reflex.reflex1.outcomes[reflex_type].peak_to_peak:>8.4f}'
                f'  {reflex.reflex1.outcomes[reflex_type].area:>8.4f}'
                f'  {reflex.reflex1.outcomes[reflex_type].onset:>8.4f}')
    summary.append(line1)
    if reflex.reflex2.outcomes[reflex_type].onset is None:
        line2 = (f'{i2:<51s}'
                f'{reflex.reflex2.outcomes[reflex_type].peak_to_peak:>8.4f}'
                f'  {reflex.reflex2.outcomes[reflex_type].area:>8.4f}')
    else:
        line2 = (f'{i2:<51s}'
                 f'{reflex.reflex2.outcomes[reflex_type].peak_to_peak:>8.4f}'
                 f'  {reflex.reflex2.outcomes[reflex_type].area:>8.4f}'
                 f'  {reflex.reflex2.outcomes[reflex_type].onset:>8.4f}')
    summary.append(line2)
    return summary


def _add_mean_double_reflex_outcomes(summary, section, muscles, intensities, reflex_types):
    if intensities is None:
        intensities = [0]
    i1 = '1'
    i2 = '2'
    summary.append('MEAN VALUES')
    summary.append(LINE)
    for muscle in muscles:
        for reflex_type in reflex_types:
            for intensity in intensities:
                p2p1 = section.reflexes[muscle].mean_outcomes_reflex1[reflex_type][intensity]['outcomes'].peak_to_peak
                area1 = section.reflexes[muscle].mean_outcomes_reflex1[reflex_type][intensity]['outcomes'].area
                onset1 = section.reflexes[muscle].mean_outcomes_reflex1[reflex_type][intensity]['outcomes'].onset
                p2p2 = section.reflexes[muscle].mean_outcomes_reflex2[reflex_type][intensity]['outcomes'].peak_to_peak
                area2 = section.reflexes[muscle].mean_outcomes_reflex2[reflex_type][intensity]['outcomes'].area
                onset2 = section.reflexes[muscle].mean_outcomes_reflex2[reflex_type][intensity]['outcomes'].onset

                p2p_missing1 = section.reflexes[muscle].mean_outcomes_reflex1[reflex_type][intensity]['missing_outcomes'].peak_to_peak
                p2p_present1 = section.reflexes[muscle].mean_outcomes_reflex1[reflex_type][intensity]['present_outcomes'].peak_to_peak
                p2p_val1 = str(p2p_present1) + '/' + str(p2p_present1 + p2p_missing1)

                area_missing1 = section.reflexes[muscle].mean_outcomes_reflex1[reflex_type][intensity]['missing_outcomes'].area
                area_present1 = section.reflexes[muscle].mean_outcomes_reflex1[reflex_type][intensity]['present_outcomes'].area
                area_val1 = str(area_present1) + '/' + str(area_present1 + area_missing1)

                p2p_missing2 = section.reflexes[muscle].mean_outcomes_reflex1[reflex_type][intensity]['missing_outcomes'].peak_to_peak
                p2p_present2 = section.reflexes[muscle].mean_outcomes_reflex1[reflex_type][intensity]['present_outcomes'].peak_to_peak
                p2p_val2 = str(p2p_present2) + '/' + str(p2p_present2 + p2p_missing2)

                area_missing2 = section.reflexes[muscle].mean_outcomes_reflex1[reflex_type][intensity]['missing_outcomes'].area
                area_present2 = section.reflexes[muscle].mean_outcomes_reflex1[reflex_type][intensity]['present_outcomes'].area
                area_val2 = str(area_present2) + '/' + str(area_present2 + area_missing2)


                if onset1 is None:
                    line1 = (f'{i1:<5s}{muscle:<8s}{reflex_type:<10s}{intensity:<28d}'
                            f'{p2p1:>8.4f}'
                            f'  {area1:>8.4f}')
                    onset_val1 = ""
                else:
                    line1 = (f'{i1:<5s}{muscle:<8s}{reflex_type:<10s}{intensity:<28d}'
                            f'{p2p1:>8.4f}'
                            f'  {area1:>8.4f}'
                            f'  {onset1:>8.4f}')
                    onset_missing1 = section.reflexes[muscle].mean_outcomes_reflex1[reflex_type][intensity]['missing_outcomes'].onset
                    onset_present1 = section.reflexes[muscle].mean_outcomes_reflex1[reflex_type][intensity]['present_outcomes'].onset
                    onset_val1 = str(onset_present1) + '/' + str(onset_present1 + onset_missing1)

                line11 = (f'{p2p_val1:>56s}'
                          f'  {area_val1:>8s}'
                          f'  {onset_val1:>8s}')

                summary.append(line1)
                summary.append(line11)


                if onset2 is None:
                    line2 = (f'{i2:<51s}'
                            f'{p2p2:>8.4f}'
                            f'  {area2:>8.4f}')
                    onset_val2 = ""
                else:
                    line2 = (f'{i2:<51s}'
                            f'{p2p2:>8.4f}'
                            f'  {area2:>8.4f}'
                            f'  {onset2:>8.4f}')
                    onset_missing2 = section.reflexes[muscle].mean_outcomes_reflex2[reflex_type][intensity]['missing_outcomes'].onset
                    onset_present2 = section.reflexes[muscle].mean_outcomes_reflex2[reflex_type][intensity]['present_outcomes'].onset
                    onset_val2 = str(onset_present2) + '/' + str(onset_present2 + onset_missing2)

                line22 = (f'{p2p_val2:>56s}'
                          f'  {area_val2:>8s}'
                          f'  {onset_val2:>8s}')
                summary.append(line2)
                summary.append(line22)

    return summary


def _train_summary(section):
    summary = list()
    line = f'{section.info.trial.upper()} | {section.info.section.upper()}'
    summary = _add_header(summary, line)

    muscles, _, intensities, _ = s2pr.plot.get_muscles_and_intensities(section)
    section_name = section.info.section
    reflex_types = list(section.info.windows.ms_reflexes[muscles[0]][section_name].keys())

    line = (f'{TRIGGER:<5s}{MUSCLE:<8s}{REFLEX:<10s}{STIM:<8s}{TIME1:<10s}'
            f'{TIME2:<10s}{P2P:^8s}  {AREA:^8s}')

    summary = _add_header(summary, line)

    for muscle in muscles:
        for reflex_type in reflex_types:
            for i, reflex in enumerate(section.reflexes[muscle].reflexes):
                summary = _add_train_reflex_outcomes(i, reflex, reflex_type, muscle, summary)
            summary.append(LINE)
    summary = _add_mean_train_reflex_outcomes(summary, section, muscles, intensities, reflex_types)
    _save_summary(summary, section)


def _add_train_reflex_outcomes(i, reflex, reflex_type, muscle, summary):
    line = (f'{i:<5d}{muscle:<8s}{reflex_type:<10s}{reflex.stim_intensity:<8d}'
            f'{reflex.extract_indexes[0]:<10.2f}{reflex.extract_indexes[1]:<10.2f}'
            f'{reflex.outcomes[reflex_type].peak_to_peak:>8.4f}'
            f'  {reflex.outcomes[reflex_type].area:>8.4f}')
    summary.append(line)
    return summary


def _add_mean_train_reflex_outcomes(summary, section, muscles, intensities, reflex_types):
    if intensities is None:
        intensities = [0]
    i = ''
    summary.append('MEAN VALUES')
    summary.append(LINE)
    for muscle in muscles:
        for reflex_type in reflex_types:
            for intensity in intensities:
                p2p = section.reflexes[muscle].mean_outcomes[reflex_type][intensity]['outcomes'].peak_to_peak
                area = section.reflexes[muscle].mean_outcomes[reflex_type][intensity]['outcomes'].area
                line = (f'{i:<5s}{muscle:<8s}{reflex_type:<10s}{intensity:<28d}'
                        f'{p2p:>8.4f}'
                        f'  {area:>8.4f}')

                summary.append(line)

                p2p_missing = section.reflexes[muscle].mean_outcomes[reflex_type][intensity]['missing_outcomes'].peak_to_peak
                p2p_present = section.reflexes[muscle].mean_outcomes[reflex_type][intensity]['present_outcomes'].peak_to_peak
                p2p_val = str(p2p_present) + '/' + str(p2p_present + p2p_missing)

                area_missing = section.reflexes[muscle].mean_outcomes[reflex_type][intensity]['missing_outcomes'].area
                area_present = section.reflexes[muscle].mean_outcomes[reflex_type][intensity]['present_outcomes'].area
                area_val = str(area_present) + '/' + str(area_present + area_missing)

                line = (f'{p2p_val:>59s}'
                        f'  {area_val:>7s}')

                summary.append(line)
                summary.append(LINE)
    return summary
