# **logistro (low-hee-stro)**

`logistro` is an extremely light addition to `logging`, providing sensible defaults.

It also includes `getPipeLogger()` which can be passed to `Popen()` so that its
`stderr` is piped to the already thread-safe `logging` library.

## CLI Flags

* `--logistro-level DEBUG|DEBUG2|INFO|WARNING|ERROR|CRITICAL`
* `--logistro-human` (default)
* `--logistro-structured` which outputs JSON

### Programmatic Alternatives

* `logistro.set_structured()`
* `logistro.set_human()`

*Generally, they must be called before any other logging call (See note below).*

## Additionally

`logger.debug2(...)` is more verbose than `logger.debug(...)`.

`logistro.betterConfig(...)` will apply the formatter  and level selected
as the default (it will ignore what you set with `format`). It accepts the same
arguments as `logging.basicConfig(...)`. **It is better to call this early in a
multithread program.**

`logistro.getLogger(...)` will call `betterConfig()`.

It provides two formatters

* `human_formatter`
* `structured_formatter`

### Example

```python
import logistro

logger = logistro.getLogger(__name__)

logger.debug2(...)
logger.debug(...) # or debug1()
logger.info(...)
logger.warning(...)
logger.error(...)
logger.critical(...)
logger.exception(...) # always inside except:

# For subprocesses:

pipe, logger = logistro.getPipeLogger(__name__+"-subprocess")
subprocess.Popen(cli_command, stderr=pipe)
os.close(pipe)
```

## Changing Logger Formatter Mid-Execution

With a typical setup, calling `set_structured()` or `set_human()`
and then `logistro.coerce_logger(logistro.getLogger())` will change the format.

See [the tech note](TECH_NOTE.md) for an intro into the complexities of `logging`.
