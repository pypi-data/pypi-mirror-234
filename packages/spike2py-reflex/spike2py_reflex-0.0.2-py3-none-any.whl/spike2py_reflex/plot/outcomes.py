import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Union

import spike2py_reflex as s2pr


def plot_outcomes(section):
    """Generate raw data plots of all reflexes in a trial section

    Included are the individual traces and the mean trace, as well
    as windows indicating the region where reflex outcomes were
    calculated.
    """

    muscles = list(section.reflexes.keys())
    if section.reflexes[muscles[0]].type == s2pr.utils.SINGLE:
        s2pr.plot.single_outcomes(section)
        s2pr.plot.single_outcomes(section)
    elif section.reflexes[muscles[0]].type == s2pr.utils.TRAIN:
        s2pr.plot.train_outcomes(section)
    elif section.reflexes[muscles[0]].type == s2pr.utils.DOUBLE:
        s2pr.plot.double_outcomes(section)


N_OUTCOMES = 3
WIDTH_SCALING = 12
HEIGHT_SCALING = 4
PEAK_TO_PEAK_COLOR = 'tab:pink'
PEAK_TO_PEAK_LABEL = 'peak-to-peak (a.u.)'
AREA_COLOR = 'tab:cyan'
AREA_LABEL = 'area (a.u.)'
ONSET_COLOR = 'tab:gray'
ONSET_LABEL = 'latency (ms)'
X_AXIS_LABEL = 'stim intensities'
P2P = 'peak_to_peak'
ONSET = 'onset'
AREA = 'area'
RATIO_LABEL = 'ratio (reflex2/reflex1)'
RATIO = 'ratio'
RATIO_COLOR = 'tab:orange'
SUBPLOT = {'peak_to_peak': 1,
           'area': 2,
           'onset': 3,
           'ratio': 4}

@dataclass
class SubplotInfo:
    rows: int
    cols: int
    row_counter: int
    muscle_subplot: int
    x: int
    y: float
    y_axis_label: str
    muscle: str
    reflex_type: str
    x_ticks: list
    color: str
    outcome: str
    num_outcomes: int
    x_axis_label: str = ''
    fillstyle: str = 'none'
    alpha: float = 1.0

