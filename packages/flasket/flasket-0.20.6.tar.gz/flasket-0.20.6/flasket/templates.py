import functools
import typing as t

from flask import current_app, has_app_context

__all__ = ["template_global"]

g_template_global = {}


def template_global(name: str = None) -> t.Callable:
    fn = None
    if callable(name) and hasattr(name, "__name__"):
        fn = name
        name = fn.__name__

    def add_template_global(fn, name):
        if has_app_context():
            if name in g_template_global:
                return

            # This will fail with the flask error
            app = current_app.flasket
            app.logger.warning(f"Adding template global '{name}' is no longer possible during runtime.")
        else:
            g_template_global[name] = fn

    @functools.wraps(fn)
    def wrapped(fn):
        nonlocal name

        add_template_global(fn, name)
        return fn

    if fn:
        add_template_global(fn, name)
    return wrapped
