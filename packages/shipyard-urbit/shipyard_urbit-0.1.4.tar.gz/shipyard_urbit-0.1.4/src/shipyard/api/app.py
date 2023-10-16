from shipyard.settings import load_settings
from .v1.app import app as v1

app = v1


def spawn_app():
    load_settings().ensure_data_dir()
    # database engine
    return app
