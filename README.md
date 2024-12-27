# **logistro (lo-hī-stro)**

`logistro` is an extremely light addition to `logging`, providing sensible defaults.

It also includes `getPipeLogger()` which can be passed to `Popen()` so that its
`stderr` is piped to the already thread-safe `logging` library.

## Quickstart

```python
import logistro

logger = logistro.getLogger(__name__)

logger.debug2(...) # new!
logger.debug(...) # or debug1()
logger.info(...)
logger.warning(...)
logger.error(...)
logger.critical(...)
logger.exception(...) # always inside except:

# For subprocesses:

pipe, logger = logistro.getPipeLogger(__name__+"-subprocess")
subprocess.Popen(cli_command, stderr=pipe)
os.close(pipe) # eventually
```

## CLI Flags

* `--logistro-level DEBUG|DEBUG2|INFO|WARNING|ERROR|CRITICAL`
* `--logistro-human` (default)
* `--logistro-structured` which outputs JSON

### Functions

* `logistro.set_structured()`
* `logistro.set_human()`

*Generally, they must be called before any other logging call (See note below).*

## Additionally


`logistro.betterConfig(...)` applies our formats and levels. It accepts the same
arguments as `logging.basicConfig(...)` except `format=`, which it ignores.
**It is better to call this early in a multithread program.**

`logistro.getLogger(...)` will ensure `betterConfig()`.

You can use our two formatters manually instead:

* `human_formatter`
* `structured_formatter`


## Changing Logger Formatter Mid-Execution

With a typical setup, calling `set_structured()` or `set_human()`
and then `logistro.coerce_logger(logistro.getLogger())` will change the format.

See [the tech note](TECH_NOTE.md) for an intro into the complexities of `logging`.
