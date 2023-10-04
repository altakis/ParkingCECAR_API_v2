import os.path

from .constants import LOGGING_DIR


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "extremely_verbose": {
            "format": "{name} {levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "debug_file_handler": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(
                LOGGING_DIR, "debug.log"
            ),  # Log debug level messages to this file
            "formatter": "extremely_verbose",
        },
        "info_file_handler": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(
                LOGGING_DIR, "info.log"
            ),  # Log info level messages to this file
            "formatter": "verbose",
        },
        "error_file_handler": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": os.path.join(
                LOGGING_DIR, "error.log"
            ),  # Log error level messages to this file
            "formatter": "extremely_verbose",
        },
        "critical_file_handler": {
            "level": "CRITICAL",
            "class": "logging.FileHandler",
            "filename": os.path.join(
                LOGGING_DIR, "critical.log"
            ),  # Log critical level messages to this file
            "formatter": "extremely_verbose",
        },
        "console_debug_handler": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",  # Log debug messages to the console
            "formatter": "extremely_verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": [
                "debug_file_handler",
                "info_file_handler",
                "error_file_handler",
                "critical_file_handler",
                "console_debug_handler",
            ],
            "level": "INFO",
            "propagate": True,
        },
    },
}
