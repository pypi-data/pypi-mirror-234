"""
Description
-----------

Main application. It handles returning the WSGI application,
but also returning the potential services it can connect to and use.

On the OpenAPI side, it handles merging multiple yaml files into a single
specification before loading it.

Classes
-------

Flasket
^^^^^^^

.. autoclass:: Flasket
  :show-inheritance:
  :members: baseurl, clients, config, current_app, debug, flask, backends, host,  make_response, port, redirect, render_template, request, rootpath, session, sitename,

"""
import logging
import os
import random
import string
import sys
import typing as t
import weakref

from flask import Flask, current_app
from flask import g as flask_g
from flask import request as current_request
from flask_gordon.ext.defaults import SERVER_LISTEN, SERVER_PORT
from flask_gordon.ext.defaults import make_config as make_settings
from flask_gordon.middleware import BeforeFirstCall, Dispatcher
from werkzeug.middleware.proxy_fix import ProxyFix as ProxyMiddleware

from flasket.middleware import GunicornApplication

from .backends import ApiBackend, DashBackend, StaticBackend
from .logger import Logger
from .properties import LoggerProperties

__all__: t.List[str] = [
    "Flasket",
]


class Flasket(
    Flask,
    LoggerProperties,
):
    def __init__(self, name):
        self._flasket = weakref.proxy(self)
        super().__init__(name)

        Logger.configure()
        self.logger.setLevel(logging.INFO)

        self._middleware = None
        self._wsgi_app = self.wsgi_app
        self._rootpath = os.path.dirname(__file__)

        # Backends loaded, and to load
        self._backends = {}
        self._backends_cls = [DashBackend, ApiBackend, StaticBackend]

        # Did we go through self.configure
        self._configured = False
        self.config["SETTINGS"] = make_settings()

    def _init_debug(self) -> None:
        """
        Set the class variables to the values that were passed on by configuration.
        If debug is on, set the logger level
        """
        debug = self.settings["server"].get("debug", False)
        if debug:
            self.logger.setLevel(logging.DEBUG)

    def _init_rootpath(self, rootpath: str) -> None:
        def add_to_syspath(path):
            if path not in sys.path:
                self.logger.info(f'Adding path "{path}" to sys.path to enable dynamic loading...')
                sys.path.insert(0, path)

        if not rootpath:
            rootpath = os.getcwd()

        # rootpath was probably passed by "__file__"
        if rootpath and os.path.isfile(rootpath):
            rootpath = os.path.dirname(rootpath)
        rootpath = os.path.abspath(rootpath)

        if not os.path.exists(rootpath) or not os.path.isdir(rootpath):
            self.logger.error(f'Root path directory "{rootpath}" does not exist.')
            sys.exit(1)
        self.logger.info(f'Using root path "{rootpath}" for dynamic loading.')

        add_to_syspath(rootpath)
        self._rootpath = rootpath

    def _init_middleware(self, middleware: str = None) -> None:
        # pylint: disable=attribute-defined-outside-init
        self._zmiddleware = middleware
        if middleware == "flask":
            return
        if middleware == "gunicorn":
            # FIXME: current_settings?
            self._middleware = GunicornApplication(self, self.config["SETTINGS"])
            return
        raise ValueError("unknown middleware")

    def _init_defaults(self) -> None:
        # Configuration comes from several locations:
        # - the command line arguments,
        # - the configuration file
        # - defaults
        #
        # Flask is also very flexible to where settings can come from.
        #
        # The most important variables, mostly to start/pre-configure the service
        # have already been set
        #
        # Set some new defaults
        self.config["JSON_SORT_KEYS"] = False
        self.config["TEMPLATES_AUTO_RELOAD"] = not self.settings["server"].get("production")
        self.config["EXPLAIN_TEMPLATE_LOADING"] = os.getenv("EXPLAIN_TEMPLATE_LOADING")
        self.config["UNIQUE_KEY"] = "".join(random.choice(string.ascii_lowercase) for i in range(6))

    # FIXME: flask / server?
    def _init_config(self) -> None:
        server = self.settings.get("flask") or {}
        for key, _ in self.config.items():
            lkey = key.lower()
            if lkey in server:
                self.config[key] = server[lkey]

    # FIXME: Move to flask-gordon
    def _init_secret(self) -> None:
        # Handle the secret session key if missing
        secret_key = self.config["SECRET_KEY"]
        if not secret_key:
            self.config["SECRET_KEY"] = "".join(random.choices(string.ascii_letters, k=20))
            self.logger.warning("Generated a random secret session key.")

    def _init_backends(self, options) -> None:
        # Load all backends
        # For every backend get option[name] for that backend
        options = options or {}
        for cls in self._backends_cls:  # pylint: disable=not-an-iterable
            cls_options = options.get(cls.name()) or {}
            self.logger.info(f"Initializing {cls.name()} backend...")
            backend = cls.init_app(flasket=weakref.proxy(self), rootpath=self._rootpath, options=cls_options)
            self._backends[backend.prefix] = backend

    def _init_wsgi_apps(self) -> None:
        # Queue the middlewares
        middleware = self.wsgi_app
        middleware = Dispatcher(self._backends["/"], self._backends)
        proxy = self.settings["server"].get("proxy", {})
        # Quick and dirty
        # pylint: disable=too-many-boolean-expressions
        if proxy and (
            int(proxy.get("x_for", 0))
            or int(proxy.get("x_proto", 0))
            or int(proxy.get("x_host", 0))
            or int(proxy.get("x_port", 0))
            or int(proxy.get("x_prefix", 0))
        ):
            middleware = ProxyMiddleware(middleware, **proxy)
        middleware = BeforeFirstCall(middleware, self._before_first_call)
        self.wsgi_app = middleware

    def configure(
        self,
        rootpath: str,
        middleware: str = None,
        options=None,
    ):
        assert self._configured is False, "You can only run 'Flasket.configure' once"
        self._configured = True

        self.logger.info("Configuring Flasket application...")

        self._init_debug()
        self._init_rootpath(rootpath)
        self._init_middleware(middleware)
        self._init_defaults()
        self._init_config()
        self._init_secret()

        # https://flask.palletsprojects.com/en/2.2.x/config/
        # Values from _init_defaults could have been overloaded
        # by _init_config
        self.config["DEBUG"] = self.settings["server"].get("debug", False)

        self._init_backends(options)
        self._init_wsgi_apps()
        return self

    # pylint: disable=arguments-differ
    def run(self):
        if not self._configured:
            self.configure(__file__)

        if self._middleware is None:
            # FIXME: current_settings?
            host = self.config["SETTINGS"]["server"].get("listen", SERVER_LISTEN)
            port = self.config["SETTINGS"]["server"].get("port", SERVER_PORT)
            debug = self.config["SETTINGS"]["server"].get("debug", False)
            super().run(host=host, port=port, debug=debug, load_dotenv=False, use_reloader=False)
        else:
            self._middleware.run()

    def _register_backend(self, backend):
        # Copy all flask config to backend config
        for key, value in self.config.items():
            # blacklist some keys
            try:
                # pylint: disable=protected-access
                backend._flask.config[key] = value
            except AttributeError:
                continue

        # And add 'flasket' to Flask app, so it's available via current_app
        # pylint: disable=protected-access
        backend._flask.flasket = weakref.proxy(self)
        backend._flask.before_request(Flasket._before_request)
        backend._flask.after_request(Flasket._after_request)

    # --------------------------------------------------------------------------
    @staticmethod
    def _before_first_call() -> None:
        Logger.disable()

    @staticmethod
    def _before_request() -> None:
        # Inject some variables available to templates
        flasket = current_app.flasket
        flask_g.flasket = flasket

    @staticmethod
    def _after_request(response) -> None:
        # Log the request
        Logger.log_request(current_request, response)
        return response

    # --------------------------------------------------------------------------
    def route(self, *args, **kwargs):
        raise NotImplementedError('to "flasket.route" is not implemented. Use "add_url_rule" instead.')

    # --------------------------------------------------------------------------
    @property
    def user_options(self, *args) -> None:
        """
        Network post on which Flasket is listening on.
        """
        raise NotImplementedError('Incorrect application, try appending ".celery"')

    @property
    def logger(self) -> logging.Logger:
        """
        Return a :class:`logging.Logger` named ``stderr``
        """
        return logging.getLogger("stderr")

    @property
    def settings(self) -> t.Dict[str, t.Any]:
        """
        Return Flasket settings used at start
        """
        # FIXME: current_settings?
        return self.config.get("SETTINGS") or {}

    @property
    def rootpath(self) -> str:
        """
        Return rootpath
        """
        return self._rootpath

    @property
    def host(self) -> str:
        """
        Network hosts on which Flasket is listening on.
        """
        return self.settings["server"].get("listen", SERVER_LISTEN)

    @property
    def port(self) -> int:
        """
        Network post on which Flasket is listening on.
        """
        return self.settings["server"].get("port", 8080)

    @property
    def sitename(self) -> str:
        """
        Return combination of network host and port
        """
        if self.port == 80:
            return f"http://{self.host}"
        return f"http://{self.host}:{self.port}"

    @property
    def baseurl(self) -> str:
        """
        Returns baseurl "{scheme}://{netloc}"
        """
        baseurl = self.settings["server"].get("baseurl", None)
        if baseurl:
            return baseurl
        return self.sitename

    @property
    def backends(self) -> t.Dict[str, "Backend"]:
        """
        Returns array of backends
        """
        return self._backends

    @property
    def production(self) -> bool:
        """
        Returns production status. Not equivalent to `not debug`
        """
        return self.settings["server"].get("production", False)
