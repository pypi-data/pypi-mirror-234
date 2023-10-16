from contextlib import asynccontextmanager, contextmanager, AsyncExitStack
from contextvars import ContextVar, Token
from dataclasses import dataclass, KW_ONLY, field
from urllib.parse import urljoin
from typing import AsyncGenerator, ClassVar, Generator, Type, TypeVar

import httpx

from .exceptions import TgHttpStatusError, TgRuntimeError


AsyncTgClientType = TypeVar('AsyncTgClient', bound='AsyncTgClient')
SyncTgClientType = TypeVar('SyncTgClient', bound='SyncTgClient')


@dataclass(frozen=True)
class AsyncTgClient:
    token: str
    _: KW_ONLY
    session: httpx.AsyncClient
    tg_server_url: str = 'https://api.telegram.org'

    api_root: str = field(init=False)

    default_client: ClassVar[ContextVar['AsyncTgClient']] = ContextVar('default_client')

    def __post_init__(self):
        api_root = urljoin(self.tg_server_url, f'./bot{self.token}/')
        object.__setattr__(self, 'api_root', api_root)

    @classmethod
    @asynccontextmanager
    async def setup(
        cls: Type[AsyncTgClientType],
        token: str,
        *,
        session: httpx.AsyncClient | None = None,
        **client_kwargs,
    ) -> AsyncGenerator[AsyncTgClientType, None]:
        if not token:
            # Safety check for empty string or None to avoid confusing HTTP 404 error
            raise ValueError(f'Telegram token is empty: {token!r}')

        async with AsyncExitStack() as stack:
            if not session:
                session = await stack.enter_async_context(httpx.AsyncClient())

            client = cls(token=token, session=session, **client_kwargs)
            with client.set_as_default():
                yield client

    @contextmanager
    def set_as_default(self) -> Generator[None, None, None]:
        default_client_token: Token = self.default_client.set(self)
        try:
            yield
        finally:
            self.default_client.reset(default_client_token)


@dataclass(frozen=True)
class SyncTgClient:
    token: str
    _: KW_ONLY
    session: httpx.Client
    tg_server_url: str = 'https://api.telegram.org'

    api_root: str = field(init=False)

    default_client: ClassVar[ContextVar['SyncTgClient']] = ContextVar('default_client')

    def __post_init__(self):
        api_root = urljoin(self.tg_server_url, f'./bot{self.token}/')
        object.__setattr__(self, 'api_root', api_root)

    @classmethod
    @contextmanager
    def setup(
        cls: Type[SyncTgClientType],
        token: str,
        *,
        session: httpx.Client = None,
        **client_kwargs,
    ) -> Generator[SyncTgClientType, None, None]:
        if not token:
            # Safety check for empty string or None to avoid confusing HTTP 404 error
            raise ValueError(f'Telegram token is empty: {token!r}')

        if not session:
            session = httpx.Client()

        client = cls(token=token, session=session, **client_kwargs)
        with client.set_as_default():
            yield client

    @contextmanager
    def set_as_default(self) -> Generator[None, None, None]:
        default_client_token: Token = self.default_client.set(self)
        try:
            yield
        finally:
            self.default_client.reset(default_client_token)


def raise_for_tg_response_status(response: httpx.Response) -> None:
    """Raise the `TgHttpStatusError` if one occurred."""
    request = response._request

    if request is None:
        raise TgRuntimeError(
            "Cannot call `raise_for_status` as the request instance has not been set on this response.",
        )

    if response.is_success:
        return

    raise TgHttpStatusError(request=request, response=response)