def single_outcomes(section):
    muscles, n_muscles, intensities, n_intensities = s2pr.plot.get_muscles_and_intensities(
        section)
    n_reflex_type = len(section.info.windows.ms_reflexes[muscles[0]].keys())

    plt.figure(figsize=(WIDTH_SCALING*n_muscles, HEIGHT_SCALING*n_reflex_type))

    rows = n_reflex_type
    cols = n_muscles*N_OUTCOMES

    for muscle_subplot, muscle in enumerate(muscles):
        for intensity in intensities:
            for reflex in section.reflexes[muscle].reflexes:
                if intensity is None:
                    for row_counter, (reflex_type, outcomes) in enumerate(reflex.outcomes.items()):
                        # peak-to-peak
                        subplot_info = SubplotInfo(rows=rows,
                                                   cols=cols,
                                                   row_counter=row_counter,
                                                   muscle_subplot=muscle_subplot,
                                                   x=0,
                                                   y=outcomes.peak_to_peak,
                                                   y_axis_label=PEAK_TO_PEAK_LABEL,
                                                   muscle=muscle,
                                                   reflex_type=reflex_type,
                                                   x_ticks=list(),
                                                   outcome=P2P,
                                                   num_outcomes=3,
                                                   color=PEAK_TO_PEAK_COLOR)
                        subplot(subplot_info)

                        # area
                        subplot_info = SubplotInfo(rows=rows,
                                                   cols=cols,
                                                   row_counter=row_counter,
                                                   muscle_subplot=muscle_subplot,
                                                   x=0,
                                                   y=outcomes.area,
                                                   y_axis_label=AREA_LABEL,
                                                   muscle=muscle,
                                                   reflex_type=reflex_type,
                                                   x_ticks=list(),
                                                   outcome=AREA,
                                                   num_outcomes=3,
                                                   color=AREA_COLOR)
                        subplot(subplot_info)

                        # onset
                        if outcomes.onset is not None:
                            subplot_info = SubplotInfo(rows=rows,
                                                       cols=cols,
                                                       row_counter=row_counter,
                                                       muscle_subplot=muscle_subplot,
                                                       x=0,
                                                       y=outcomes.area,
                                                       y_axis_label=ONSET_LABEL,
                                                       muscle=muscle,
                                                       reflex_type=reflex_type,
                                                       x_ticks=list(),
                                                       outcome=ONSET,
                                                       num_outcomes=3,
                                                       color=ONSET_COLOR)
                            subplot(subplot_info)


                if intensity == reflex.stim_intensity:
                    for row_counter, (reflex_type, outcomes) in enumerate(
                            reflex.outcomes.items()):
                        # peak-to-peak
                        subplot_info = SubplotInfo(rows=rows,
                                                   cols=cols,
                                                   row_counter=row_counter,
                                                   muscle_subplot=muscle_subplot,
                                                   x=intensity,
                                                   y=outcomes.peak_to_peak,
                                                   y_axis_label=PEAK_TO_PEAK_LABEL,
                                                   muscle=muscle,
                                                   reflex_type=reflex_type,
                                                   x_ticks=intensities,
                                                   x_axis_label=X_AXIS_LABEL,
                                                   outcome=P2P,
                                                   num_outcomes=3,
                                                   color=PEAK_TO_PEAK_COLOR)
                        subplot(subplot_info)

                        # area
                        subplot_info = SubplotInfo(rows=rows,
                                                   cols=cols,
                                                   row_counter=row_counter,
                                                   muscle_subplot=muscle_subplot,
                                                   x=intensity,
                                                   y=outcomes.area,
                                                   y_axis_label=AREA_LABEL,
                                                   muscle=muscle,
                                                   reflex_type=reflex_type,
                                                   x_ticks=intensities,
                                                   x_axis_label=X_AXIS_LABEL,
                                                   outcome=AREA,
                                                   num_outcomes=3,
                                                   color=AREA_COLOR)
                        subplot(subplot_info)

                        # onset
                        if outcomes.onset is not None:
                            subplot_info = SubplotInfo(rows=rows,
                                                       cols=cols,
                                                       row_counter=row_counter,
                                                       muscle_subplot=muscle_subplot,
                                                       x=intensity,
                                                       y=outcomes.onset,
                                                       y_axis_label=ONSET_LABEL,
                                                       muscle=muscle,
                                                       reflex_type=reflex_type,
                                                       x_ticks=intensities,
                                                       x_axis_label=X_AXIS_LABEL,
                                                       outcome=ONSET,
                                                       num_outcomes=3,
                                                       color=ONSET_COLOR)
                            subplot(subplot_info)
    save_figure(section)


def subplot(sp):
    subplot_id = (sp.row_counter * sp.cols) + (sp.muscle_subplot * sp.num_outcomes) + SUBPLOT[sp.outcome]
    plt.subplot(sp.rows, sp.cols, subplot_id)
    plt.plot(sp.x, sp.y, 'o', fillstyle=sp.fillstyle, color=sp.color,
             alpha=sp.alpha)
    plt.ylabel(sp.y_axis_label)
    plt.title(f'{sp.muscle}-{sp.reflex_type}')
    plt.xticks(ticks=sp.x_ticks)
    plt.xlabel(sp.x_axis_label)



def save_figure(section):
    plt.suptitle(f'{section.info.trial}_{section.info.section}_outcomes')
    plt.tight_layout()
    figure_name = f'{section.info.trial}_{section.info.section}_outcomes.pdf'
    path = section.info.study_path / section.info.subject / 'figures' / 'outcomes'
    if not path.exists():
        path.mkdir()
    plt.savefig(path/figure_name)


