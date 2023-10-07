from ..properties import LoggerProperties


class Backend(LoggerProperties):
    """
    A backend holds a flask and a flasket
    """

    def __init__(self, flasket, rootpath):
        self._flask = None
        self._flasket = flasket
        self._rootpath = rootpath

    def __call__(self, environ: dict, start_response):
        # pylint: disable=not-callable
        return self._flask(environ, start_response)

    @property
    def flasket(self) -> "Flasket":
        """
        Return Flasket weak reference.
        """
        return self._flasket
