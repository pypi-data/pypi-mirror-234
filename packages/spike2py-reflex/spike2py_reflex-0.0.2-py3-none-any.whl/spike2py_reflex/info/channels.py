"""Class to hold channel-related info that updates as required."""

from typing import Union
from dataclasses import dataclass


@dataclass
class ChannelsInfo:
    emg: list
    triggers: dict
    stim_intensity: Union[str, None] = None


class Channels:
    """Channel information to process study, subject and section.

    Channel information is stored in an instance of `ChannelsInfo`, but is
    externally accessed as class properties:
      - Channels.emg
      - Channels.triggers
      - Channels.stim_intensity
    By accessing the data in this way when process a given section, the user
    will be sure to be accessing the correct information. section-level
    information trumps subject-level, which trumps study-level.
    """

    def __init__(self, study_channel_info: Union[None, dict] = None):
        """
        Parameters
        ----------
        study_channel_info
            Contains information about channels required to process data with
            spike2py_reflex. Expected keys are "emg", "triggers" and
            "stim_intensity". The values associated with the "triggers" key
            are the name of relevant spike2py_reflex section, the spike2py
            channel name associated with the trigger, and the type of trigger
            ("single", "double", "train"). "stim_intensity" has a value
            corresponding to the spike2py channel name containing the stimulus
            intensity (if one was used).

        Examples
        --------
        {"emg": ["Fdi"],
        "triggers": {
            "mmax": {
                "channels": "Mmax",
                "type": "single"
                },
            "hreflex": {
                "channels": "Ds8",
                "type": "double"
                }
            },
        "stim_intensity": "Stim"
        }

        """
        self._study = None
        self._subject = None
        self._section = None
        if study_channel_info is not None:
            self._study = ChannelsInfo(**study_channel_info)

    def add_subject(self, subject_channel_info=None):
        """Add channel information for a subject"""
        if subject_channel_info is not None:
            self._subject = ChannelsInfo(**subject_channel_info)
        elif subject_channel_info is None:
            self._subject = self._study

    def add_section(self, section_channel_info=None):
        """Add channel information for a section"""
        if section_channel_info is not None:
            self._section = ChannelsInfo(**section_channel_info)
        elif section_channel_info is None:
            self._section = self._subject

    def clear_subject(self):
        """Clear subject-level channel information"""
        self._subject = None

    def clear_section(self):
        """Clear section-level channel information"""
        self._section = None

    @property
    def emg(self) -> list:
        """List of one or more emg channels from which to extract reflexes"""
        return self._section.emg

    @property
    def triggers(self) -> dict:
        """Dict for each section specifying trigger channel and trigger type"""
        return self._section.triggers

    @property
    def stim_intensity(self) -> Union[str, None]:
        """Str of specifying stimulation intensity channel (if used)"""
        return self._section.stim_intensity
