import collections
import os
import sys
import traceback
import typing as t
from copy import deepcopy

import yaml
from boltons.fileutils import iter_find_files
from connexion import FlaskApp
from connexion.exceptions import InvalidSpecification

from .._utils import deepmerge
from ._backend import Backend


def _load_yamlfiles(files: t.List[str]) -> t.Dict:
    """
    For every yaml file, load the file and merge with previous

    Parameters
    ----------
    files: List[str]
        list of files to parse and merge

    Returns
    -------
    dict:
        merged dictionary
    """
    try:
        data = {}
        for file in files:
            with open(file, encoding="UTF-8") as fd:
                newdata = yaml.safe_load(fd)
            if newdata:
                data = deepmerge(data, newdata)
        return data
    except yaml.scanner.ScannerError as err:
        raise type(err)(
            f"yaml scanner error: {err.problem} in '{err.problem_mark.name}', at line {err.problem_mark.line}",
        ) from None
    except yaml.parser.ParserError as err:
        raise type(err)(
            f"yaml parser error: {err.problem} in '{err.problem_mark.name}', at line {err.problem_mark.line}",
        ) from None
    except Exception as err:
        raise type(err)(f"{str(err)} in file {file}") from None


def _find_yamlfiles(paths: t.List[str], logger: object) -> collections.OrderedDict:
    """
    Find all yaml files in paths, returns a merged dict

    Parameters
    ----------
    paths: List[str]
        list of paths to search

    Returns
    -------
    dict:
        merged dictionary
    """
    # Make paths unique but keep order
    paths = list(dict.fromkeys(paths))

    # Merge all yml files from the directory
    files = []
    for path in paths:
        if os.path.exists(path):
            if logger:
                logger.info(f'Reading OpenAPI files from "{path}"...')
            files.extend(iter_find_files(path, ["*.yml", "*.yaml"]))

    # Load the contents
    data = _load_yamlfiles(files)

    # sort the keys in /components/schemas, since the UI uses that order
    data["components"]["schemas"] = collections.OrderedDict(
        sorted((data["components"]["schemas"]).items(), key=lambda s: s[0].lower()),
    )
    data["paths"] = collections.OrderedDict(
        sorted((data["paths"]).items(), key=lambda s: s[0].lower()),
    )
    return data


def _remove_path_if_key(specs: t.Dict, key: str, value: str) -> t.Dict:
    """
    For every API path in specs, remove it if we find specs[...][key] = value

    Parameters
    ----------
    specs: Dict
        OpenAPI specs

    key: str
        Key to look for

    value: str
        Value to look for

    Returns
    -------
    dict:
        OpenAPI specs without the removed keys
    """
    rv = deepcopy(specs)
    for path in specs.get("paths", {}).keys():
        for method in specs["paths"][path].keys():
            if key not in specs["paths"][path][method]:
                continue
            if specs["paths"][path][method][key] == value:
                del rv["paths"][path][method]
    return rv


class ApiBackend(Backend):
    @staticmethod
    def init_app(flasket, rootpath, options=None) -> "ApiBackend":
        return ApiBackend(flasket, rootpath, options)

    def __init__(self, flasket, rootpath, _options=None):
        super().__init__(flasket, rootpath)

        self._specs = None

        self._init_rootpath()
        self._init_specs()
        self._init_connexion()
        self._flasket._register_backend(self)

    def _init_rootpath(self) -> None:
        self._rootpath = os.path.join(self._rootpath, "api")
        if not os.path.exists(self._rootpath):
            self.logger.warning('Directory "api" in root path does not exist.')

    def _init_specs(self) -> None:
        # Build specs from yml files, and remove debug endpoints
        # TODO: Move to flask-gordon
        specpath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../api"))
        searchpath = [specpath, self._rootpath]
        specs = _find_yamlfiles(searchpath, self.logger)
        # Don't get flask.debug, but settings debug
        # TODO: Move to flask-gordon
        # if not self.flasket.settings["server"].get("debug", False):
        # pylint: disable=protected-access
        if self._flasket._zmiddleware != "flask":
            self.logger.info("Removing API debug endpoints.")
            specs = _remove_path_if_key(specs, "x-debug", True)
        else:
            self.logger.warning("Keeping API debug endpoints.")
        self._specs = specs

    def _init_connexion(self) -> None:
        # https://connexion.readthedocs.io/en/latest/
        self._connexion = FlaskApp(__name__, specification_dir="api")
        enable_ui = (self.flasket.settings["server"].get("ui", True),)
        try:
            self._connexion.add_api(
                self._specs,
                strict_validation=True,
                validate_responses=True,
                options={
                    "openapi_spec_path": "/api/openapi.json",
                    "swagger_url": "/api/ui",
                    "swagger_ui": enable_ui,
                    "swagger_spec": enable_ui,
                    # Quick hate to override connexion.apis.flask_api._spec_for_prefix basepath.
                    # In a normal configuration, it will default to '/api', but concatenate with
                    # another '/api' resulting in '/api/api' and the ApiApiFix that was onced added
                    # below.
                    "swagger_ui_basepath": "/",
                    # https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/
                    "swagger_ui_config": {
                        "displayOperationId": False,
                        "showCommonExtensions": False,
                        "tryItOutEnabled": True,
                    },
                },
            )
            self._flask = self._connexion.app

        except InvalidSpecification as err:
            raise type(err)(f"OpenAPI specification error: {err.message}") from None
        except Exception:
            # TODO: improve on this (raise as import error for example)
            print(traceback.print_exc(), file=sys.stderr)
            raise

        if enable_ui:
            self.logger.info(f"Swagger UI is available at: {self.flasket.sitename}/api/ui")
        else:
            self.logger.info("Swagger UI not started")

    @staticmethod
    def name() -> str:
        return "api"

    @property
    def prefix(self) -> str:
        return "/api"
