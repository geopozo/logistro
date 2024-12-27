"""
Logistro wraps `logging` for added defaults and subprocess logging.

Typical usage:

```python

import logistro
logger = logistro.getLogger(__name__)
logger.debug2("This will be printed more informatively")

# Advanced
pipe, logger = logistro.getPipeLogger(__name__)
# Pipe all stderr to our logger
subprocess.Popen(process_name, stderr=pipe)

# Eventually close the pipe in case other process doesn't
subprocess.wait()
os.close(pipe)
```
"""

from ._api import (
    DEBUG2,
    betterConfig,
    coerce_logger,
    getLogger,
    getPipeLogger,
    human_formatter,
    set_human,
    set_structured,
    structured_formatter,
)

__all__ = [
    "DEBUG2",
    "betterConfig",
    "coerce_logger",
    "getLogger",
    "getPipeLogger",
    "human_formatter",
    "set_human",
    "set_structured",
    "structured_formatter",
]
