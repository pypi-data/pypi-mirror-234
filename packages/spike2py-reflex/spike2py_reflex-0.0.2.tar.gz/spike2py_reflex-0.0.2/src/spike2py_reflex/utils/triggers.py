import numpy as np
from spike2py_preprocess.trial_sections import find_nearest_time_index

import spike2py_reflex as s2pr


class Triggers:

    def __init__(self, info, data):
        """

        Parameters
        ----------
        info
        data

        Attributes
        ----------
        extract: list of indexes corresponding to each trigger; for double stim it corresponds to the first trigger
        double: list of pairs of indexes corresponding to the pair of triggers in a double
        """

        section = info.section
        self.type = info.channels.triggers[section]["type"]

        trigger_channel = getattr(data, info.channels.triggers[section]["channels"])
        self._raw = trigger_channel.times

        emg = getattr(data, info.channels.emg[0])
        self._times = emg.times

        self._triggers = self._clean_triggers(info)

        self.extract = None
        self.double = None

        self._get_idx(info)

    def _clean_triggers(self, info):
        triggers = self._remove_khz()
        return self._remove_rejected_triggers(triggers, info)

    def _remove_khz(self):
        triggers = [self._raw[0]]
        for i in range(1, len(self._raw)):
            trig_isi = self._raw[i] - self._raw[i - 1]
            if trig_isi > s2pr.utils.KHZ_ISI_THRESHOLD:
                triggers.append(self._raw[i])
        return triggers

    def _remove_rejected_triggers(self, triggers: list, info) -> list:
        """Remove triggers flagged for removal.

        `rejected_triggers_times` are extract from the section-specific JSON file.
        If no triggers flagged for removal, `triggers` is returned unmodified.

        Parameters
        ----------
        triggers: Trigger times.
        rejected_trigger_times: List of value pairs indicating windows in which to remove triggers.
                                Example: [[5.5, 12], [45, 45.3]]
                                Triggers present between 5.5s and 12s, and those present between
                                45s and 45.3s would be removed.

        Returns
        -------
        List of trigger times.
        """
        if info.rejected_trig_windows:
            original_triggers = np.array(triggers)
            trigger_mask = np.bool_(np.ones(len(triggers)))  # Initial mask `True` for all triggers
            for lower_value, upper_value in info.rejected_trig_windows:
                lower = original_triggers > lower_value
                upper = original_triggers < upper_value
                trigger_mask *= np.invert(lower * upper)  # Update mask based on current trigger times
            triggers = original_triggers[trigger_mask]  # Use mask to retain only wanted triggers.
        return triggers

    def _get_idx(self, info):
        if self.type in [s2pr.utils.SINGLE, s2pr.utils.TRAIN]:
            self.extract = self._get_idx_single_triggers()
        elif self.type == s2pr.utils.DOUBLE:
            extract, double = self._get_idx_double_triggers(info)
            self.extract = extract
            self.double = double

    def _get_idx_single_triggers(self):
        """Get idx of each trigger."""
        trigger_indexes = list()
        for trigger in self._triggers:
            trigger_indexes.append(find_nearest_time_index(self._times, trigger))
        return trigger_indexes

    def _get_idx_double_triggers(self, info):
        """Get indexes to extract data for entire double and each individual reflex.

        It is possible that doubles were used at the start of section, followed by singles.
        Need to account for this possibility. If it happens, the single reflexes will be
        stored as reflex_1 of dc.ReflexDouble.reflex_1.
        """
        extract = list()
        double = list()
        # If trig1-trig2 have double isi, skip one pulse - trig2 cannot be start of new double.
        skip_one = False
        for i in range(len(self._triggers)):
            if not skip_one:
                trig1 = self._triggers[i]
                try:
                    # Last trig can be single or part of double.
                    # If part of double, can access triggers[i + 1] and the skip_one.
                    # If not, last trig will be trig1 and triggers[i + 1] will through AssertionError.
                    trig2 = self._triggers[i + 1]
                    isi = trig2 - trig1
                    try:
                        # If isi not approximately double_isi, AssertionError
                        self._is_double(isi, info)
                        extract.append(find_nearest_time_index(self._times, trig1))
                        double1 = find_nearest_time_index(self._times, trig1)
                        double2 = find_nearest_time_index(self._times, trig2)
                        double.append([double1, double2])
                        skip_one = True
                    except AssertionError:
                        extract.append(find_nearest_time_index(self._times, trig1))
                        double1 = find_nearest_time_index(self._times, trig1)
                        double.append([double1, None])
                except IndexError:
                    extract.append(find_nearest_time_index(self._times, trig1))
                    double1 = find_nearest_time_index(self._times, trig1)
                    double.append([double1, None])
            else:
                skip_one = False
        return extract, double

    def _is_double(self, isi, info):
        double_isi = info.stim_params.double_isi * s2pr.utils.CONVERT_MS_TO_S
        return np.testing.assert_approx_equal(actual=isi, desired=double_isi, significant=3)
