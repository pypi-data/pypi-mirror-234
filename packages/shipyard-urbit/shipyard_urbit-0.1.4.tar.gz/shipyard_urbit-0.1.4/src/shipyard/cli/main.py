import os
import platform
from rich import print
import typer

from shipyard.api.main import gunicorn_run, uvicorn_run
from shipyard.db import connect_database
from shipyard.envoy.tunnel import open_tunnel
from shipyard.models import SshTunnel
from shipyard.settings import DEFAULT_DATA_DIR, get_settings, load_settings


app = typer.Typer()


@app.callback(no_args_is_help=True)
def callback(
    data_dir: str = typer.Option(
        None,
        help="Directory containing the application database, will be created if necessary.",
        show_default=f"{DEFAULT_DATA_DIR}{os.sep}",  # pyright:ignore
    ),
):
    """
    Urbit hosting and automation platform

    Global options must be entered before a command.
    """
    if data_dir:
        os.environ["SHIPYARD_DATA_DIR"] = data_dir

    try:
        load_settings().ensure_data_dir()
    except OSError as e:
        print(f"Cannot access directory {get_settings().data_dir}{os.sep}")
        print(e)
        raise typer.Exit(1)

    connect_database()


@app.command()
def api(
    host: str = typer.Option("127.0.0.1", help="Host the server will listen on"),
    port: int = typer.Option("8000", help="Port the server will listen on"),
    log_level: str = typer.Option("info", help="Logging level of the server"),
    dev: bool = typer.Option(
        False, help="Run a dev server that reloads on code changes"
    ),
):
    """
    Run a local API server
    """
    uvicorn_run(host=host, port=port, log_level=log_level, workers=2, reload=dev)


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def gunicorn():
    """
    Run API in a custom Gunicorn app.

    Use for specialized deployments.  All command line options are passed
    directly to Gunicorn.

    Reference:
    https://docs.gunicorn.org/en/latest/settings.html
    """
    if platform.system() == "Windows":
        print("Gunicorn not supported on Windows")
        raise typer.Exit(1)
    else:
        gunicorn_run()


@app.command(no_args_is_help=True)
def tunnel(
    host: str = typer.Option(
        ..., "--host", "-h", help="Hostname of the remote SSH server"
    ),
    user: str = typer.Option(
        ..., "--user", "-u", help="Username to login to remote SSH server"
    ),
    port: int = typer.Option(
        22, "--port", "-p", help="Listening port of the remote SSH server"
    ),
    local_port: int = typer.Option(
        4000, "--local-port", "-L", help="Local port to forward application to"
    ),
    remote_port: int = typer.Option(
        4000, "--remote-port", "-R", help="Remote application port to forward"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Print additional status information"
    ),
):
    """
    Open an SSH tunnel to a remote ship, allowing you to connect on a local port
    """
    ssh: SshTunnel = SshTunnel(
        url=f"ssh://{user}@{host}:{port}",  # pyright:ignore
        local_port=local_port,
        remote_port=remote_port,
    )
    open_tunnel(ssh, verbose)
