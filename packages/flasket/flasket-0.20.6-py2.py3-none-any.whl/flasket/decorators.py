import functools

from flask import current_app

__all__ = ["endpoint"]


def endpoint(fn):
    """
    Decorate a function to pass 'app' to it
    """

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        app = kwargs.pop("app", current_app.flasket)
        return fn(
            app=app,
            *args,
            **kwargs,
        )

    return wrapper
