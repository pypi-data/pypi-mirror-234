import os
import typing as t

from boltons.fileutils import iter_find_files
from dash import Dash

from ._backend import Backend

dash = None


class DashBackend(Backend):
    _callbacks = []
    _registered_pages = []

    @staticmethod
    def init_app(flasket, rootpath, options=None) -> "DashBackend":
        return DashBackend(flasket, rootpath, options)

    @staticmethod
    def name() -> str:
        return "dash"

    @property
    def prefix(self) -> str:
        return "/app"

    @staticmethod
    def _prefix() -> str:
        return "/app"

    def __init__(self, flasket, rootpath, options=None):
        super().__init__(flasket, rootpath)

        self._init_rootpath(rootpath)
        self._init_dash(options)
        self._init_app_files()
        self._init_decorators()
        self._flasket._register_backend(self)
        self._configured = True

    def _init_rootpath(self, rootpath: str) -> None:
        rootpath = os.path.join(rootpath, "app")
        if not os.path.exists(rootpath):
            self.logger.warning('Directory "app" in root path does not exist.')
        self._rootpath = rootpath

    def _init_dash(self, options: t.Dict[str, t.Any]) -> None:
        # Some settings can't be used together
        use_pages = options.get("use_pages", False)
        if use_pages:
            pages_folder = options.get("pages", "")
        else:
            pages_folder = None

        # pylint: disable=global-statement
        global dash
        dash = Dash(
            __name__,
            # url_base_pathname="/app/",
            # requests_pathname_prefix="/app/",
            routes_pathname_prefix="/app/",
            #
            assets_external_path=options.get("assets_external_path"),
            assets_folder=options.get("assets_folder", "assets"),
            # assets_ignore='',
            assets_url_path=options.get("assets_url_path", "assets"),
            # background_callback_manager=None,
            # compress=None,
            # eager_loading=False,
            external_scripts=options.get("external_scripts"),
            external_stylesheets=options.get("external_stylesheets"),
            extra_hot_reload_paths=options.get("extra_hot_reload_paths"),
            include_assets_files=options.get("include_assets_files", True),
            # long_callback_manager=None,
            # meta_tags=None,
            pages_folder=pages_folder,
            plugins=options.get("plugins", []),
            prevent_initial_callbacks=options.get("prevent_initial_callbacks", False),
            # serve_locally=True,
            # server=True,
            # show_undo_redo=False,
            suppress_callback_exceptions=options.get("suppress_callback_exceptions", False),
            title=options.get("title", "Flasket"),
            update_title=options.get("update_title", ""),
            use_pages=use_pages,
        )

        # FIXME: disable=invalid-envvar-default
        # pylint: disable=invalid-envvar-default
        if options.get("debug", False):
            dash.enable_dev_tools(debug=True)

        # pylint: disable=invalid-envvar-default
        elif os.getenv("DASH_DEBUG", False):
            dash.enable_dev_tools(debug=True)

        self._flask = dash.server
        self.logger.info(f"Aplication is available at: {self.flasket.sitename}/app/")

    def _init_app_files(self) -> None:
        files = iter_find_files(self._rootpath, "*.py")
        files = sorted(set(files))

        # TODO: Load __init__.py only once.
        #
        # If only __init__.py exists, then load it. Otherwise,
        # do not load it as it will be automatically loaded.
        modules = []
        dirname = self._flasket.rootpath.split("/")[-1]
        for file in files:
            file = os.path.relpath(file, self._flasket.rootpath)
            # if os.path.basename(file) == "__init__.py":
            #     continue
            file = file[:-3]
            file = file.replace("/", ".")
            file = dirname + "." + file
            modules += [file]

        for module in modules:
            __import__(module, globals(), locals())

    def _init_decorators(self):
        # pylint: disable=unused-variable
        def callback_wrapper(cb_fn, cb_args, cb_kwargs):
            @self._dash.callback(*cb_args, **cb_kwargs)
            def wrapper(*args, **kwargs):
                print("Setting callback on saved dash app")
                return cb_fn(*args, **kwargs)

    def __call__(self, environ: dict, start_response):
        return self._flask(environ, start_response)
