"""Package with classes and dataclasses to manage spike2py_reflex information

The main class is `Info`. It is populated and updated as data is being
processed. It holds and updates instances of the other classes: Channel,
StimParams, TrialSections, and Windows.

A key functionality of `Info` and the other classes is that, depending on
whether the subject or the trial required tweaks to aspects of the info, the
changes to the info will be retained for given trial(s) and subject(s). In all
other instances the study-level info will be used.

"""

from .channels import Channels
from .stim_params import StimParams
from .windows import Window, Windows, WindowTypes, GroupedWindows
from .trials_sections import TrialsSections
from .info import Info
