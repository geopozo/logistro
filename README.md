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
See NOTE below for why python's `logging` is so complicated.

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

Like logging, If using from multiple threads, call `betterConfig()` early.

## Technical Note

Python's `logging` is over-engineered and not quite good enough:

### Background

`Loggers` exist in a tree structure, hierarchy defined by the name.
There is a root logger that you cannot change.
`Loggers` have `Handlers`, `Handlers` have `Formatters`. When you call a logging
function on a `Logger`, it searches up the tree for all parent handlers.
In simple usage, usually only the root logger has a handler.

### Problem

Changing the format mid-program means finding all the (relevant?) handlers
in the tree. `pytest` for example attaches other handlers so it can capture
logging. We set our format on all of, and just, the root logger's handlers.
We strip useless data from the process logger by using a filter.
I don't want to shotgun handlers for a mid-execution change.
If you are customizing things this much, you can use our formatters directly.

* tests
* argument flag levels
* docs
* get it into choreographer

and after this, we continue refactor
