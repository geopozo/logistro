# **logistro (low-hee-stro)**

Logistro is a VERY simple wrapper for python's logging.

## Quick start
In our my_package/tests/app.py:

```python
import logistro as logging

logging.critical("Hello world with critical")
logging.error("Hello world with error")
logging.warning("Hello world with warning")
logging.info("Hello world with info")

logging.set_level(logging.DEBUG2)
logging.debug1("Hello world with debug1")
logging.debug2("Hello world with debug2")

```
In bash:

```bash
$ python tests/quick_start.py
```
In the log:

```log
WARNING: Verify the arguments ['tests/quick_start.py']
2024-12-06 14:31:47,232 - CRITICAL - None:__main__:<module>(): Hello world with critical
2024-12-06 14:31:47,233 - ERROR - None:__main__:<module>(): Hello world with error
2024-12-06 14:31:47,233 - WARNING - None:__main__:<module>(): Hello world with warning
2024-12-06 14:31:47,233 - DEBUG1 - None:__main__:<module>(): Hello world with debug1
2024-12-06 14:31:47,233 - DEBUG2 - None:__main__:<module>(): Hello world with debug2

```


## Flags for the logs
`Logistro` defaults to `--logistro_human`, which provides a human-readable format. Alternatively, `--logistro_structured` is better suited for machines, as it uses a JSON format for viewing logs.
#### Example of `--logistro_human`:
In our my_package/tests/app.py
```python
import my_package
import logistro as logging

logging.set_level(logging.DEBUG2)

logging.info("This is app.py to verify logistro functions")
my_package.print_module()
logging.info("Thanks!")
```
In bash:

```bash
$ python tests/app.py
```
In the log:
```log
WARNING: Verify the arguments ['tests/app.py']
2024-12-06 14:10:05,735 - INFO - None:__main__:<module>(): This is app.py to verify logistro functions
2024-12-06 14:10:05,735 - DEBUG2 - my_package:my_package.module:get_file(): The functions get_file() starts here
2024-12-06 14:10:05,735 - INFO - my_package:my_package:print_module(): We are in my_package (['info'])
2024-12-06 14:10:05,735 - DEBUG1 - my_package:my_package:print_module(): Success print_module
2024-12-06 14:10:05,736 - INFO - None:__main__:<module>(): Thanks!

```
#### Example of `--logistro_structured`:
In our my_package/tests/app.py
```python
import my_package
import logistro as logging

logging.set_level(logging.DEBUG2)

logging.info("This is app.py to verify logistro functions")
my_package.print_module()
logging.info("Thanks!")
```
In bash:
```bash
$ python tests/app.py --logistro_structured
```
In the log:
```log
WARNING: Verify the arguments ['tests/app.py']
{
    "time": "2024-12-06 14:14:53",
    "level": "INFO",
    "package": null,
    "file": "__main__",
    "module_function": "<module>",
    "message": "This is app.py to verify logistro functions",
    "tags": null
}
{
    "time": "2024-12-06 14:14:53",
    "level": "DEBUG2",
    "package": "my_package",
    "file": "my_package.module",
    "module_function": "get_file",
    "message": "The functions get_file() starts here",
    "tags": null
}
{
    "time": "2024-12-06 14:14:53",
    "level": "INFO",
    "package": "my_package",
    "file": "my_package",
    "module_function": "print_module",
    "message": "We are in my_package",
    "tags": [
        "info"
    ]
}
{
    "time": "2024-12-06 14:14:53",
    "level": "DEBUG1",
    "package": "my_package",
    "file": "my_package",
    "module_function": "print_module",
    "message": "Success print_module",
    "tags": null
}
{
    "time": "2024-12-06 14:14:53",
    "level": "INFO",
    "package": null,
    "file": "__main__",
    "module_function": "<module>",
    "message": "Thanks!",
    "tags": null
}

```


## **Initialize logistro**
```python
import logistro as logging
```
This should initialize all the code within logistro to use in your own script

### **Set the level**
Set the logistro logger level. Use `set_level(lvl)` and customize your logs. The level must be integer.

```python
import logistro as logging

logging.set_level(logging.DEBUG2) # This change the level to the lowest level of logistro
logging.set_level(logging.ERROR) # This change the level to ERROR, just will see logs with ERROR and CRITICAL
```

## **Funtions for the logs**

All the fuctions in logistro to log, have this parameters:
* `message` : Is the message of the log, this doesn't have default value
* `tags` : This is a new strategy for from logistro, you can set tags for your logs to improve the debugging. The default value is `None`
* `stream_output` : You can set the stream output for the structured logs (for human logs, you must set this with the logger with logging strategies). The default value is `sys.stderr`.

#### The avaible functions are:
* `debug1()`
* `debug2()`
* `info()`
* `warn()`
* `error()`
* `critical()`

## **Details**
The functions and attributes described here are useful for deep develop for logs.

### **Customize parser**
If you want to set args in python with argparse to your project and use it, please use this method `customize_parser()`. This parser enables the flags:
* `--logistro_human`
* `--logistro_structured`
* `--include_tags`
* `--exclude_tags`

```python
import argparse
import logistro as logging

parser_logging = logging.customize_parser(add_help=False) # This is our method to create the custom parser

# Here you must use the logistro parser as parent in argparse.ArgumentParser()
parser = argparse.ArgumentParser(description='tool to help debug problems', parents=[parser_logging])

# Set your arg
parser.add_argument('--no-run', dest='run', action='store_false')
```

### **Customize pytest_addoption()**
If you want to set the logistro args in your tests to use in your projects, please use this method `customize_pytest_addoption()`. This enables the flags:
* `--logistro_human`
* `--logistro_structured`
* `--include_tags`
* `--exclude_tags`

In your conftest.py:
```python
import pytest
import logistro as logging

def pytest_addoption(parser):
    parser.addoption("--debug", action="store_true", dest="debug", default=False)
    logging.customize_pytest_addoption(parser) # Use our function to improve your develop tools for logs with pytest
```


### **Use logger**
You can use use the logger from logistro as you want, just get the attribute `.logger`.
```python
import logistro as logging

logger = logistro.logger

```
To set the level, you must use the logger of logistro:
```python
import logistro as logging

logging.logger.setLevel(logging.DEBUG2) 
```
### **Use human format**
Set the human format in your code without the flags. Use `set_human()` and simplify this task. Note: The default format in logistro is human.

### **Use structured format**
Set the structure format in your code without the flags. Use `set_structured()` and simplify this task. This is the best for machines.