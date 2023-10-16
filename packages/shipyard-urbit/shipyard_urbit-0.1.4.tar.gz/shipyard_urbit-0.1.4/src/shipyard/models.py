from pathlib import Path
from typing import ClassVar, Optional
import logging

from pydantic import (
    AnyUrl,
    BaseModel,
    DirectoryPath,
    FileUrl,
    PostgresDsn,
    conint,
    constr,
    root_validator,
)
from sqlmodel import Field, SQLModel


class SshRemoteIn(BaseModel):
    host: constr(min_length=1)  # pyright:ignore
    user: constr(min_length=1)  # pyright:ignore
    port: Optional[int] = 22


class SshTunnelIn(SshRemoteIn):
    local_port: conint(gt=1024, lt=65536)  # pyright:ignore
    remote_port: conint(gt=0, lt=65536)  # pyright:ignore


class SshUrl(AnyUrl):
    allowed_schemes = {"ssh"}
    user_required = True


class SshRemote(BaseModel):
    url: SshUrl

    @classmethod
    def from_input(cls, ssh_in: SshRemoteIn):
        return SshRemote(
            url=f"ssh://{ssh_in.user}@{ssh_in.host}:{ssh_in.port}"  # pyright:ignore
        )


class SshTunnel(SshRemote):
    local_port: conint(gt=1024, lt=65536)  # pyright:ignore
    remote_port: conint(gt=0, lt=65536)  # pyright:ignore

    @classmethod
    def from_input(cls, ssh_in: SshTunnelIn):
        return SshTunnel(
            url=f"ssh://{ssh_in.user}@{ssh_in.host}:{ssh_in.port}",  # pyright:ignore
            remote_port=ssh_in.remote_port,
            local_port=ssh_in.local_port,
        )


class SqliteDsn(FileUrl):
    allowed_schemes = {"sqlite"}


class SqliteConn(BaseModel):
    dir: DirectoryPath
    file: Path
    url: SqliteDsn

    @classmethod
    def builder(cls, dir: DirectoryPath, file: Path):
        url: SqliteDsn = f"sqlite:///{dir}/{file}"  # pyright:ignore
        return SqliteConn(dir=dir, file=file, url=url)


class PostgresConn(BaseModel):
    url: PostgresDsn


class Host(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class Task(BaseModel):
    version: ClassVar[int]
    loggable: ClassVar[bool] = True

    def run(self):
        raise NotImplementedError("Cannot run generic task")

    @property
    def logger(self):
        return logging.getLogger(self.__class__.full_class_name())

    # ClassVar is not included in pydantic validation
    # https://docs.pydantic.dev/usage/models/#automatically-excluded-attributes
    @root_validator(pre=True)
    def validate_version(cls, _):
        if not cls.version or cls.version < 1:
            raise ValueError(
                "Task subclasses must specify a version number 1 or greater."
            )

    @classmethod
    def full_class_name(cls):
        return f"{cls.__module__}.{cls.__qualname__}"


class TaskLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    version: int

    @classmethod
    def fromTask(cls, task: Task):
        return TaskLog(
            version=task.__class__.version,
            full_name=task.__class__.full_class_name(),
        )
