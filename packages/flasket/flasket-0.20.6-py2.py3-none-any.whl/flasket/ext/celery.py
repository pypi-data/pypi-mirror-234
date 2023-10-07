from celery import Celery as BaseCelery

from ..properties import LoggerProperties


class Celery(BaseCelery, LoggerProperties):
    def __init__(self, app: "Flasket" = None):
        self.logger.info("Initializing Celery extension...")

        self._app = app
        if app is None:
            name = __name__
        else:
            name = app.name

        super().__init__(name, include=[f"{name}.tasks"])

        if app is not None:
            self.init_app(app=app)

    def init_app(self, app: "Flasket" = None):
        self.logger.info("Configuring Celery extension...")
        if app is not None:
            self._app = app

        # Delayed configuration does not work:
        #   self.add_defaults(self._configure)
        #   return self
        #
        # def _configure(self):
        self._app.config["broker_url"] = self._app.settings["celery"]["broker_url"]
        self._app.config["result_backend"] = self._app.settings["celery"]["result_backend"]
        self.conf.update(self._app.config)
        return self
