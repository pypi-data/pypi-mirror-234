## Usage

- Using as a context manager:
```python
import time
from cheetiming import timing

with timing() as t:
    time.sleep(.1)    
print(t)
print(t.elapsed)
```
Output:
```
Timer: (Unnamed), 1 call(s), 0.1137937 seconds
0.1137937
```
- Using as a _named_ context manager:
```python
import time
from cheetiming import timing

with timing('my_named_code_block') as t:
    time.sleep(.1)    
print(t)
print(t.name, t.elapsed)
```
Output:
```
Timer: my_named_code_block, 1 call(s), 0.10922489999999999 seconds
my_named_code_block 0.10922489999999999
```
- Reusing a _named_ context manager:
```python
import time
from cheetiming import timing, timing_report

with timing('my_repeating_code_block') as t:
    time.sleep(.1)
print(t)
with timing('my_repeating_code_block') as t:
    time.sleep(.1)    
print(t)
# print timing_report:
print(timing_report(t.name))
```
Output:
```
Timer: my_repeating_code_block, 1 call(s), 0.10937360000000002 seconds
Timer: my_repeating_code_block, 1 call(s), 0.10943849999999994 seconds
my_repeating_code_block:
 1:	1 call(s), 0.10937360000000002 seconds
 2:	1 call(s), 0.10943849999999994 seconds
total:	2 call(s), 0.21881209999999995 seconds


```
- Using in a ___for___ loop
```python
from cheetiming import iterate_with_timer, timing_session
      
my_list = [2, 4, 6, 7]
for i, item in iterate_with_timer(my_list):
    print(f'loop {i}: retrieving item:{item}')
print(timing_session)
print(timing_session.calls, 'calls', timing_session.elapsed, 'sec') 
```
Output:
```
loop 0: retrieving item:2
loop 1: retrieving item:4
loop 2: retrieving item:6
loop 3: retrieving item:7
Timer: (Unnamed), 4 call(s), 1.2699999999976619e-05 seconds
4 calls 1.2699999999976619e-05 sec
```
- Using in a _named_ ___for___ loop
```python
from cheetiming import iterate_with_timer, timing_session, timing_report
      
my_list = [2, 4, 6, 7]
for i, item in iterate_with_timer(my_list, 'my_loop_timer'):
    print(f'loop {i}: retrieving item:{item}')
print(timing_session)
print(timing_report('my_loop_timer'))
```
Output:
```
loop 0: retrieving item:2
loop 1: retrieving item:4
loop 2: retrieving item:6
loop 3: retrieving item:7
Timer: my_loop_timer, 4 call(s), 1.0599999999971743e-05 seconds
my_loop_timer:
 1:	4 call(s), 1.0599999999971743e-05 seconds
total:	4 call(s), 1.0599999999971743e-05 seconds


```
- Using as a ___range___ -like generator loop to repeat a code block _n_ times
```python
from cheetiming import range_with_timer, timing_session
      
for i in range_with_timer(5):
    print(f'loop {i}')
print(timing_session)
print(timing_session.calls, 'calls', timing_session.elapsed, 'sec')
```
Output:
```
loop 0
loop 1
loop 2
loop 3
loop 4
Timer: (Unnamed), 5 call(s), 1.3299999999993872e-05 seconds
5 calls 1.3299999999993872e-05 sec
```
- Using as a _named_ ___range___ -like generator loop to repeat a code block _n_ times
```python
from cheetiming import range_with_timer, timing_session, timing_report
      
for i in range_with_timer(5, 'my_range_timer'):
    print(f'loop {i}')
print(timing_session)
print(timing_report('my_range_timer'))
```
Output:
```
loop 0
loop 1
loop 2
loop 3
loop 4
Timer: my_range_timer, 5 call(s), 1.2099999999959365e-05 seconds
my_range_timer:
 1:	5 call(s), 1.2099999999959365e-05 seconds
total:	5 call(s), 1.2099999999959365e-05 seconds


```
- Using as a pseudo- ___range___ -like generator loop to run a code block only __once__
(it brings lower overhead than using a context manager)
```python
from cheetiming import run_with_timer, timing_session
      
for _ in run_with_timer():
    print('running my code block only once!')
print(timing_session)
```
Output:
```
running my code block only once!
Timer: (Unnamed), 1 call(s), 6.300000000014627e-06 seconds
```
- Using as a _named_ pseudo- ___range___ -like generator loop to run a code block only __once__
(it brings lower overhead than using a context manager)
```python
from cheetiming import run_with_timer, timing_session, timing_report
      
for _ in run_with_timer('my_pseudo_range_timer'):
    print('running my code block only once!')
print(timing_session)
print(timing_report('my_pseudo_range_timer'))
```
Output:
```
running my code block only once!
Timer: my_pseudo_range_timer, 1 call(s), 4.600000000021254e-06 seconds
my_pseudo_range_timer:
 1:	1 call(s), 4.600000000021254e-06 seconds
total:	1 call(s), 4.600000000021254e-06 seconds


```
- Using timing_report to print statistics for all named timers
```python
from cheetiming import timing_report

# using named timers from the examples above here ...

print(timing_report())
```
Output:
```
my_named_code_block:
 1:	1 call(s), 0.10922489999999999 seconds
total:	1 call(s), 0.10922489999999999 seconds

my_repeating_code_block:
 1:	1 call(s), 0.10937360000000002 seconds
 2:	1 call(s), 0.10943849999999994 seconds
total:	2 call(s), 0.21881209999999995 seconds

my_loop_timer:
 1:	4 call(s), 1.0599999999971743e-05 seconds
total:	4 call(s), 1.0599999999971743e-05 seconds

my_range_timer:
 1:	5 call(s), 1.2099999999959365e-05 seconds
total:	5 call(s), 1.2099999999959365e-05 seconds

my_pseudo_range_timer:
 1:	1 call(s), 4.600000000021254e-06 seconds
total:	1 call(s), 4.600000000021254e-06 seconds


```
- Printing a specific timer's report
```python
from cheetiming import timing_report

# using named timers from the examples above here ...

print(timing_report('my_repeating_code_block'))
```
Output:
```
my_repeating_code_block:
 1:	1 call(s), 0.10937360000000002 seconds
 2:	1 call(s), 0.10943849999999994 seconds
total:	2 call(s), 0.21881209999999995 seconds


```
