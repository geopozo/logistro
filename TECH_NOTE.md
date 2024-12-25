# Technical Note

Python's `logging` is over-engineered and not quite good enough:

## Background

`Loggers` exist in a tree structure, hierarchy defined by the name.
There is a root logger that you cannot change.
`Loggers` have `Handlers`, `Handlers` have `Formatters`. When you call a logging
function on a `Logger`, it searches up the tree for all parent handlers.
In simple usage, usually only the root logger has a handler.

## Problem

* Changing the format mid-program means finding all the (relevant?) handlers
in the tree. `pytest` for example attaches other handlers so it can capture
logging. Our `better_config()` will set our format on the root logger's handlers.

* You cannot attach two formatters to a handler
* Two handlers cannot access the same file

Having both those be true simultaneously presents problems.

For our process logger, where a lot of context is erronenous,
we strip useless data from the process logger by using a filter.
