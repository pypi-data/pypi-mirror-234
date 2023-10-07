import functools
import os

from flask import Blueprint, Flask, send_from_directory

from ._backend import Backend


class StaticBackend(Backend):
    @staticmethod
    def init_app(flasket, rootpath, options=None) -> "StaticBackend":
        return StaticBackend(flasket, rootpath, options)

    def __init__(self, flasket, rootpath, options=None):
        super().__init__(flasket, rootpath)

        self._init_rootpath()
        self._init_blueprint()
        self._init_redirect(options)
        self._flasket._register_backend(self)

    def _init_rootpath(self) -> None:
        rootpath = self._rootpath
        if os.path.exists(os.path.join(rootpath, "static")):
            filepath = os.path.join(rootpath, "static")
            self._basepath = filepath
            self.logger.info(f'Reading static files from "{self._basepath}" directory.')
        elif os.path.exists(os.path.join(rootpath, "htdocs")):
            filepath = os.path.join(rootpath, "htdocs")
            self._basepath = filepath
            self.logger.info(f'Reading static files from "{self._basepath}" directory.')
        else:
            self._basepath = "/non-existent"
            self.logger.warning("Neither 'static' nor 'htdocs' directories in root path exist.")

    def _init_blueprint(self):
        # Use None for static_folder to prevent adding a automatic "/<filename>" route
        self._flask = Flask(__name__, root_path=self._basepath, static_folder=None, template_folder=None)
        blueprint = Blueprint(
            "static",
            __name__,
            root_path=self._basepath,
            static_folder=None,
            template_folder=None,
        )
        blueprint.add_url_rule("/<path:path>", view_func=self.send_file)
        self._flask.register_blueprint(blueprint)

    def _init_redirect(self, options):
        redirect_to = options.get("redirect_to", "/app/")
        redirect_code = options.get("redirect_code", 308)
        redirect_fn = functools.partial(self._flask.redirect, location=redirect_to, code=redirect_code)
        redirect_fn.__name__ = "redirect"
        blueprint = Blueprint(
            "redirect",
            __name__,
            root_path=self._rootpath,
            static_folder=None,
            template_folder=None,
        )
        blueprint.add_url_rule("/", view_func=redirect_fn)
        self._flask.register_blueprint(blueprint)

    @staticmethod
    def name() -> str:
        return "static"

    @property
    def prefix(self) -> str:
        return "/"

    def send_file(self, path: str) -> object:
        return send_from_directory(path=path, directory=self._basepath)
