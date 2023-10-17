# performance_tester

Collection of modules for testing performance.

## Installation
Command
```bash
pip install performance_tester
```
or add the following line in Pipfile if you use Pipenv
```
[dev-packages]
performance_tester = "*"
```

## Examples
```py
from performance_tester import measure_execution_time

@measure_execution_time(100)
def adder(a, b): # the function that you want to check the performance
    c = a + b
    return c

result = adder(1, 2)
```
Output:
```
100 loops:
mean: 3.573999492800795e-07 sec.
std : 1.1951605991912876e-07 sec.
max : 1.4500001270789653e-06 sec.
min : 3.199984348611906e-07 sec.
```
