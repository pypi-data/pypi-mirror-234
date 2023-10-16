import time
import pytest
from cheetiming import timing, timers, timing_session, iterate_with_timer, range_with_timer, run_with_timer


def test_ctx_manager():
    with timing('my_name') as t:
        time.sleep(.5)
    assert t.calls == 1
    assert 0 < t.elapsed < 1
    assert timers['my_name'][-1] is t


def test_iterate_with_timer():
    for i, item in iterate_with_timer([2,3,4], 'iterate_timer'):
        time.sleep(.1)
    assert timing_session.calls == 3
    assert 0 < timing_session.elapsed < 1
    assert timers['iterate_timer'][-1].calls == timing_session.calls
    assert timers['iterate_timer'][-1].name == timing_session.name
    assert timers['iterate_timer'][-1].elapsed == timing_session.elapsed


def test_range_with_timer():
    for i in range_with_timer(3, 'range_timer'):
        time.sleep(.1)
    assert timing_session.calls == 3
    assert 0 < timing_session.elapsed < 1
    assert timers['range_timer'][-1].calls == timing_session.calls
    assert timers['range_timer'][-1].name == timing_session.name
    assert timers['range_timer'][-1].elapsed == timing_session.elapsed


def test_run_with_timer():
    for i in run_with_timer('run_timer'):
        time.sleep(.1)
    assert timing_session.calls == 1
    assert 0 < timing_session.elapsed < 1
    assert timers['run_timer'][-1].calls == timing_session.calls
    assert timers['run_timer'][-1].name == timing_session.name
    assert timers['run_timer'][-1].elapsed == timing_session.elapsed


# def test_recreate_timer_calls_count(timer):
#     for _ in timer.timing('my_name1'):
#         pass
#     for _ in timer.timing('my_name2', 1000):
#         pass
#     for _ in timer.timing('my_name1', 1000):
#         pass
#     assert timer.timing_data['my_name1']['calls'] == 1001
#     assert timer.timing_data['my_name2']['calls'] == 1000
#
#
# def test_recreate_timer_calls_count_time(timer):
#     for _ in timer.timing('my_name1'):
#         time.sleep(1.1)
#     for _ in timer.timing('my_name2', 4):
#         time.sleep(.3)
#     for _ in timer.timing('my_name1', 2):
#         time.sleep(1.1)
#     assert timer.timing_data['my_name1']['calls'] == 3
#     assert timer.timing_data['my_name2']['calls'] == 4
#
#     assert 3 < timer.timing_data['my_name1']['elapsed'] < 4
#     assert 1 < timer.timing_data['my_name2']['elapsed'] < 2


