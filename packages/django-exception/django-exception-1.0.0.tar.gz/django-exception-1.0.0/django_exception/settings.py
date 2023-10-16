LOGGING = {
    "version": 1,
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
        "django_exception": {
            "level": "ERROR",
            "class": "django_exception.ExceptionLogHandler",
        },
    },
    "root": {
        "handlers": ["console", "django_exception"],
        "level": "DEBUG",
    },
    "loggers": {
        "django_exception": {
            "level": "ERROR",
            "handlers": ["django_exception"],
            "propagate": True,
        },
    },
}
