import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy

import spike2py_reflex as s2pr

PLOT_WIDTH_SCALING = 4
PLOT_HEIGHT_SCALING = 2
REFLEX_COLORS = ['m', 'g', 'k']


def plot_single(section):
    """Plot section single reflexes.

    Generates a plot with n columns, where n = 2 * number_muscles, and m rows,
    where m = number of stimulation intensities. For each muscle, there are
    two columns. The first column plots the data extracted for each reflex,
    and also the avg reflex. The second column plots the same data, but with
    the `plot` window applied to provide a better view of the extracted reflexes.
    Also provided on this plot data are the windows provided from which to compute
    reflex outcomes.

    """
    muscles, n_muscles, intensities, n_intensities = get_muscles_and_intensities(section)
    plot_width, plot_height = get_plot_width_height(n_muscles, n_intensities)

    # Additional scaling to figure size added based on appearance
    plt.figure(figsize=(plot_width * 2, 2 * plot_height * n_intensities))
    _gen_figure(muscles, n_muscles, intensities, n_intensities, section)
    plt.tight_layout()
    save_figure(section)


def get_muscles_and_intensities(section):
    muscles = list(section.reflexes.keys())
    n_muscles = len(muscles)
    intensities = list(section.reflexes[muscles[0]].avg_waveform.keys())
    n_intensities = 1
    if intensities is not None:
        n_intensities = len(intensities)
    return muscles, n_muscles, intensities, n_intensities


def get_plot_width_height(n_muscles, n_intensities):
    plot_width = PLOT_WIDTH_SCALING * n_muscles
    plot_height = PLOT_HEIGHT_SCALING * n_intensities
    return plot_width, plot_height


def _gen_figure(muscles, n_muscles, intensities, n_intensities, section):
    """For each intensity of each muscle, add subplots"""
    subplot = 1
    for intensity in intensities:
        for muscle in muscles:
            # Extracted reflex
            plt.subplot(n_intensities, n_muscles * 2, subplot)
            overlay_reflexes(section, muscle, intensity)

            # Same reflex but with adjusted x-axis and reflex windows highlighted
            plt.subplot(n_intensities, n_muscles * 2, subplot + 1)
            overlay_reflexes(section, muscle, intensity, legend=False)
            set_x_lim(section.info.windows.ms_plotting.single)
            add_reflex_windows(section.info, muscle)
            subplot += 2  # Iterate by 2 to skip over zoomed version of previous muscle


def overlay_reflexes(section, muscle, intensity, legend=True):
    """Plot overlayed raw reflexes and their average

    `intensity` is a numerical value or None.
    `legend` can be turned off for subplots where we want to show reflex windows.

    """
    # First, plot the overlayed raw reflexes
    count = 0
    for reflex in section.reflexes[muscle].reflexes:
        if intensity is None:
            if legend:
                plt.plot(section.reflexes[muscle].x_axis_extract,
                         reflex.waveform,
                         label=(f'{reflex.extract_indexes[0]:6.1f}-'
                                f'{reflex.extract_indexes[1]:6.1f}'),
                         alpha=0.3)
            else:
                plt.plot(section.reflexes[muscle].x_axis_extract,
                         reflex.waveform,
                         alpha=0.3)
            count += 1
        else:
            if intensity == reflex.stim_intensity:
                if legend:
                    plt.plot(section.reflexes[muscle].x_axis_extract,
                             reflex.waveform,
                             label=(f'{reflex.extract_indexes[0]:6.1f}-'
                                    f'{reflex.extract_indexes[1]:6.1f}'),
                             alpha=0.3)
                    count += 1
                else:
                    plt.plot(section.reflexes[muscle].x_axis_extract,
                             reflex.waveform,
                             alpha=0.3)
                    count += 1
    # Second, plot the average of the raw reflexes
    if intensity is None:
        if section.reflexes[muscle].avg_waveform is not None:
            for _, value in section.reflexes[muscle].avg_waveform.items():
                # If `single` processed, value will be a `Single` instance
                # If `train` processed, value will be ndarray
                if type(value) == numpy.ndarray:
                    plt.plot(section.reflexes[muscle].x_axis_extract,
                             value,
                             alpha=1,
                             color='black')
                else:
                    plt.plot(section.reflexes[muscle].x_axis_extract,
                             value.waveform,
                             alpha=1,
                             color='black')

    # If there are reflexes collected at different stimulation intensities
    else:
        if section.reflexes[muscle].avg_waveform is not None:
            try:
                avg_reflex = section.reflexes[muscle].avg_waveform[intensity]
                if type(avg_reflex) == numpy.ndarray:
                    plt.plot(section.reflexes[muscle].x_axis_extract,
                             avg_reflex,
                             alpha=1,
                             color='black')

                else:
                    plt.plot(section.reflexes[muscle].x_axis_extract,
                             avg_reflex.waveform,
                             alpha=1,
                             color='black')
            except KeyError:
                pass

    plt.xlabel('time (s)')
    plt.grid()
    if intensity is None:
        plt.title((f'{section.info.subject}-'
                   f'{section.info.trial}-'
                   f'{section.info.section}-'
                   f'{muscle}'), fontsize=10)
    else:
        plt.title((f'{section.info.subject}-'
                   f'{section.info.trial}-'
                   f'{section.info.section}-'
                   f'{muscle}-'
                   f'{intensity}mA'), fontsize=10)
    if (count < 11) and legend:
        plt.legend(fontsize='x-small')


def add_reflex_windows(info, muscle):
    """Add transparent colored box indicating window for reflex outcome calculations"""
    axes = plt.gca()
    y_lim = axes.get_ylim()
    if info.windows.ms_reflexes is None:
        return
    legend_items = list()
    legend_names = list()
    try:
        # Add all specified reflex windows
        for section_name, section_reflex_info in info.windows.ms_reflexes[muscle].items():
            if section_name == info.section:
                for i, (reflex, reflex_window) in enumerate(section_reflex_info.items()):
                    xy = [reflex_window[0] * s2pr.utils.CONVERT_MS_TO_S, y_lim[0]]
                    width = (reflex_window[1] * s2pr.utils.CONVERT_MS_TO_S) - (reflex_window[0] * s2pr.utils.CONVERT_MS_TO_S)
                    height = y_lim[1] - y_lim[0]
                    rect = patches.Rectangle(xy=xy,
                                             width=width,
                                             height=height,
                                             linewidth=1,
                                             edgecolor=REFLEX_COLORS[i],
                                             facecolor=REFLEX_COLORS[i],
                                             alpha=0.2,
                                             label=reflex)
                    axes.add_patch(rect)
                    legend_items.append(rect)
                    legend_items.append(reflex)
        plt.legend(handles=legend_items, labels=legend_names, fontsize='x-small')
    except KeyError:
        pass


def set_x_lim(xlim):
    plt.xlim([xlim[0] * s2pr.utils.CONVERT_MS_TO_S, xlim[1] * s2pr.utils.CONVERT_MS_TO_S])


def save_figure(section):
    plt.tight_layout()
    figure_name = f'{section.info.trial}_{section.info.section}_reflexes.pdf'
    path = section.info.study_path / section.info.subject / 'figures' / 'reflexes'
    if not path.exists():
        path.mkdir()
    plt.savefig(path/figure_name)
    plt.close()
