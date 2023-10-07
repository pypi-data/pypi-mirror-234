# pysistant


```python
from pysistant.helpers import Timer


with Timer() as t:
    x = 10+20
    
    print(t.elapsed_time())
```