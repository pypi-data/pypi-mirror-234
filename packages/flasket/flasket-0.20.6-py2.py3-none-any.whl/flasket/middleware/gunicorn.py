import logging
import multiprocessing
import typing as t

from flask.logging import default_handler
from gunicorn.app.base import BaseApplication
from torxtools.pathtools import expandpath

__all__: t.List[str] = [
    "GunicornApplication",
]


class GunicornApplication(BaseApplication):  # type: ignore[misc]
    # .venv/lib/python3.9/site-packages/gunicorn/app/base.py
    """
    Gunicorn WSGI application class
    """

    @staticmethod
    def _get_cpu_workers(workers: int) -> int:
        """
        Return the number of workers gunicorn should start with.
        Impose a max limit to avoid overloading the host.

        Parameters
        ----------
        workers: int

            number of workers configured

        Returns
        -------
        int
        """
        if workers > 0:
            return workers

        # Do not overload the host with a default value too large
        # if it's a container, it could report host cpus
        cpus = max((multiprocessing.cpu_count() * 2), 1)
        if workers == 0:
            return min(cpus, 8)
        return cpus

    # pylint: disable=abstract-method
    # http://docs.gunicorn.org/en/stable/custom.html
    def __init__(
        self,
        flasket,
        cfg: t.Dict[str, t.Any],
    ) -> None:
        """
        Initialize a Flasket application, and configure Gunicorn

        Parameters
        ----------
        cfg: dict

            dictionary containing configuration for the application
        """
        self._flasket = flasket
        # Rework the configuration
        cfg = cfg["server"]
        cfg["workers"] = self._get_cpu_workers(cfg.get("workers", 0))
        self.options = {
            "bind": cfg.get("listen", "localhost") + ":" + str(cfg.get("port", 8080)),
            "pidfile": expandpath(cfg.get("pidfile")),
            "workers": cfg["workers"],
            "accesslog": "/dev/null",
            "errorlog": "/dev/null",
        }

        flasket.logger.info(f"Starting {cfg['workers']} workers...")
        super().__init__()

        # Use the Flask logger to log identically between flask and gunicorn
        # We have to specify a null FileStream handler, we'll remove it on first call
        # by using the _gunicorn identifier
        logger = logging.getLogger("gunicorn.error")
        default_handler._gunicorn = False
        logger.addHandler(default_handler)

    def init(self, parser: t.Any, opts: t.Any, args: t.Any) -> None:
        """
        Overloaded abstract method.
        """
        raise NotImplementedError

    def load_config(self) -> None:
        """
        Overloaded abstract method.

        Load Gunicorn configuration ourselves.
        """
        # Pass the configuration down to gunicorn.app.base.BaseApplication
        cfg = {k: v for k, v in self.options.items() if k in self.cfg.settings and v is not None}
        for k, v in cfg.items():
            self.cfg.set(k.lower(), v)

    def load(self) -> "Flasket":
        """
        Overloaded abstract method.

        Return a callable __call__ WSGI application
        """
        return self._flasket
