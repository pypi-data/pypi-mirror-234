import logging
import os
import sys
import time
import traceback
from traceback import TracebackException


def excepthook(exc_type, exc_message, tb):
    from .models import ExceptionModel

    module = tb.tb_frame.f_globals["__name__"]
    exc_traceback = "\n".join(traceback.format_exception(exc_type, exc_message, tb))
    filename = traceback.extract_tb(tb)[-1].filename
    lineno = traceback.extract_tb(tb)[-1].lineno
    for name, _module in sys.modules.items():
        if getattr(_module, "__file__", "") == filename:
            module = _module
    defaults = dict(
        module=module.__name__,
        exc_class="%s.%s" % (exc_class.__module__, exc_class.__name__),
        exc_message=exc_message,
        exc_traceback=exc_traceback,
        timestamp=round(time.time(), 3),
    )
    ExceptionModel.objects.update_or_create(defaults, filename=filename, lineno=lineno)


class ExceptionLogHandler(logging.Handler):
    def emit(self, record):
        from .models import ExceptionModel

        exc_traceback = traceback.format_exc()
        if record.exc_info:
            exc_class, exc_message, tb = record.exc_info
        else:
            exc_class, exc_message, tb = sys.exc_info()
        filename, lineno = tb.tb_frame.f_code.co_filename, tb.tb_lineno
        module = tb.tb_frame.f_globals["__name__"]
        for f in traceback.extract_tb(tb):
            if os.getcwd() in f.filename:
                filename, lineno = f.filename, f.lineno
        for name, _module in sys.modules.items():
            if getattr(_module, "__file__", "") == filename:
                module = _module
        defaults = dict(
            module=module.__name__,
            exc_class="%s.%s" % (exc_class.__module__, exc_class.__name__),
            exc_message=exc_message,
            timestamp=round(time.time(), 3),
        )
        ExceptionModel.objects.update_or_create(
            defaults,
            filename=filename,
            lineno=lineno,
        )
