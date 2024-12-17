import inspect
import logging

import logistro.args as args

## New Constants and Globals

DEBUG2 = 5

logging.addLevelName(DEBUG2, "DEBUG2")

human_formatter = logging.Formatter("%(asctime)s - %(message)s")
human_formatter._logistro_human = True
human_formatter._logistro_structured = False

structured_formatter = logging.Formatter("%(message)s")
structured_formatter._logistro_structured = True
structured_formatter._logistro_human = False

default_handler = logging.StreamHandler()


# if called without a handler, sets defaults (and flags)
def set_human(handler=None):
    if not handler:
        args.parsed.human = True
        handler = default_handler
    handler.setFormatter(human_formatter)


# if called without a handler, sets defaults (and flags)
def set_structured(handler=None):
    if not handler:
        args.parsed.human = False
        handler = default_handler
    handler.setFormatter(structured_formatter)


def betterConfig(human=args.parsed.human):
    if human:
        default_handler.setFormatter(human_formatter)
    else:
        default_handler.setFormatter(structured_formatter)
    logging.basicConfig(handlers=[default_handler])


class LogistroLogger(logging.getLoggerClass()):
    # Improve the name of the log
    def __init__(self, name):
        betterConfig()
        super().__init__(name)

    def _get_context_info(self):
        # TODO: wrap all in try except as stuff might not work
        current_frame = inspect.currentframe()
        if not current_frame:
            # TODO: warn, we don't support this interpreter
            return None, None, None

        # this function is current_frame
        # and back again is the logging function the dev calls
        # TODO this will have to be automated to find non-logistro functions
        logistro_log_fn = current_frame.f_back

        # python module = python file
        calling_frame = logistro_log_fn.f_back  # calling frame
        calling_file = calling_frame.f_code.co_filename  # file path
        calling_function = calling_frame.f_code.co_name  # function name
        module_obj = inspect.getmodule(calling_frame)  # calling module
        if module_obj:
            calling_package = module_obj.__package__  # calling package
        else:
            calling_package = "None"

        # The function where logistro is used
        return calling_package, calling_file, calling_function

    # Returns true or false if tags match filter
    def _check_tag_filter(self, tags=set()):
        # Check None values
        if not filter:
            return True

        # Check tags
        included = args.parsed.included_tags
        if included and set(included).isdisjoint(set(tags)):
            return False

        excluded = args.parsed.excluded_tags
        if excluded and not set(excluded).isdisjoint(set(tags)):
            return False

        return True

    def generate_log_obj(self, msg, tags):
        # Fix Format
        # Fix inspection
        # TODO: this is where we format
        # TODO: but first, we read format
        package, file, function = self._get_context_info()
        # TODO: time
        # TODO: add in process helper
        log_obj = dict(
            package=package,
            file=file,
            function=function,
            msg=msg,
            tags=tags,
        )
        # TODO: get style and level
        return log_obj

    def log(self, level, msg, tags=None, *args, **kwargs):
        betterConfig()
        if isinstance(tags, str):
            tags = [tags]
        if tags:
            self._check_tag_filter(tags=set(tags))
        log_obj = self.generate_log_obj(msg, tags)
        formatted_msg = log_obj
        super().log(int(level), formatted_msg, *args, **kwargs)

    def debug2(self, msg, tags=None, *args, **kwargs):
        self.log(DEBUG2, msg, tags, *args, **kwargs)

    def debug(self, msg, tags=None, *args, **kwargs):
        self.log(logging.DEBUG, msg, tags, *args, **kwargs)

    def debug1(self, msg, tags=None, *args, **kwargs):
        self.log(logging.DEBUG, msg, tags, *args, **kwargs)

    def info(self, msg, tags=None, *args, **kwargs):
        self.log(logging.INFO, msg, tags, *args, **kwargs)

    def warning(self, msg, tags=None, *args, **kwargs):
        self.log(logging.WARNING, msg, tags, *args, **kwargs)

    def exception(self, msg, tags=None, *args, **kwargs):
        self.log(logging.ERROR, msg, tags, *args, **kwargs)

    def error(self, msg, tags=None, *args, **kwargs):
        self.log(logging.ERROR, msg, tags, *args, **kwargs)

    def critical(self, msg, tags=None, *args, **kwargs):
        self.log(logging.CRITICAL, msg, tags, *args, **kwargs)


logging.setLoggerClass(LogistroLogger)
logger = logging.getLogger(__name__)

debug1 = 0
debug2 = 0
info = 0
warning = 0
error = 0
info = 0
exception = 0
critical = 0
