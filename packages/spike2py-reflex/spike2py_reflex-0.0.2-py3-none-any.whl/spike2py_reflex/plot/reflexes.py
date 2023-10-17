import spike2py_reflex as s2pr


def reflexes(section):
    """Generate raw data plots of all reflexes in a trial section

    Included are the individual traces and the mean trace, as well
    as windows indicating the region where reflex outcomes were
    calculated.
    """

    muscles = list(section.reflexes.keys())
    if section.reflexes[muscles[0]].type == s2pr.utils.SINGLE:
        s2pr.plot.plot_single(section)
        s2pr.plot.single_outcomes(section)
    elif section.reflexes[muscles[0]].type == s2pr.utils.TRAIN:
        s2pr.plot.plot_train(section)
        s2pr.plot.train_outcomes(section)
    elif section.reflexes[muscles[0]].type == s2pr.utils.DOUBLE:
        s2pr.plot.plot_double(section)
        s2pr.plot.double_outcomes(section)


