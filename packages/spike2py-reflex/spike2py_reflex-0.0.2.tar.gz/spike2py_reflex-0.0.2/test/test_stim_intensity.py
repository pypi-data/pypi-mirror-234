import spike2py_reflex as s2pr


def test_get_stim_intensity(info_data_hreflex):
    info, data = info_data_hreflex
    intensities = s2pr.utils.get_stim_intensity(info, data)
    assert intensities == [19, 19, 19, 19, 19, 19, 19]