def train_outcomes(section):
    muscles, n_muscles, intensities, n_intensities = s2pr.plot.get_muscles_and_intensities(
        section)
    n_reflex_type = len(section.info.windows.ms_reflexes[muscles[0]].keys())

    plt.figure(figsize=(WIDTH_SCALING*0.75*n_muscles, HEIGHT_SCALING*n_reflex_type))

    rows = n_reflex_type
    cols = n_muscles*(N_OUTCOMES-1)

    for muscle_subplot, muscle in enumerate(muscles):
        for intensity in intensities:
            for reflex in section.reflexes[muscle].reflexes:
                if intensity is None:
                    for row_counter, (reflex_type, outcomes) in enumerate(reflex.outcomes.items()):
                        # peak-to-peak
                        subplot_info = SubplotInfo(rows=rows,
                                                   cols=cols,
                                                   row_counter=row_counter,
                                                   muscle_subplot=muscle_subplot,
                                                   x=0,
                                                   y=outcomes.peak_to_peak,
                                                   y_axis_label=PEAK_TO_PEAK_LABEL,
                                                   muscle=muscle,
                                                   reflex_type=reflex_type,
                                                   x_ticks=list(),
                                                   outcome=P2P,
                                                   num_outcomes=2,
                                                   color=PEAK_TO_PEAK_COLOR)
                        subplot(subplot_info)

                        # area
                        subplot_info = SubplotInfo(rows=rows,
                                                   cols=cols,
                                                   row_counter=row_counter,
                                                   muscle_subplot=muscle_subplot,
                                                   x=0,
                                                   y=outcomes.area,
                                                   y_axis_label=AREA_LABEL,
                                                   muscle=muscle,
                                                   reflex_type=reflex_type,
                                                   x_ticks=list(),
                                                   outcome=AREA,
                                                   num_outcomes=2,
                                                   color=AREA_COLOR)
                        subplot(subplot_info)

                if intensity == reflex.stim_intensity:
                    for row_counter, (reflex_type, outcomes) in enumerate(
                            reflex.outcomes.items()):
                        # peak-to-peak
                        subplot_info = SubplotInfo(rows=rows,
                                                   cols=cols,
                                                   row_counter=row_counter,
                                                   muscle_subplot=muscle_subplot,
                                                   x=intensity,
                                                   y=outcomes.peak_to_peak,
                                                   y_axis_label=PEAK_TO_PEAK_LABEL,
                                                   muscle=muscle,
                                                   reflex_type=reflex_type,
                                                   x_ticks=intensities,
                                                   x_axis_label=X_AXIS_LABEL,
                                                   outcome=P2P,
                                                   num_outcomes=2,
                                                   color=PEAK_TO_PEAK_COLOR)
                        subplot(subplot_info)

                        # area
                        subplot_info = SubplotInfo(rows=rows,
                                                   cols=cols,
                                                   row_counter=row_counter,
                                                   muscle_subplot=muscle_subplot,
                                                   x=intensity,
                                                   y=outcomes.area,
                                                   y_axis_label=AREA_LABEL,
                                                   muscle=muscle,
                                                   reflex_type=reflex_type,
                                                   x_ticks=intensities,
                                                   x_axis_label=X_AXIS_LABEL,
                                                   outcome=AREA,
                                                   num_outcomes=2,
                                                   color=AREA_COLOR)
                        subplot(subplot_info)
    save_figure(section)


