import spike2py_reflex as s2pr


def test_windows_types():
    window = s2pr.info.Window(single=1,
                            double=2,
                            double_single_pulse=3,
                            train_single_pulse=4)
    window_types = s2pr.info.WindowTypes(extract=window,
                                       plotting=window,
                                       reflexes={'a': 5},
                                       sd=[6, 7])
    assert window_types.extract.single == 1
    assert window_types.reflexes['a'] == 5

    window_types.clear()

    assert window_types.extract.single is None
    assert window_types.reflexes is None


def test_grouped_windows_initialise_with_win_info(demo_study_reflex):
    win_info = demo_study_reflex['windows']
    win = s2pr.info.GroupedWindows(win_info=win_info)

    assert win.ms.extract.single == [-250, 100]
    assert win.ms.plotting.double == [-25, 75]
    assert win.ms.sd == [-205, -5]

    assert win.idx.extract.single is None
    assert win.idx.plotting.double is None
    assert win.idx.sd is None


def test_grouped_windows_update(demo_study_reflex):
    win_info = demo_study_reflex['windows']
    win = s2pr.info.GroupedWindows(win_info=win_info)
    assert win.ms.sd == [-205, -5]

    new_window = [-50, -3]
    win.update({"sd": new_window})
    assert win.ms.sd == new_window

    extract_data = {"single": [1, 1],
                    "double": [2, 2],
                    "double_single_pulse": [3, 3],
                    "train_single_pulse": [4, 4]}
    win.update({"extract": extract_data})
    assert win.ms.extract.single == [1, 1]


def test_grouped_windows_update_fs(demo_study_reflex):
    win_info = demo_study_reflex['windows']
    win = s2pr.info.GroupedWindows(win_info=win_info)
    win.add_double_isi(50)
    win.add_fs(2000)


def test_grouped_windows_compute_x_axis(demo_study_reflex):
    win_info = demo_study_reflex['windows']
    win = s2pr.info.GroupedWindows(win_info=win_info)
    assert win._x_axis is None
    win.add_double_isi(50)
    win.fs = 1984
    win._get_x_axis()
    assert len(win._x_axis) == 3967


def test_grouped_windows_compute_idx(demo_study_reflex):
    win_info = demo_study_reflex['windows']
    win = s2pr.info.GroupedWindows(win_info=win_info)
    win.add_double_isi(50)
    win.add_fs(1984)
    assert win.idx.sd['single'] == [89, 486]
    assert win.idx.reflexes['Fdi']['mmax'] == {'hreflex': {'double': [[536, 575], [635, 675]],
             'single': [536, 575],
             'train': [70, 89]},
 'mmax': {'double': [[512, 536], [611, 635]],
          'single': [512, 536],
          'train': [46, 70]}}
    assert win.idx.extract.double == [-496, 298]


def test_grouped_windows_compute_x_axes(demo_study_reflex):
    win_info = demo_study_reflex['windows']
    win = s2pr.info.GroupedWindows(win_info=win_info)
    win.add_double_isi(50)
    win.add_fs(1984)
    assert len(win.x_axes.single) == 694
    assert len(win.x_axes.double) == 794
    assert len(win.x_axes.double_single_pulse) == 109
    assert len(win.x_axes.train_single_pulse) == 90


def test_windows_init(demo_study_reflex):
    win_info = demo_study_reflex['windows']
    win = s2pr.info.Windows(win_info)
    assert win._study.ms.sd == [-205, -5]


def test_windows_add_fs_compute_idx(demo_study_reflex):
    win_info = demo_study_reflex['windows']
    win = s2pr.info.Windows(win_info)
    win.double_isi = 50
    win.fs = 1984
    assert win._study.idx.sd == {'double': [89, 486], 'single': [89, 486]}


def test_windows_add_subject_long(demo_study_reflex, demo_subject_windows_long):
    win_info = demo_study_reflex['windows']
    win = s2pr.info.Windows(win_info)
    win.add_subject(demo_subject_windows_long)
    assert win._study.ms.sd == [-205, -5]
    assert win._subject.ms.sd == [-50, -20]
    assert win._subject.ms.plotting.single == [-25, 50]
    win.clear_subject()
    assert win._subject.ms.sd == None


