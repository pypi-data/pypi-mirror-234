import matplotlib.pyplot as plt

import spike2py_reflex as s2pr

PLOT_WIDTH_SCALING = 1
PLOT_HEIGHT_SCALING = 1


def plot_train(section):
    """Plot section train reflexes (singles).

    Generates a plot with n columns, where n = number_muscles, and m rows,
    where m = number of stimulation intensities. Each column plots the data
    extracted for each reflex, and also the avg reflex, and this with the `plot`
    window applied to provide a better view of the extracted reflexes. Also
    provided on this plot data are the windows provided from which to compute
    reflex outcomes.

    """

    info = section.info
    muscles, n_muscles, intensities, n_intensities = s2pr.plot.get_muscles_and_intensities(section)
    plot_width, plot_height = s2pr.plot.get_plot_width_height(n_muscles, n_intensities)
    plt.figure(figsize=(plot_width, plot_height * n_intensities))
    _gen_figure(muscles, n_muscles, intensities, n_intensities, section, info)
    plt.tight_layout()
    s2pr.plot.save_figure(section)


def _gen_figure(muscles, n_muscles, intensities, n_intensities, section, info):
    """For each intensity of each muscle, add subplots"""
    subplot = 1
    for intensity in intensities:
        for muscle in muscles:
            plt.subplot(n_intensities, n_muscles, subplot)
            s2pr.plot.overlay_reflexes(section, muscle, intensity, legend=False)
            s2pr.plot.add_reflex_windows(info, muscle)
            s2pr.plot.set_x_lim(section.info.windows.ms_plotting.train_single_pulse)
            subplot += 1
