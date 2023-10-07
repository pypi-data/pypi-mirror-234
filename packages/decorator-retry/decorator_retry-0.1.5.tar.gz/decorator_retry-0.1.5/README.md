# A simple decorator for retry functions  

```python
@retry(ValueError, KeyError,
         retry = True, 
         attempts = 3,
         wait = 1,
         reraise = True,
         logger = logging.debug
         )
def func():
   pass
```
## Decorator parameters

### exceptions

*SPECIFIED* exception types.

### retry

if retry is True , retry when the decorated function throws the *SPECIFIED* exceptions.   
if retry is False , retry when the decorated function throws the *UNSPECIFIED* exceptions.   
Default is True.

### attempts

The number of retries attempted. Default is 3.  

### wait

The wait interval between retries (second).   
Default is 1 second.

### reraise

If reraise is True, when an exception is thrown by the decorated function, that exception will be rethrown. If raraise is False, then None is returned instead.   
Default is True.

### logger

The logger function will be used when the decorated function raise exception.
Default is logging.warning.