from contextlib import contextmanager
from typing import Iterable

from cheetiming.timing_session import TimingSession


class TimerManager:
    """
    this instance is typically created once per module
    """
    def __init__(self, manager_name: str):
        self._timers = {}
        self._name = manager_name
        self.default_timing_session = TimingSession(autostart=False)

    def _start_new_timing_session(self, name: str = None):
        timing_session = TimingSession(name, autostart=False)
        if name:
            if timing_session.name not in self._timers:
                self._timers[timing_session.name] = [timing_session]
            else:
                self._timers[timing_session.name].append(timing_session)
        timing_session.start()
        return timing_session

    def _stop_timing_session(self, timing_session: TimingSession, n_calls=1):
        timing_session.stop(n_calls=n_calls)
        self.default_timing_session.update(timing_session)

    @contextmanager
    def timing(self, name: str = None):
        timing_session = self._start_new_timing_session(name)
        try:
            timing_session.start()
            yield timing_session
        finally:
            self._stop_timing_session(timing_session)

    def iterate_with_timer(self, iterable_: Iterable, name: str = None):
        timing_session = self._start_new_timing_session(name)
        i = -1
        for i, item in enumerate(iterable_):
            yield i, item
        # TODO: test .stop is not called before the loop ends properly
        self._stop_timing_session(timing_session, n_calls=i+1)

    def range_with_timer(self, stop: int, name: str = None):
        timing_session = self._start_new_timing_session(name)
        i = -1
        for i in range(stop):
            yield i
        self._stop_timing_session(timing_session, n_calls=i+1)

    def timing_report(self, timer_name: str = None):
        def _session_report(timer_name, timing_sessions):
            s = f'{timer_name}:\n'
            for i, sess in enumerate(timing_sessions):
                s += f' {i + 1}:\t{sess.print_stats()}\n'
            total_of_sessions = TimingSession.aggregate_from_list(timing_sessions)
            s += f'total:\t{total_of_sessions.print_stats()}\n\n'
            return s

        if timer_name:
            if timer_name not in self._timers:
                # Exception will not be raised to let the main code (except timing) run normally
                return f'Timer named {timer_name} not found.'
            timing_sessions = self._timers[timer_name]
            return _session_report(timer_name, timing_sessions)
        else:
            s = ''
            for (timer_name, timing_sessions) in self._timers.items():
                s += _session_report(timer_name, timing_sessions)
            return s

    @property
    def timers(self):
        return self._timers


def create_timer(timer_name: str):
    """
    While timer_name is not checked to be unique in this package,
    it's highly recommended to create timers with unique names.


    :param timer_name:
    :type timer_name:
    :return:
    :rtype:
    """
    return TimerManager(timer_name)


default_timer_manager = TimerManager('__default_timer_manager__')

timing = default_timer_manager.timing
iterate_with_timer = default_timer_manager.iterate_with_timer
range_with_timer = default_timer_manager.range_with_timer
timing_session = default_timer_manager.default_timing_session
timing_report = default_timer_manager.timing_report
timers = default_timer_manager.timers

# TODO: currently not tested and not used
named_timer_managers = {}


def null_timer_range(name: str = None):
    """
    a placeholder for cheetiming.run_with_timer when no timer is instantiated
    :param name:
    :return:
    """
    for i in range(1):
        yield i


def reset_timers():
    timers.clear()