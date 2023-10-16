from functools import partial

from ._version import __version__

from .timer_manager import create_timer
from .timer_manager import timing
from .timer_manager import iterate_with_timer
from .timer_manager import range_with_timer
from .timer_manager import timing_session
from .timer_manager import timing_report
from .timer_manager import timers
from .timer_manager import null_timer_range

run_with_timer = partial(range_with_timer, 1)

