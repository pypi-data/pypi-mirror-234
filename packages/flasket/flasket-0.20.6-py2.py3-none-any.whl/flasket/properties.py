import logging
import typing as t

__all__: t.List[str] = [
    "LoggerProperties",
]


class LoggerProperties:
    """
    Minimal class for inheritance of the logger property
    """

    @property
    def logger(self) -> logging.Logger:
        """
        Return a :class:`logging.Logger` named ``stderr``
        """
        return logging.getLogger("stderr")


### from .exceptions import HTTPExceptions
### class FlasketProperties(HTTPExceptions):
###     def __init__(self, flasket):
###         self._flasket = flasket
###
###     # The class accesses fields that exist only
###     # on the flasket class
###
###     #    @property
###     #    def settings(self) -> t.Dict[str, t.Any]:
###     #        """
###     #        Return Flasket configuration used at start
###     #        """
###     #        return self._flasket._settings
###
###     @property
###     def options(self) -> t.Dict[str, t.Any]:
###         """
###         Return Flasket options used at start
###         """
###         return self._flasket._cfg
###
###     @property
###     def rootpath(self) -> str:
###         """
###         Return Flasket rootpath used at start
###         """
###         return self._flasket._rootpath
###
###     @property
###     def clients(self) -> object:
###         return self._flasket._clients
###
###     @property
###     def sitename(self) -> str:
###         """
###         Return combination of network host and port
###         """
###         return self._flasket.sitename
###
###     @property
###     def host(self) -> str:
###         """
###         Network hosts on which Flasket is listening on.
###         """
###         return self._flasket.host
###
###     @property
###     def port(self) -> int:
###         """
###         Network post on which Flasket is listening on.
###         """
###         return self._flasket.port
###
###     @property
###     def baseurl(self) -> str:
###         """
###         Returns baseurl "{scheme}://{netloc}"
###         """
###         return self._flasket.baseurl
###
###
### @define(kw_only=True, slots=False)
### class FlaskProperties:
###     _flask = field(default=None, init=False)
###
###     @property
###     def flask(self) -> flask.Flask:
###         """
###         Return underlying Flask object
###         """
###         return self._flask
###
###     def __call__(self, environ: dict, start_response):
###         return self._flask.wsgi_app(environ, start_response)
###
###     @property
###     def current_app(self) -> t.Any:
###         """
###         Return Flask current_app
###         """
###         return flask.current_app
###
###     @property
###     def session(self) -> t.Any:
###         """
###         Return Flask session
###         """
###         return flask.session
###
###     @property
###     def request(self) -> t.Any:
###         """
###         Return Flask request
###         """
###         return flask.request
###
###     @staticmethod
###     def redirect(location, code=302) -> t.Any:
###         """
###         Redirect with a 302 Found
###         """
###         return flask.redirect(location, code=code)
###
###     @staticmethod
###     def make_response(*args) -> t.Any:
###         """
###         Create a Flask response object
###         """
###         return flask.make_response(
###             *args,
###         )
###
###     @staticmethod
###     def render_template(template_name_or_list, **context):
###         return flask.render_template(template_name_or_list, **context)
###
###
### @define(kw_only=True, slots=False)
### class BackendProperties(FlasketProperties, FlaskProperties, LoggerProperties):
###     def __post_init__(self) -> None:
###         # Register a route to always call before/after_app_request
###         self._flasket._register_fake_route(handler=self)
###
###     # pylint: disable=bad-staticmethod-argument
###     @staticmethod
###     def post_init(cls):
###         @functools.wraps(cls, updated=())
###         class Wrapper(cls):
###             def __attrs_post_init__(self):
###                 super().__attrs_post_init__()
###                 super().__post_init__()
###
###         return Wrapper
