import spike2py_reflex as s2pr


def test_triggers_singles(info_data_mmax):
    triggers = s2pr.utils.Triggers(info_data_mmax[0], info_data_mmax[1])
    assert triggers.type == 'single'
    print(triggers._raw)
    assert round(triggers._raw[0]) == 155
    assert len(triggers._raw) == 6
    assert triggers.extract == [17453, 62332, 98842, 139727, 178267, 199410]
    assert len(triggers.extract) == 6
    assert triggers.double is None


def test_triggers_doubles(info_data_hreflex):
    triggers = s2pr.utils.Triggers(info_data_hreflex[0], info_data_hreflex[1])
    assert triggers.type == 'double'
    assert round(triggers._raw[0]) == 806
    assert len(triggers._raw) == 14
    assert triggers.extract == [18775, 54235, 80455, 100836, 119376, 140202, 159884]
    assert triggers.double == [[18775, 18874],
                               [54235, 54334],
                               [80455, 80555],
                               [100836, 100936],
                               [119376, 119475],
                               [140202, 140301],
                               [159884, 159983]]


def test_triggers_ramp(info_data_ramp):
    triggers = s2pr.utils.Triggers(info_data_ramp[0], info_data_ramp[1])
    assert triggers.type == 'train'
    assert round(triggers._raw[0]) == 1504
    assert len(triggers._raw) == 1663
    assert len(triggers.extract) == 1663
    assert triggers.double is None


