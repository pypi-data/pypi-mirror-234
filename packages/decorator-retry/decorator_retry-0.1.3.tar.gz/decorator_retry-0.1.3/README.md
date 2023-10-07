# A simple decorator for retry functions  

```
In [1]: import logging
   ...: from decorator_retry import retry
   ...: 

In [2]: @retry(ValueError, KeyError, retry=True, attempts=3, wait=1.5, reraise=True, logger=logging.warning)
   ...: def foo():
   ...:     raise ValueError("Raise")
   ...: 

In [3]: foo()
WARNING:root:foo raise ValueError in specified list, will try again.
WARNING:root:foo raise ValueError in specified list, will try again.
WARNING:root:foo raise ValueError in specified list, will try again.
WARNING:root:foo will reraise ValueError.
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
...
ValueError: Raise

In [4]: @retry(ValueError, KeyError, retry=False, attempts=3, wait=1.5, reraise=True, logger=logging.warning)
   ...: def foo():
   ...:     raise ValueError("Raise")
   ...: 

In [5]: foo()
WARNING:root:foo raise ValueError, will not retry.
WARNING:root:foo will reraise ValueError.
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
...
ValueError: Raise

In [6]: @retry(ValueError, KeyError, retry=True, attempts=3, wait=1.5, reraise=False, logger=logging.warning)
   ...: def foo():
   ...:     raise ValueError("Raise")
   ...: 

In [7]: foo()
WARNING:root:foo raise ValueError in specified list, will try again.
WARNING:root:foo raise ValueError in specified list, will try again.
WARNING:root:foo raise ValueError in specified list, will try again.
WARNING:root:foo will not reraise ValueError.

In [8]: @retry(ValueError, KeyError, retry=False, attempts=3, wait=1.5, reraise=False, logger=logging.warning)
   ...: def foo():
   ...:     raise KeyError("Raise")
   ...: 

In [9]: foo()
WARNING:root:foo raise KeyError, will not retry.
WARNING:root:foo will not reraise KeyError.

```

