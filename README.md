# **logistro (low-hee-stro)**

`logistro` is an extremely light addition to `logging`.

It provides two *structured* and *human-readable* formats.

Additionally, it also includes `getPipeLogger()` which can be passed to `Popen()`
so that there stdout and stderr is piped to the already thread-safe logging
library.

With CLI flags:

* `--logistro-structured` which outputs JSON

* `--logistro-human` (default)

Or with functions: `logistro.set_structured()` and `logistro.set_human()`.

It also adds `logger.debug2(...)`: more verbose then `logger.debug(...)`.

Calling `logistro.betterConfig(...)` will apply the formatter selected
as the default (it will override what you set with `format`). It accepts
all normal arguments as `logging.basicConfig(...)`.

Calling `logistro.getLogger(__name__)` will apply the format to that logger...
*it will also call `betterConfig()` if you haven't called it already*.

Feel free to use the two formatters it provides manually: `human_formatter` and
`structured_formatter`.

```python
import logistro

logger = logistro.getLogger(__name__)

logger.debug2('hey, this still works! its just more informative')
logger.debug1('hey, this still works! its just more informative')
logger.info('hey, this still works! its just more informative')
logger.warning('hey, this still works! its just more informative')
logger.error('hey, this still works! its just more informative')
logger.critical('hey, this still works! its just more informative')
# following should be called in except: clause
logger.exception('hey, this still works! its just more informative')
```

Like logging, If using from multiple threads, call `betterConfig()` early.

### **Customize pytest_addoption()**

If you want to set the logistro args in your tests to use in your projects,
please use this method `customize_pytest_addoption()`. This enables the flags:

* `--logistro_human`
* `--logistro_structured`
* `--include_tags`
* `--exclude_tags`

In your conftest.py:

```python
import pytest
import logistro as logging

def pytest_addoption(parser):
    parser.addoption(
      "--debug",
      action="store_true",
      dest="debug",
      default=False
      )
    logging.customize_pytest_addoption(parser)
    # Use our function to improve your develop tools for logs with pytest
```

## Todo

* evaluate pytest (why do we need it)
  * evaluate argparse
* docs
* tests
* argument flag levels
* get it into choreographer

and after this, we continue refactor