def test_windows_add_subject_short(demo_study_reflex, demo_subject_windows_short):
    win_info = demo_study_reflex['windows']
    win = s2pr.info.Windows(win_info)
    win.add_subject(demo_subject_windows_short)

    assert win._study.ms.sd == [-205, -5]
    assert win._subject.ms.sd == [-51, -21]

    assert win._study.ms.reflexes['Fdi']['mmax'] == {'hreflex': [20, 40], 'mmax': [8, 20]}
    assert win._subject.ms.reflexes['Fdi']['mmax'] == {'hreflex': [26, 45], 'mmax': [6, 21]}

    assert win._study.ms.extract.single == [-250, 100]
    assert win._subject.ms.extract.single == [-250, 100]


def test_windows_add_subject_section(demo_study_reflex, demo_subject_windows_short, demo_section_windows_short):
    win_info = demo_study_reflex['windows']
    win = s2pr.info.Windows(win_info)
    win.add_subject(demo_subject_windows_short)
    win.add_section(demo_section_windows_short)

    assert win._study.ms.sd == [-205, -5]
    assert win._subject.ms.sd == [-51, -21]
    assert win._section.ms.sd == [-58, -26]

    assert win._study.ms.reflexes['Fdi']['mmax'] == {'hreflex': [20, 40], 'mmax': [8, 20]}
    assert win._subject.ms.reflexes['Fdi']['mmax'] == {'hreflex': [26, 45], 'mmax': [6, 21]}
    assert win._section.ms.reflexes['Fdi']['mmax'] == {'hreflex': [19, 39], 'mmax': [8, 26]}

    assert win._study.ms.extract.single == [-250, 100]
    assert win._subject.ms.extract.single == [-250, 100]
    assert win._section.ms.extract.single == [-250, 100]


def test_windows_add_subject_section_get_idx(demo_study_reflex, demo_subject_windows_short, demo_section_windows_short):
    win_info = demo_study_reflex['windows']
    win = s2pr.info.Windows(win_info)
    win.add_subject(demo_subject_windows_short)
    win.add_section(demo_section_windows_short)
    win.double_isi = 50
    win.fs = 1984
    assert win._study.idx.sd == {'double': [89, 486], 'single': [89, 486]}
    assert win._subject.idx.sd == {'double': [395, 454], 'single': [395, 454]}
    assert win._section.idx.sd == {'double': [381, 444], 'single': [381, 444]}

    assert win._study.idx.reflexes['Fdi']['mmax'] == {'hreflex': {'double': [[536, 575], [635, 675]],
             'single': [536, 575],
             'train': [70, 89]},
 'mmax': {'double': [[512, 536], [611, 635]],
          'single': [512, 536],
          'train': [46, 70]}}
    assert win._subject.idx.reflexes['Fdi']['mmax'] == {'hreflex': {'double': [[548, 585], [647, 684]],
             'single': [548, 585],
             'train': [82, 89]},
 'mmax': {'double': [[508, 538], [607, 637]],
          'single': [508, 538],
          'train': [42, 72]}}
    assert win._section.idx.reflexes['Fdi']['mmax'] == {'hreflex': {'double': [[534, 573], [633, 673]],
             'single': [534, 573],
             'train': [68, 89]},
 'mmax': {'double': [[512, 548], [611, 647]],
          'single': [512, 548],
          'train': [46, 82]}}

    assert win._study.idx.extract.single == [-496, 198]
    assert win._subject.idx.extract.single == [-496, 198]
    assert win._section.idx.extract.single == [-496, 198]


def test_windows_get_attributes(demo_study_reflex, demo_subject_windows_short, demo_section_windows_short):
    win_info = demo_study_reflex['windows']
    win = s2pr.info.Windows(win_info)
    win.add_subject(demo_subject_windows_short)
    win.add_section(demo_section_windows_short)
    win.double_isi = 50
    win.fs = 1984

    assert win.idx_sd == {'double': [381, 444], 'single': [381, 444]}
    assert win.idx_reflexes['Fdi']['mmax'] == {'hreflex': {'double': [[534, 573], [633, 673]],
             'single': [534, 573],
             'train': [68, 89]},
 'mmax': {'double': [[512, 548], [611, 647]],
          'single': [512, 548],
          'train': [46, 82]}}
    assert win.idx_extract.single == [-496, 198]

# # TODO: Add a test to make sure that if sd window not specified, sd idx set to None
