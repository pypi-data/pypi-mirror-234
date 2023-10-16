import uvicorn
from gunicorn.app.base import Application

from shipyard.tasks import with_task_runner


class ShipyardGunicorn(Application):
    """
    Custom Gunicorn Application that allows setting options
    programmatically, falling back to default Gunicorn configuration
    if no options provided.

    Loads the shipyard api using UvicornWorker by default.

    Example with config:
        ShipyardGunicorn(
            {"bind": f"{host}:{port}", "loglevel": log_level, "workers": 2}
        ).run()
    """

    def __init__(self, options, **kwargs):
        self.options = options
        super().__init__(**kwargs)

    def load(self):
        return "shipyard.api.app:app"

    def init(self, parser, opts, args):
        return {"worker_class": "uvicorn.workers.UvicornWorker"}

    def load_config(self):
        if not self.options:
            super().load_config()
        else:
            default = self.init(None, None, None)
            config = {**default, **self.options}
            for k, v in config.items():
                self.cfg.set(k, v) #pyright: ignore


@with_task_runner
def uvicorn_run(**kwargs):
    uvicorn.run("shipyard.api.app:spawn_app", factory=True, **kwargs)


@with_task_runner
def gunicorn_run():
    ShipyardGunicorn(None).run()
