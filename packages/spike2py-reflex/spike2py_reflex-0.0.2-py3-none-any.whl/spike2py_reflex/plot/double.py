import matplotlib.pyplot as plt

import spike2py_reflex as s2pr

PLOT_WIDTH_SCALING = 1
PLOT_HEIGHT_SCALING = 2


def plot_double(section):
    """Plot section double reflexes.

    Generates a plot with n columns, where n = 2 * number_muscles, and m rows,
    where m = number of stimulation intensities. For each muscle, there are
    two columns. The first column plots the data extracted for the pair of reflexes,
    and also the mean waveform. The second column plots the same extracted reflex_1
    and reflex_2, overlayed in red and blue, as well as their averaged. Also provided
    on this plot data are the windows provided from which to compute reflex outcomes.

    """

    info = section.info
    muscles, n_muscles, intensities, n_intensities = s2pr.plot.get_muscles_and_intensities(section)
    plot_width, plot_height = s2pr.plot.get_plot_width_height(n_muscles, n_intensities)
    plt.figure(figsize=(plot_width * 2 * PLOT_WIDTH_SCALING, plot_height * n_intensities * PLOT_HEIGHT_SCALING))
    _gen_figure(muscles, n_muscles, intensities, n_intensities, section, info)
    plt.tight_layout()
    s2pr.plot.save_figure(section)


def _gen_figure(muscles, n_muscles, intensities, n_intensities, section, info):
    """For each intensity of each muscle, add subplots"""
    subplot = 1
    for intensity in intensities:
        for muscle in muscles:
            # Extracted reflex
            plt.subplot(n_intensities, n_muscles * 2, subplot)
            s2pr.plot.overlay_reflexes(section, muscle, intensity)

            # reflex1 and reflex2
            plt.subplot(n_intensities, n_muscles * 2, subplot + 1)
            _overlay_double_reflexes(section, muscle, info, intensity)
            s2pr.plot.add_reflex_windows(section.info, muscle)
            s2pr.plot.set_x_lim(section.info.windows.ms_plotting.double_single_pulse)
            subplot += 2  # To skip to the plot of reflex1 and reflex2


def _overlay_double_reflexes(section, muscle, info, intensity=None):

    # Plot individual raw reflexes
    count = 0
    for reflex in section.reflexes[muscle].reflexes:
        if intensity is None:
            if reflex.reflex1.waveform is not None:
                plt.plot(section.reflexes[muscle].x_axis_singles,
                         reflex.reflex1.waveform,
                         alpha=0.3,
                         color='red')
            if reflex.reflex2.waveform is not None:
                plt.plot(section.reflexes[muscle].x_axis_singles,
                         reflex.reflex2.waveform,
                         alpha=0.3,
                         color='blue')
            count += 1
        else:
            if intensity == reflex.stim_intensity:
                if reflex.reflex1.waveform is not None:
                    plt.plot(section.reflexes[muscle].x_axis_singles,
                             reflex.reflex1.waveform,
                             alpha=0.6,
                             color='red')
                if reflex.reflex2.waveform is not None:
                    plt.plot(section.reflexes[muscle].x_axis_singles,
                             reflex.reflex2.waveform,
                             alpha=0.6,
                             color='blue')
                count += 1

    # Plot avg reflexes
    if intensity is None:
        if section.reflexes[muscle].avg_reflex1 is not None:
            for _, value in section.reflexes[muscle].avg_reflex1.items():
                plt.plot(section.reflexes[muscle].x_axis_singles,
                         value.waveform,
                         alpha=1,
                         color='red',
                         label='reflex1')
        if section.reflexes[muscle].avg_reflex2 is not None:
            for _, value in section.reflexes[muscle].avg_reflex2.items():
                plt.plot(section.reflexes[muscle].x_axis_singles,
                         value.waveform,
                         alpha=1,
                         color='blue',
                         label='reflex2')
    else:
        if section.reflexes[muscle].avg_reflex1 is not None:
            try:
                avg_reflex = section.reflexes[muscle].avg_reflex1[intensity]
                plt.plot(section.reflexes[muscle].x_axis_singles,
                         avg_reflex.waveform,
                         alpha=1,
                         color='red',
                         label='reflex1')
            except KeyError:
                pass
            try:
                avg_reflex = section.reflexes[muscle].avg_reflex2[intensity]
                plt.plot(section.reflexes[muscle].x_axis_singles,
                         avg_reflex.waveform,
                         alpha=1,
                         color='blue',
                         label='reflex2')
            except KeyError:
                pass

    plt.xlabel('time (s)')
    plt.grid()
    if intensity is None:
        plt.title((f'{info.subject}-'
                   f'{info.trial}-'
                   f'{info.section}-'
                   f'{muscle}-'
                   f'reflex1/2'), fontsize=10)
    else:
        plt.title((f'{info.subject}-'
                   f'{info.trial}-'
                   f'{info.section}-'
                   f'{muscle}-'
                   f'{intensity}mA-'
                   f'reflex1-2'), fontsize=10)