def double_outcomes(section):
    muscles, n_muscles, intensities, n_intensities = s2pr.plot.get_muscles_and_intensities(
        section)
    n_reflex_type = len(section.info.windows.ms_reflexes[muscles[0]].keys())

    plt.figure(figsize=(WIDTH_SCALING*n_muscles*1.25, HEIGHT_SCALING*n_reflex_type))

    rows = n_reflex_type
    cols = n_muscles*(N_OUTCOMES+1)

    for muscle_subplot, muscle in enumerate(muscles):
        for intensity in intensities:
            for reflex in section.reflexes[muscle].reflexes:
                if intensity is None:
                    # Reflex 1
                    for row_counter, (reflex_type, outcomes) in enumerate(reflex.reflex1.outcomes.items()):
                        # peak-to-peak
                        subplot_info = SubplotInfo(rows=rows,
                                                   cols=cols,
                                                   row_counter=row_counter,
                                                   muscle_subplot=muscle_subplot,
                                                   x=0,
                                                   y=outcomes.peak_to_peak,
                                                   y_axis_label=PEAK_TO_PEAK_LABEL,
                                                   muscle=muscle,
                                                   reflex_type=reflex_type,
                                                   x_ticks=list(),
                                                   outcome=P2P,
                                                   num_outcomes=4,
                                                   color=PEAK_TO_PEAK_COLOR)
                        subplot(subplot_info)

                        # area
                        subplot_info = SubplotInfo(rows=rows,
                                                   cols=cols,
                                                   row_counter=row_counter,
                                                   muscle_subplot=muscle_subplot,
                                                   x=0,
                                                   y=outcomes.area,
                                                   y_axis_label=AREA_LABEL,
                                                   muscle=muscle,
                                                   reflex_type=reflex_type,
                                                   x_ticks=list(),
                                                   outcome=AREA,
                                                   num_outcomes=4,
                                                   color=AREA_COLOR)
                        subplot(subplot_info)

                        # onset
                        if outcomes.onset is not None:
                            subplot_info = SubplotInfo(rows=rows,
                                                       cols=cols,
                                                       row_counter=row_counter,
                                                       muscle_subplot=muscle_subplot,
                                                       x=0,
                                                       y=outcomes.onset,
                                                       y_axis_label=ONSET_LABEL,
                                                       muscle=muscle,
                                                       reflex_type=reflex_type,
                                                       x_ticks=list(),
                                                       outcome=ONSET,
                                                       num_outcomes=3,
                                                       color=ONSET_COLOR)
                            subplot(subplot_info)

                    # Reflex 2

                    for row_counter, (reflex_type, outcomes) in enumerate(
                            reflex.reflex2.outcomes.items()):
                        try:  # In case there is not reflex 2
                            # peak-to-peak
                            subplot_info = SubplotInfo(rows=rows,
                                                       cols=cols,
                                                       row_counter=row_counter,
                                                       muscle_subplot=muscle_subplot,
                                                       x=1,
                                                       y=outcomes.peak_to_peak,
                                                       y_axis_label=PEAK_TO_PEAK_LABEL,
                                                       muscle=muscle,
                                                       reflex_type=reflex_type,
                                                       x_ticks=list(),
                                                       outcome=P2P,
                                                       num_outcomes=4,
                                                       color=PEAK_TO_PEAK_COLOR,
                                                       fillstyle='full',
                                                       alpha=0.3)
                            subplot(subplot_info)

                            # area
                            subplot_info = SubplotInfo(rows=rows,
                                                       cols=cols,
                                                       row_counter=row_counter,
                                                       muscle_subplot=muscle_subplot,
                                                       x=1,
                                                       y=outcomes.area,
                                                       y_axis_label=AREA_LABEL,
                                                       muscle=muscle,
                                                       reflex_type=reflex_type,
                                                       x_ticks=list(),
                                                       outcome=AREA,
                                                       num_outcomes=4,
                                                       color=AREA_COLOR,
                                                       fillstyle='full',
                                                       alpha=0.3
                                                       )
                            subplot(subplot_info)

                            # onset
                            if outcomes.onset is not None:
                                subplot_info = SubplotInfo(rows=rows,
                                                           cols=cols,
                                                           row_counter=row_counter,
                                                           muscle_subplot=muscle_subplot,
                                                           x=1,
                                                           y=outcomes.onset,
                                                           y_axis_label=ONSET_LABEL,
                                                           muscle=muscle,
                                                           reflex_type=reflex_type,
                                                           x_ticks=list(),
                                                           outcome=ONSET,
                                                           num_outcomes=4,
                                                           color=ONSET_COLOR,
                                                           fillstyle='full',
                                                           alpha=0.3
                                                           )
                                subplot(subplot_info)
                        except:
                            pass
                    # Ratio
                    try:
                        for row_counter, (reflex_type, ratio) in enumerate(
                                reflex.ratio.items()):
                            # ratio
                            subplot_info = SubplotInfo(rows=rows,
                                                       cols=cols,
                                                       row_counter=row_counter,
                                                       muscle_subplot=muscle_subplot,
                                                       x=0,
                                                       y=ratio,
                                                       y_axis_label=RATIO_LABEL,
                                                       muscle=muscle,
                                                       reflex_type=reflex_type,
                                                       x_ticks=list(),
                                                       outcome=RATIO,
                                                       num_outcomes=4,
                                                       color=RATIO_COLOR)
                            subplot(subplot_info)
                    except Exception as e:
                        print(e)

                if intensity == reflex.stim_intensity:
                    # Reflex 1
                    for row_counter, (reflex_type, outcomes) in enumerate(
                            reflex.reflex1.outcomes.items()):
                        # peak-to-peak
                        subplot_info = SubplotInfo(rows=rows,
                                                   cols=cols,
                                                   row_counter=row_counter,
                                                   muscle_subplot=muscle_subplot,
                                                   x=intensity,
                                                   y=outcomes.peak_to_peak,
                                                   y_axis_label=PEAK_TO_PEAK_LABEL,
                                                   muscle=muscle,
                                                   reflex_type=reflex_type,
                                                   x_ticks=intensities,
                                                   outcome=P2P,
                                                   num_outcomes=4,
                                                   x_axis_label=X_AXIS_LABEL,
                                                   color=PEAK_TO_PEAK_COLOR)
                        subplot(subplot_info)

                        # area
                        subplot_info = SubplotInfo(rows=rows,
                                                   cols=cols,
                                                   row_counter=row_counter,
                                                   muscle_subplot=muscle_subplot,
                                                   x=intensity,
                                                   y=outcomes.area,
                                                   y_axis_label=AREA_LABEL,
                                                   muscle=muscle,
                                                   reflex_type=reflex_type,
                                                   x_ticks=intensities,
                                                   outcome=AREA,
                                                   num_outcomes=4,
                                                   x_axis_label=X_AXIS_LABEL,
                                                   color=AREA_COLOR)
                        subplot(subplot_info)

                        # onset
                        if outcomes.onset is not None:
                            subplot_info = SubplotInfo(rows=rows,
                                                       cols=cols,
                                                       row_counter=row_counter,
                                                       muscle_subplot=muscle_subplot,
                                                       x=intensity,
                                                       y=outcomes.onset,
                                                       y_axis_label=ONSET_LABEL,
                                                       muscle=muscle,
                                                       reflex_type=reflex_type,
                                                       x_ticks=intensities,
                                                       outcome=ONSET,
                                                       num_outcomes=4,
                                                       x_axis_label=X_AXIS_LABEL,
                                                       color=ONSET_COLOR)
                            subplot(subplot_info)
                    # Reflex 2

                    for row_counter, (reflex_type, outcomes) in enumerate(
                            reflex.reflex2.outcomes.items()):
                        try:
                            # peak-to-peak
                            subplot_info = SubplotInfo(rows=rows,
                                                       cols=cols,
                                                       row_counter=row_counter,
                                                       muscle_subplot=muscle_subplot,
                                                       x=intensity + 1,
                                                       y=outcomes.peak_to_peak,
                                                       y_axis_label=PEAK_TO_PEAK_LABEL,
                                                       muscle=muscle,
                                                       reflex_type=reflex_type,
                                                       x_ticks=intensities,
                                                       outcome=P2P,
                                                       num_outcomes=4,
                                                       x_axis_label=X_AXIS_LABEL,
                                                       color=PEAK_TO_PEAK_COLOR,
                                                       fillstyle='full',
                                                       alpha=0.3
                                                       )
                            subplot(subplot_info)

                            # area
                            subplot_info = SubplotInfo(rows=rows,
                                                       cols=cols,
                                                       row_counter=row_counter,
                                                       muscle_subplot=muscle_subplot,
                                                       x=intensity + 1,
                                                       y=outcomes.area,
                                                       y_axis_label=AREA_LABEL,
                                                       muscle=muscle,
                                                       reflex_type=reflex_type,
                                                       x_ticks=intensities,
                                                       outcome=AREA,
                                                       num_outcomes=4,
                                                       x_axis_label=X_AXIS_LABEL,
                                                       color=AREA_COLOR,
                                                       fillstyle='full',
                                                       alpha=0.3
                                                       )
                            subplot(subplot_info)

                            # onset
                            if outcomes.onset is not None:
                                subplot_info = SubplotInfo(rows=rows,
                                                           cols=cols,
                                                           row_counter=row_counter,
                                                           muscle_subplot=muscle_subplot,
                                                           x=intensity + 1,
                                                           y=outcomes.onset,
                                                           y_axis_label=ONSET_LABEL,
                                                           muscle=muscle,
                                                           reflex_type=reflex_type,
                                                           x_ticks=intensities,
                                                           outcome=ONSET,
                                                           num_outcomes=4,
                                                           x_axis_label=X_AXIS_LABEL,
                                                           color=ONSET_COLOR,
                                                           fillstyle='full',
                                                           alpha=0.3
                                                           )
                                subplot(subplot_info)

                            # Ratio
                            for row_counter, (reflex_type, ratio) in enumerate(
                                    reflex.ratio.items()):
                                # ratio
                                subplot_info = SubplotInfo(rows=rows,
                                                           cols=cols,
                                                           row_counter=row_counter,
                                                           muscle_subplot=muscle_subplot,
                                                           x=intensity,
                                                           y=ratio,
                                                           y_axis_label=RATIO_LABEL,
                                                           muscle=muscle,
                                                           reflex_type=reflex_type,
                                                           x_ticks=intensities,
                                                           outcome=RATIO,
                                                           num_outcomes=4,
                                                           x_axis_label=X_AXIS_LABEL,
                                                           color=RATIO_COLOR)
                                subplot(subplot_info)
                        except Exception as e:
                            print(e)

    save_figure(section)

