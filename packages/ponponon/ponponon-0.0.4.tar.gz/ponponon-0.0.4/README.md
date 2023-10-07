# ponponon

## Introduce

ponponon(pon) an advanced message queue framework, derived from [nameko](https://github.com/nameko/nameko)

⭐️ 🌟 ✨ ⚡️ ☄️ 💥

## Installation

Package is uploaded on PyPI.

You can install it with pip:

```shell
pip install ponponon
```

## Requirements

Python -- one of the following:

- CPython : 3.8 and newer ✅
- PyPy : Software compatibility not yet tested ❓

## Features

- Support for concurrent processes: eventlet, gevent
- Support amqp protocol
- Support for http protocol
- Support for grpc protocol
- Support typing hints, like Fastapi

## Documentation

📄 Intensified preparation in progress

## Example

### Create it

```python
from typing import Optional
from loguru import logger
from pon.events.entrance import event_handler


class DNACreateService:
    name = 'dna_create_service'

    @event_handler(source_service='ye', event_name='take')
    def auth(self, src_dna: str, content_type: Optional[str] = None) -> None:
        logger.debug(f'src_dna: {src_dna}')

    @event_handler(source_service='ye', event_name='to_decode')
    def decode(self, src_dna: str) -> None:
        logger.debug(f'src_dna: {src_dna}')


class SampleSearchService:
    name = 'sample_search_service'

    @event_handler(source_service='ye', event_name='take')
    def search(self, url: str) -> None:
        logger.debug(f'url: {url}')
```

### Run it

```shell
pon run --config config.yaml services
```

### Check it

## Resources

![](https://www.rabbitmq.com/img/logo-rabbitmq.svg)

## License

pon is released under the MIT License. See LICENSE for more information.
