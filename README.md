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
Generally, they can be called once before anything else happens in logging.
(See note below about changing mid-program).

It also adds `logger.debug2(...)`: more verbose then `logger.debug(...)`.

Calling `logistro.betterConfig(...)` will apply the formatter selected
as the default (it will gnore what you set with `format`). It accepts
all normal arguments as `logging.basicConfig(...)`.

Calling `logistro.getLogger(__name__)` will also call `betterConfig()`
if you haven't called it already*.

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

## Changing Logger Formatter Mid-Execution

If you don't have any weird setup, and you need to change the logging style
mid-execution, try calling an above function like `set_structured()`
and then `logistro.coerce_logger(logistro.getLogger())`. See the file
*TECH_NOTE.md* for an intro into the complexities.
Like logging, If using from multiple threads, call `betterConfig()` early.


* tests
* argument flag levels
* docs
* get it into choreographer

and after this, we continue refactor
