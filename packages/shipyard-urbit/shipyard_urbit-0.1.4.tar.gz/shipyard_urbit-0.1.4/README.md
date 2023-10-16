# Shipyard

Urbit hosting and automation platform.

Note: this is a Pre-Release package.  All changes will be breaking.  Wait for release 1.0.0 or later.

## Install

```
pip install shipyard-urbit
```

## Usage

```
shipyard
```

To use the application locally, run `shipyard api` and visit `localhost:8000`.

For multi-user production deploymenrs, or any other custom configuration, use `shipyard gunicorn` passing Gunicorn server options ([Reference](https://docs.gunicorn.org/en/stable/settings.html)).  Omit the `wsgi_app` argument and `worker_class` option as these are preconfigured by shipyard.

## Configuration

Specify the following environment vars to configure your application.  You may use a `.env` file in the location where `shipyard` is run.

- `SHIPYARD_DATA_DIR` - directory where SQLite database and other data will live, default: `~/.shipyard/`
    -  Override at runtime using the `--data-dir` option. Global command line options must come before the application command, example: `shipyard --data-dir=mydir api`
- `SHIPYARD_SQLITE_FILENAME` - name of the db file within the data directory, default: `shipyard.db`
- `SHIPYARD_POSTGRES_URL` - PostgreSQL connection string to override use of SQLite, default: `None`

PostgreSQL is only recommended for large multi-user deployments. You must create your database before connecting with shipyard like so:

```
CREATE DATABASE shipyard;
```

Then `SHIPYARD_POSTGRES_URL` should look something like this:

```
postgresql://user:password@127.0.0.1:5432/shipyard
```

## API Overview

Visit [redacted] for full API Documentation.

## Development

### Modules

#### shipyard

 * `db.py` - database engine for SQLite/PostreSQL application state
 * `models.py` - types used throughout the project
 * `settings.py` - system-wide settings and env vars
 * `tasks.py` - for running background jobs or long running processes

#### shipyard.api

HTTP API built with FastAPI.

#### shipyard.cli

Command-line interface built with Typer.

#### shipyard.colony

Host setup and configuration using Ansible.

#### shipyard.deploy

Creating and migrating Urbit ships within our host infrastructure.

#### shipyard.envoy

Communication and direction of Urbit ships.

#### shipyard.vigil

Monitoring and alerting. WIP.

## License

This project is licensed under Apache-2.0.  Code licensed from other projects will be clearly marked with the appropriate notice.
