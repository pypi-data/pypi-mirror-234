"""Types."""

from __future__ import annotations

import re
from datetime import datetime, timedelta
from enum import Enum, IntEnum
from random import random
from ssl import SSLContext
from time import sleep
from typing import Any, Callable, Iterator, Optional, TypeVar, Union, cast
from urllib.parse import unquote

import structlog
from asyncio_mqtt import Client as AsyncClient
from paho.mqtt.client import Client
from pydantic import AnyUrl, BaseConfig, StrictStr, UrlSchemeError
from pydantic.fields import ModelField
from pydantic.tools import parse_obj_as

logger = structlog.get_logger(__name__)


TimeType = Union[int, float, datetime, timedelta]

T = TypeVar("T")


class Identifier(StrictStr):
    """Dotted-identifier name."""

    regex = re.compile(r"^[a-zA-Z]\w*$")


class DNSName(StrictStr):
    """DNS-safe name."""

    regex = re.compile("^[a-z]([-a-z0-9]*[a-z0-9])?$")


class DottedName(StrictStr):
    """Dotted-identifier name."""

    regex = re.compile("^[a-z0-9]([-_.a-z0-9]*[a-z0-9])?$")


class MQTTUrl(AnyUrl):
    """MQTT URL."""

    allowed_schemes = {"mqtt", "mqtts"}

    _DEFAULT_PORTS = {"mqtt": "1883", "mqtts": "8883"}

    host: str

    @classmethod
    def validate(cls, value: Any, field: ModelField, config: BaseConfig) -> AnyUrl:
        """Validate URL."""

        try:
            result = super().validate(value, field, config)
        except UrlSchemeError:
            result = super().validate(f"mqtt://{value}", field, config)

        if result.port is None:
            result.port = cls._DEFAULT_PORTS[result.scheme]
            result = parse_obj_as(cls, cls.build(**{x: getattr(result, x) for x in cls.__slots__}))

        return result

    def get_sync_client(
        self,
        client_id: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        max_attempts: Optional[int] = None,
        min_interval: float = 1.0,
        max_interval: float = 32.0,
    ) -> Client:
        """Get synchronous client."""

        client = Client(client_id=client_id or "")

        if username is None and self.user:
            username = unquote(self.user)
        if password is None and self.password:
            password = unquote(self.password)

        if username:
            client.username_pw_set(username, password)

        if self.scheme == "mqtts":
            client.tls_set_context()

        host, port = self.host, int(cast(str, self.port))

        interval, i = 0.0, 0
        while True:
            i += 1
            try:
                client.connect(host, port)
            except Exception as e:
                if max_attempts is not None and i >= max_attempts:
                    raise ConnectionError(f"Unable to connect to broker: {e}")
                logger.info("Retrying connection", interval=interval, attempt=i)
                sleep(interval + random())  # nosec
                interval = min(max(2.0 * interval, min_interval), max_interval)
                continue
            else:
                break

        return client

    def get_async_client(
        self,
        client_id: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> AsyncClient:
        """Get asynchronous client."""

        if username is None and self.user:
            username = unquote(self.user)
        if password is None and self.password:
            password = unquote(self.password)

        return AsyncClient(
            hostname=self.host,
            port=int(cast(str, self.port)),
            client_id=client_id,
            username=username,
            password=password,
            tls_context=SSLContext() if self.scheme == "mqtts" else None,
        )


class QOS(IntEnum):
    """Quality-of-Service."""

    AT_MOST_ONCE = 0
    AT_LEAST_ONCE = 1
    EXACTLY_ONCE = 2

    @classmethod
    def __get_validators__(cls) -> Iterator[Callable[[Any, ModelField, BaseConfig], Any]]:
        """Get pydantic validators."""

        yield cls.validate

    @classmethod
    def validate(cls, value: Any, field: ModelField, config: BaseConfig) -> int:
        """Validate data."""

        if isinstance(value, int):
            return cls(value)
        elif not isinstance(value, str):
            raise TypeError(f"Invalid value {value!r}") from None

        try:
            return cls.__members__[value.upper()]
        except KeyError:
            raise ValueError(f"Invalid value {value!r}") from None


class EnumType(Enum):
    """Enum type."""

    @classmethod
    def __get_validators__(cls) -> Iterator[Callable[[Any, ModelField, BaseConfig], Any]]:
        """Get pydantic validators."""

        yield cls.validate

    @classmethod
    def validate(cls, value: Any, field: ModelField, config: BaseConfig) -> Any:
        """Validate data."""

        if isinstance(value, cls):
            return cls(value)
        elif not isinstance(value, str):
            raise TypeError(f"Invalid value {value!r}") from None

        try:
            return cls(value)
        except ValueError:
            raise ValueError(f"Invalid value {value!r}") from None


class Access(EnumType):
    """Access type."""

    RO = "RO"
    RW = "RW"
    WO = "WO"


class Storage(EnumType):
    """Storage type."""

    NONE = "none"
    NODE = "node"
    NODE_CLOUD = "node-and-cloud"
