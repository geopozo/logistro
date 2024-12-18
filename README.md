# **logistro (low-hee-stro)**

`logistro` is an extremely light addition to `logging`.

It provides two *structured* and *human-readable* formats with better defaults.

Additionally, it also includes `getPipeLogger()` which can be passed to `Popen()`
so that there `stdout` and `stderr` is piped to the already thread-safe `logging`
library.

Set level by flag: `--logistro-level DEBUG|DEBUG2|INFO|WARNING|ERROR|CRITICAL`

With CLI flags:

* `--logistro-human` (default)

* `--logistro-structured` which outputs JSON

Or with functions: `logistro.set_structured()` and `logistro.set_human()`.
Generally, they must be called before any other logging call.
(See note below about changing mid-program).

It also adds `logger.debug2(...)`: more verbose then `logger.debug(...)`.

Calling `logistro.betterConfig(...)` will apply the formatter  and level selected
as the default (it will ignore what you set with `format`). It accepts
all other normal arguments as `logging.basicConfig(...)`.

Calling `logistro.getLogger(...)` will also call `betterConfig()`
if you haven't called it already*.

Feel free to use the two formatters it provides manually: `human_formatter` and
`structured_formatter`.

```python
import logistro

logger = logistro.getLogger(__name__)

logger.debug2('hey, this still works! its just more informative')
logger.debug1('hey, this still works! its just more informative')
# debug1 = debug
logger.debug('hey, this still works! its just more informative')
logger.info('hey, this still works! its just more informative')
logger.warning('hey, this still works! its just more informative')
logger.error('hey, this still works! its just more informative')
logger.critical('hey, this still works! its just more informative')
# following should be called in except: clause
logger.exception('hey, this still works! its just more informative')
```

## Changing Logger Formatter Mid-Execution

If you don't have any weird setup, and you need to change the logging style
mid-execution, try calling an above function like `set_structured()`
and then `logistro.coerce_logger(logistro.getLogger())`. See the file
*TECH_NOTE.md* for an intro into the complexities of Python's `logging`.
Like `logging`, if using from multiple threads, call `betterConfig()` early.
