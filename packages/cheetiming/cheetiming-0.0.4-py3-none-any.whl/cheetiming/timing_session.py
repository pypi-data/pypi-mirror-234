from __future__ import annotations

import timeit
from typing import List


class TimingSession(object):
    def __init__(self, name: str = None, autostart=True):
        self._name = name
        self._calls = 0
        self._elapsed = 0
        if autostart:
            self._start = timeit.default_timer()
        else:
            self._start = None

    def print_stats(self):
        return f'{self._calls} call(s), {self._elapsed} seconds'

    def __repr__(self):
        return f'Timer: {self._name or "(Unnamed)"}, ' + self.print_stats()

    def start(self):
        self._start = timeit.default_timer()

    def reset(self):
        self._calls = 0
        self._elapsed = 0
        self._start = None

    def stop(self, n_calls=1):
        # TODO: check if was not started
        self._elapsed += timeit.default_timer() - self._start
        self._calls += n_calls

    def update(self, other: TimingSession):
        self._name = other._name
        self._start = other._start
        self._calls = other._calls
        self._elapsed = other._elapsed

    @classmethod
    def aggregate_from_list(cls, timing_sessions: List[TimingSession]):
        agg_session = TimingSession(autostart=False)
        agg_session._calls = sum(s._calls for s in timing_sessions)
        agg_session._elapsed = sum(s._elapsed for s in timing_sessions)
        return agg_session

    @property
    def name(self):
        return self._name

    @property
    def calls(self):
        return self._calls

    @property
    def elapsed(self):
        return self._elapsed
