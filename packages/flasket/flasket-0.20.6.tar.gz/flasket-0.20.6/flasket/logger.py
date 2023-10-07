import logging
import sys

from flask.logging import default_handler

__all__ = []


class Logger:
    @staticmethod
    def configure() -> None:
        # Set default logging to a simple timestamp and message
        # default_handler is StreamHandler(stream=sys.stderr)
        formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
        default_handler.setStream(sys.stderr)
        default_handler.setLevel(logging.INFO)
        default_handler.setFormatter(formatter)

        # On the "stderr" logger we log info, warning and errors but not requests
        logger = logging.getLogger("stderr")
        handler = logging.StreamHandler(stream=sys.stderr)
        handler.setFormatter(formatter)
        Logger._clear_handlers(logger)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        # On the "request" logger, we log only the requests
        formatter = logging.Formatter("[%(asctime)s] - %(message)s")
        handler = logging.StreamHandler(stream=sys.stdout)
        handler.setFormatter(formatter)
        logger = logging.getLogger("request")
        Logger._clear_handlers(logger)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

    @staticmethod
    def disable() -> None:
        # Remove the FileHandlers from the Gunicorn logger
        # to prevent double logging
        for name in ["gunicorn.error", "gunicorn.access"]:
            logger = logging.getLogger(name)
            for handler in logger.handlers:
                # pylint: disable=protected-access
                if handler._gunicorn:
                    logger.removeHandler(handler)

        # Delete the werkzeug logger
        logger = logging.getLogger("werkzeug")
        Logger._clear_handlers(logger)

    @staticmethod
    def log_request(request: object, response: object) -> None:
        url = request.path
        if request.args:
            url = request.full_path
            url = url[:1024]
        header = request.headers.get("User-Agent", "")
        message = f'{request.remote_addr} - "{request.method} {url}" {response.status_code} - {header}'

        logger = logging.getLogger("request")
        logger.info(message)

    @staticmethod
    def _clear_handlers(logger) -> None:
        # Clear handlers before adding new handlers
        # This prevents multiple handlers and multiple
        # printing during unit tests
        for handler in logger.handlers:
            logger.removeHandler(handler)
