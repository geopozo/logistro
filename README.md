# **logistro (low-hee-stro)**

Logistro is a VERY simple wrapper for python's logging.

## Flags for the logs
Logistro has for deafult value a `--logistro_human`, to has a human-redeable. And the --logistro_structured, it is better for the machines.
#### Example of `--logistro_human`:
```
2024-11-12 16:58:32,421 - DEBUG1 - my_package:my_package.main:print(): Hello world
2024-11-12 16:58:34,569 - DEBUG2 - my_package:my_package.main:print(): Success 'Hello world'
2024-11-12 16:58:34,570 - INFO - my_package:my_package.main:print(): You print a Hello world

```
#### Example of `--logistro_structured`:
```
{
    "time": "2024-12-02 17:06:50",
    "level": "DEBUG1",
    "package": "my_package",
    "file": "my_package.my_package",
    "module_function": "print",
    "message": "Hello world",
    "tag": null
}
```


## **Initialize logistro**
```python
import logistro as logging
```
This should initialize all the code within logistro to use in your own script

## **Curstomize parser**
If you want to set args in python with argparse to your project and use, please use this method `customize_parser()`. This parser enables the flags:
* `--logistro_human`
* `--logistro_structured`

```python
import argparse
import logistro as logging

parser_logging = logging.customize_parser(add_help=False) # This is our method to create the custom parser

# Here you must use the logistro parser as parent in argparse.ArgumentParser()
parser = argparse.ArgumentParser(description='tool to help debug problems', parents=[parser_logging])

# Set your arg
parser.add_argument('--no-run', dest='run', action='store_false')
```

## **Use logger**
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
