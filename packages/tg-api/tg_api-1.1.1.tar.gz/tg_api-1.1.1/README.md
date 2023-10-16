# Tg API

![PyPI - Downloads](https://img.shields.io/pypi/dm/tg_api)
![PyPI - License](https://img.shields.io/pypi/l/tg_api)

Библиотека Tg API упрощает работу с веб-API Telegram. Она предоставляет тонкую обёртку над веб API Telegram и библиотекой [HTTPX](https://www.python-httpx.org/). Библиотека Tg API добавляет к HTTPX схемы данных и удобные часто используемые функции, но не мешает, при необходимости, спускаться ниже на уровень HTTP-запросов.

Ключевые возможности библиотеки Tg API:

- Поддержка синхронных и асинхронных запросов к API
- Shortcuts для часто используемых запросов
- Лёгкий доступ к боту из любого места в коде
- Наглядные схемы данных для всех типов запросов и ответов API
- Аннотация типов для удобства работы с IDE
- Простое низкоуровневое API для кастомизации запросов к API
- Набор инструментов для удобной работы с исключениями

Документация: [https://tg-api.readthedocs.io/en/latest/](https://tg-api.readthedocs.io/en/latest/)

## Содержимое

1. [Ключевые концепции](#key-conceptions)
1. [Примеры использования](#usage-examples)
    1. [Синхронное API](#usage-examples-sync)
    1. [Асинхронное API](#usage-examples-async)
    1. [Низкоуровневое API](#usage-examples-low-level)
1. [Документация по API](#docs)
1. [Как развернуть local-окружение](#local-setup)
1. [Как вести разработку](#development)
    1. [Как обновить local-окружение](#update-local-env)
    1. [Как установить python-пакет в образ с Django](#add-python-package-to-django-image)
    1. [Как запустить линтеры Python](#run-python-linters)
    1. [Как запустить тесты](#run-tests)
    1. [Как собрать документацию Sphinx](#build-docs)

<a name="key-conceptions"></a>
## Ключевые концепции

Библиотека Tg API предлагает несколько необычных концепций для работы с API. Пробежимся по ним вкратце.

**No God Object**. Библиотека не предоставляет пользователю никакого аналога "god object" для работы с API, как то `TgBot` или `TgApi`. В других библиотеках часто можно увидеть подобный код:

```py
bot = TgBot(token=...)
bot.send_message(text='Hello world!', chat_id=43)
```

Такой подход прекрасно выглядит в туториалах, он кажется простым и естественным, но ему сильно не хватает гибкости. При интенсивном использовании и кастомизации вы неизбежно столкнётесь с нехваткой документации, неожиданными ограничениями ПО и вам придётся лезть в код библиотеки, чтобы решить свою проблему. Подробно типичные проблемы такого подхода описаны в антипаттерне [God object](https://ru.wikipedia.org/wiki/%D0%91%D0%BE%D0%B6%D0%B5%D1%81%D1%82%D0%B2%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9_%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82).

В библиотеке Tg API нет и не будет аналога объекта `Bot`. Вместо него для отправки запросов используются объекты `SendMessageRequest`, `SendPhotoRequest` и подобные Request-объекты, по одному для каждому API endpoint из [документации Telegram](here https://core.telegram.org/bots/api). Сначала вы готовите запрос к API, затем отправляете и обрабатываете результат. Пример:

```py
# создаём объект запроса, но ещё не отправляем
tg_request = SendMessageRequest(text='Hello world!', chat_id=43)
# отправляем запрос в API
# вызов метода поднимет исключение TgRuntimeError если сервере Telegram ответит HTTP статусом != 2xx
tg_response: SendMessageResponse = tg_request.send()
```

Преимущество такого подхода в том, что он не создаёт лишних обёрток над схемой запроса и ответа к API. Вам не нужно искать документацию по методу `send_message`, не нужно мириться с ограничениями этого метода. Вы сможете отправлять в API даже запросы с крайне нетипичными параметрами, и полная схема доступных параметров у вас всегда под рукой.

**Default configuration**. Вам не нужен прямой доступ к объекту `TgBot`, `TgApi` или `TgClient` для работы с API. Обычно приходится таскать подобный объект за собой из функции в функцию, чтобы где-то там глубоко внутри отправить пользователю сообщение в Tg. Библиотека `Tg API` использует `contextvars`, чтобы передавать настройки подключения неявно. Пример:


```py
def do_something():
    # Function send message without direct access to TgClient object
    tg_request = SendMessageRequest(text='Hello world!', chat_id=43)
    tg_request.send()


def main(token: str) -> None:
    with TgClient.setup(token):
        do_something()
```

<a name="usage-examples"></a>
## Примеры использования

<a name="usage-examples-sync"></a>
### Синхронное API

Пример отправки пользователю текстового сообщения:

```py
from tg_api import SyncTgClient, SendMessageRequest


with SyncTgClient.setup(token):
    tg_request = SendMessageRequest(chat_id=tg_chat_id, text='Message proofs high level usage.')
    tg_request.send()
```

Пример удаления у пользователя любого сообщения по идентификатору сообщения:

```py
from tg_api import SyncTgClient, DeleteMessageRequest


with SyncTgClient.setup(token):
    tg_request = DeleteMessageRequest(chat_id=tg_chat_id, message_id=message_id)
    tg_request.send()
```


Пример изменения у пользователя текста любого сообщения по идентификатору сообщения:

```py
from tg_api import SyncTgClient, EditMessageTextRequest


with SyncTgClient.setup(token):
    tg_request = EditMessageTextRequest(chat_id=tg_chat_id, message_id=message_id, text='edited text')
    tg_request.send()
```

Пример изменения у пользователя заголовка сообщения по идентификатору сообщения:

```py
from tg_api import SyncTgClient, EditMessageCaptionRequest


with SyncTgClient.setup(token):
    tg_request = EditMessageCaptionRequest(chat_id=chat_id, message_id=message_id, caption='edited caption')
    tg_request.send()
```

Пример изменения у пользователя фото в сообщении по URL по идентификатору сообщения:

```py
from tg_api import SyncTgClient, EditUrlMessageMediaRequest


with SyncTgClient.setup(token):
    media = InputMediaUrlDocument(
        media='https://link_to_photo.jpg',
        caption='caption'
    )
    tg_request = EditUrlMessageMediaRequest(chat_id=chat_id, message_id=message_id, media=media)
    tg_request.send()
```


Пример изменения у пользователя документа в сообщении чтением документента из файла по идентификатору сообщения:

```py
from tg_api import SyncTgClient, EditBytesMessageMediaRequest, InputMediaBytesDocument


with SyncTgClient.setup(token):
    with open('path_to_document.pdf', 'rb') as f:
        media_content = f.read()
    media = InputMediaBytesDocument(
        media='attach://attachement.pdf',
        media_content=media_content,
        caption='caption'
    )
    tg_request = EditBytesMessageMediaRequest(chat_id=chat_id, message_id=message_id, media=media)
    tg_request.send()
```


Пример изменения у пользователя клавиатуры любого сообщения по идентификатору сообщения:

```py
from tg_api import SyncTgClient, InlineKeyboardButton, InlineKeyboardMarkup


keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='button_1', callback_data='test'),
            InlineKeyboardButton(text='button_2', callback_data='test'),
        ],
    ],
)

with SyncTgClient.setup(token):
    tg_request = EditMessageReplyMarkupRequest(chat_id=tg_chat_id, message_id=message_id, reply_markup=keyboard)
    tg_request.send()
```

Пример отправки пользователю сообщения с клавиатурой:
```py
from tg_api import (
    SyncTgClient,
    SendMessageRequest,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def main(token: str, chat_id: int) -> None:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='button_1', callback_data='test'),
                InlineKeyboardButton(text='button_2', callback_data='test'),
            ],
        ],
    )
    with SyncTgClient.setup(token):
        tg_request = SendMessageRequest(
            chat_id=chat_id,
            text='Message proofs keyboard support.',
            reply_markup=keyboard,
        )
        tg_request.send()
```

Пример отправки пользователю фото из файловой системы:
```py
from tg_api import SyncTgClient, SendBytesPhotoRequest

def main():
    with SyncTgClient.setup(token):
        with open(photo_filename, 'rb') as f:
            photo_content = f.read()
        tg_request = SendBytesPhotoRequest(chat_id=chat_id, photo=photo_content, filename=photo_filename)
        tg_request.send()
```


Пример отправки пользователю фото по URL:
```py
from tg_api import SyncTgClient, SendUrlPhotoRequest

def main():
    with SyncTgClient.setup(token):
        tg_request = SendUrlPhotoRequest(chat_id=chat_id, photo=photo_url, filename=photo_filename)
        tg_request.send()
```

Пример отправки пользователю документа из файловой системы:
```py
from tg_api import SyncTgClient, SendBytesDocumentRequest

def main():
    with SyncTgClient.setup(token):
        with open(document_filename, 'rb') as f:
            document_content = f.read()
        tg_request = SendBytesDocumentRequest(chat_id=chat_id, document=document_content, filename=document_filename)
        tg_request.send()
```


Пример отправки пользователю документа по URL:
```py
from tg_api import SyncTgClient, SendUrlDocumentRequest

def main():
    with SyncTgClient.setup(token):
        tg_request = SendUrlDocumentRequest(chat_id=chat_id, document=document_url, filename=document_filename)
        tg_request.send()
```

<a name="usage-examples-async"></a>
### Асинхронное API

Пример отправки пользователю текстового сообщения:

```py
from tg_api import AsyncTgClient, SendMessageRequest


async with AsyncTgClient.setup(token):
    tg_request = SendMessageRequest(chat_id=chat_id, text='Message proofs high level API usage.')
    # вызов метода поднимет исключение TgRuntimeError если сервере Telegram ответит HTTP статусом != 2xx
    await tg_request.asend()
```

Пример удаления у пользователя любого сообщения по идентификатору сообщения:

```py
from tg_api import AsyncTgClient, DeleteMessageRequest


async with AsyncTgClient.setup(token):
    tg_request = DeleteMessageRequest(chat_id=chat_id, message_id=message_id)
    await tg_request.asend()
```

Пример изменения у пользователя текста любого сообщения по идентификатору сообщения:

```py
from tg_api import AsyncTgClient, EditMessageTextRequest


async with AsyncTgClient.setup(token):
    tg_request = EditMessageTextRequest(chat_id=chat_id, message_id=message_id, text='edited text')
    await tg_request.asend()
```


Пример изменения у пользователя фото в сообщении по URL по идентификатору сообщения:

```py
from tg_api import AsyncTgClient, EditUrlMessageMediaRequest


async with AsyncTgClient.setup(token):
    media = InputMediaUrlDocument(
        media='https://link_to_photo.jpg',
        caption='caption'
    )
    tg_request = EditUrlMessageMediaRequest(chat_id=chat_id, message_id=message_id, media=media)
    await tg_request.asend()
```


Пример изменения у пользователя документа в сообщении чтением документента из файла по идентификатору сообщения:

```py
from tg_api import AsyncTgClient, EditBytesMessageMediaRequest, InputMediaBytesDocument


async with AsyncTgClient.setup(token):
    with open('path_to_document.pdf', 'rb') as f:
        media_content = f.read()
    media = InputMediaBytesDocument(
        media='attach://attachement.pdf',
        media_content=media_content,
        caption='caption'
    )
    tg_request = EditBytesMessageMediaRequest(chat_id=chat_id, message_id=message_id, media=media)
    await tg_request.asend()
```


Пример изменения у пользователя клавиатуры любого сообщения по идентификатору сообщения:

```py
from tg_api import AsyncTgClient, InlineKeyboardButton, InlineKeyboardMarkup


keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='button_1', callback_data='test'),
            InlineKeyboardButton(text='button_2', callback_data='test'),
        ],
    ],
)

async with AsyncTgClient.setup(token):
    tg_request = EditMessageReplyMarkupRequest(chat_id=chat_id, message_id=message_id, reply_markup=keyboard)
    await tg_request.asend()
```

Пример изменения у пользователя заголовка сообщения по идентификатору сообщения:

```py
from tg_api import AsyncTgClient, EditMessageCaptionRequest


async with AsyncTgClient.setup(token):
    tg_request = EditMessageCaptionRequest(chat_id=chat_id, message_id=message_id, caption='edited caption')
    await tg_request.asend()
```

Пример отправки пользователю сообщения с клавиатурой:

```py
from tg_api import (
    AsyncTgClient,
    SendMessageRequest,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


async def main(token: str, chat_id: int) -> None:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='button_1', callback_data='test'),
                InlineKeyboardButton(text='button_2', callback_data='test'),
            ],
        ],
    )
    async with AsyncTgClient.setup(token):
        tg_request = SendMessageRequest(
            chat_id=chat_id,
            text='Message proofs keyboard support.',
            reply_markup=keyboard,
        )
        await tg_request.asend()
```


Пример отправки пользователю фото из файловой системы:
```py
import aiofiles

import tg_api


async def main(token: str, chat_id: int, photo_filename: str) -> None:
    async with tg_api.AsyncTgClient.setup(token):
        async with aiofiles.open(photo_filename, 'rb') as f:
            photo_content = await f.read()
        tg_request = tg_api.SendBytesPhotoRequest(chat_id=chat_id, photo=photo_content, filename=photo_filename)
        await tg_request.asend()
```


Пример отправки пользователю фото по URL:
```py
import tg_api


async def main(token: str, chat_id: int, photo_filename: str, photo_url: str) -> None:
    async with tg_api.AsyncTgClient.setup(token):
        tg_request = tg_api.SendUrlPhotoRequest(chat_id=chat_id, photo=photo_url, filename=photo_filename)
        await tg_request.asend()
```

Пример отправки пользователю документа из файловой системы:
```py
import aiofiles

import tg_api


async def main(token: str, chat_id: int, document_filename: str) -> None:
    async with tg_api.AsyncTgClient.setup(token):
        async with aiofiles.open(document_filename, 'rb') as f:
            document_content = await f.read()
        tg_request = tg_api.SendBytesDocumentRequest(chat_id=chat_id, document=document_content, filename=document_filename)
        await tg_request.asend()
```


Пример отправки пользователю документа по URL:
```py
import tg_api


async def main(token: str, chat_id: int, document_filename: str, document_url: str) -> None:
    async with tg_api.AsyncTgClient.setup(token):
        tg_request = tg_api.SendUrlDocumentRequest(chat_id=chat_id, document=document_url, filename=document_filename)
        await tg_request.asend()
```

<a name="usage-examples-low-level"></a>
### Низкоуровневое API

Низкоуровневое API позволяет использовать все самые свежие возможности [Telegram Bot API](https://core.telegram.org/bots/api), даже если их поддежку ещё не успели завезти
в библиотеку tg_api. Можно добавлять свои типы запросов и ответов API, менять способ отправки HTTP-запросов и реакции на ответ.

Пример использования низкоуровневого асинхронного API:

```py
from httpx import Response as HttpResponse
from tg_api import AsyncTgClient, SendMessageRequest, SendMessageResponse, raise_for_tg_response_status


async def main(token: str, chat_id: int) -> None:
    async with AsyncTgClient.setup(token) as tg_client:
        tg_request = SendMessageRequest(chat_id=chat_id, text='Message proofs low level API usage.')
        json_bytes = tg_request.json(exclude_none=True).encode('utf-8')

        http_response: HttpResponse = await tg_client.session.post(
            f'{tg_client.api_root}sendMessage',
            headers={'content-type': 'application/json'},
            content=json_bytes,
        )
        # поднимет исключение TgRuntimeError если сервере Telegram ответит HTTP статусом != 2xx
        raise_for_tg_response_status(http_response)

        tg_response = SendMessageResponse.parse_raw(http_response.content)
        print('Id нового сообщения:', tg_response.result.message_id)
```

<a name="docs"></a>
## Документация по API

- [tg_methods.py](./tg_methods.py) -- схемы запросов к API и ответов
- [tg_types.py](./tg_methods.py) -- библиотека типов данных, с которыми работает Tg API


<a name="local-setup"></a>
## Как развернуть local-окружение

Для запуска ПО вам понадобятся консольный Git, Docker и Docker Compose. Инструкции по их установке ищите на официальных сайтах:

- [Install Docker Desktop](https://www.docker.com/get-started/)
- [Install Docker Compose](https://docs.docker.com/compose/install/)

Склонируйте репозиторий.

В репозитории используются хуки pre-commit, чтобы автоматически запускать линтеры и автотесты. Перед началом разработки установите [pre-commit package manager](https://pre-commit.com/).

В корне репозитория запустите команду для настройки хуков:

```shell
$ pre-commit install
```

В последующем при коммите автоматически будут запускаться линтеры и автотесты. Есть линтеры будет недовольны, или автотесты сломаются, то коммит прервётся с ошибкой.

Перед запуском Docker Compose в корне репозитория создайте файл `.env` со следующими переменными:

``` bash
# Replace numbers with id values of your system user.
# Run command `id` in terminal to figure out actual id values.
UID=1000
GID=1000
```
Скачайте и соберите докер-образы с помощью Docker Сompose:

```shell
$ docker compose pull --ignore-buildable
$ docker compose build
```

В репозиторий добавлен Makefile, который поможет упростить и/или автоматизировать часть рутинных команд в процессе разработки
Для того чтобы посмотреть список доступных команд введите:

``
make help
``

Вы получите похожий вывод
```
Available targets:
build                          Собирает докер-образ
up                             Запускает докер-контейнер
clean                          Очищает все volume в соответствии с docker-compose
linter                         Запускает python линтеры
test                           Запускает python-тесты
help                           Отображает список доступных целей и их описания
build-docs                     Запускает сборку документации Sphinx
```

<a name="development"></a>
## Как вести разработку

<a name="update-local-env"></a>
### Как обновить local-окружение

Чтобы обновить local-окружение до последней версии подтяните код из центрального окружения и пересоберите докер-образы:

``` shell
$ git pull
$ docker compose build
```

<a name="add-python-package-to-django-image"></a>
### Как установить python-пакет в образ

В качестве менеджера пакетов для образа используется [Poetry](https://python-poetry.org/docs/).

Конфигурационные файлы Poetry `pyproject.toml` и `poetry.lock` проброшены в контейнер в виде volume, поэтому изменения зависимостей внутри контейнера попадают и наружу в git-репозиторий.

Вот пример как добавить в зависимости библиотеку asks. Запустите все контейнеры. Подключитесь к уже работающему контейнеру `tg-api` и внутри запустите команду `poetry add asks`. Затем выйдите из контейнера и остановить работу контейнеров:

```shell
$ docker compose up -d
$ docker compose exec tg-api bash
container:$ poetry add asks
container:$ exit
$ docker compose down
```

Конфигурационные файлы `pyproject.toml` и `poetry.lock` обновятся не только внутри контейнера, но и в репозитории благодаря настроенным docker volumes. Осталось только закоммитить изменения.

Чтобы все новые контейнеры также получали свежий набор зависимостей не забудьте обновить докер-образ:

```shell
$ docker compose build tg-api
```

Аналогичным образом можно удалять python-пакеты.

<a name="run-python-linters"></a>
### Как запустить линтеры Python

Линтеры запускаются в отдельном docker-контейнере, а код подключается к нему с помощью volume. Например, чтобы проверить линтером код в каталогах `tg_api` и `tests` запустите команду:

```shell
$ docker compose run --rm py-linters flake8 /tg_api/ /tests/
[+] Building 0.0s (0/0)
[+] Building 0.0s (0/0)
/tg_api/client.py:23:121: E501 line too long (148 > 120 characters)
1
```
Цифра в конце `1` -- это количество найденных линтером ошибок форматирования кода.

Того же результата можно добиться с помощью make:

```shell
$ make linter
...
```

Тот же образ с линтером можно использовать, чтобы подсветить ошибки форматирования прямо внутри IDE. Вот пример настройки Sublime Text с предустановленными плагинами [SublimeLinter](http://www.sublimelinter.com/en/stable/) и [SublimeLinter-flake8](https://packagecontrol.io/packages/SublimeLinter-flake8):

```jsonc
// project settings file
{
    "settings": {
        // specify folder where docker-compose.yaml file placed to be able to launch `docker compose`
        "SublimeLinter.linters.flake8.working_dir": "/path/to/repo/",
        "SublimeLinter.linters.flake8.executable": ["docker", "compose", "run", "--rm", "py-linters", "flake8"],
    },
}
```

<a name="run-tests"></a>
### Как запустить тесты

В репозитории используются автотесты [pytest](https://docs.pytest.org/). Запустить их можно так:

```shell
$ docker compose run --rm tg-api pytest
=========================== test session starts ===========================
platform linux -- Python 3.11.4, pytest-7.3.2, pluggy-1.2.0
cachedir: /pytest_cache_dir
rootdir: /opt/app
configfile: pyproject.toml
plugins: httpx-0.22.0, anyio-3.7.0
collected 6 items

test_asend.py ..                                                                                                       [ 33%]
test_types.py ....                                                                                                     [100%]

============================================================= 6 passed in 0.22s==============================================
```

Того же результата можно добиться с помощью make:

```shell
$ make test
...
```

Если вы чините поломанный тест, часто его запускаете и не хотите ждать когда отработают остальные, то можно запускать их по-отдельности. При этом полезно включать опцию `-s`, чтобы pytest не перехватывал вывод в консоль и выводил все сообщения. Пример для теста `test_update_parsing` из файла `tests/test_types.py`:

```shell
$ docker compose run --rm tg-api pytest -s test_asend.py::test_httpx_mocking
```

Подробнее про [Pytest usage](https://docs.pytest.org/en/6.2.x/usage.html).

<a name="build-docs"></a>
### Как собрать документацию Sphinx

Документация в репозитории собирается с помощью Sphinx и публикуется на ReadTheDocs. Этот сервис сам скачивает репозиторий и запускает сборку на своих серверах. Для публикации свежей версии документации достаточно изменить код в main-ветке центрального репозитория, зайти в личный кабинет ReadTheDocs и нажать кнопку.

Новую сборку документации можно проверить на своей машине ещё до публикации на ReadTheDocs и до коммита. Sphinx со всеми зависимостями установлен в отладочный докер-образ. Запустить сборку можно командой:

```shell
$ docker compose run --rm tg-api bash -c "cd sphinx_docs; make html"
...
build succeeded.

The HTML pages are in build/html.
```

Того же результата можно добиться с помощью make:

```shell
$ make build-docs
...
```

В результате сборки в репозиториии появится набор HTML-файлов в каталоге `sphinx_docs/build/index.html`. Индексный HTML лежит в файле `sphinx_docs/build/index.html` — откройте его в браузере.
