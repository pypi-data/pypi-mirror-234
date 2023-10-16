# Mercoa Python Library

[![pypi](https://img.shields.io/pypi/v/mercoa.svg)](https://pypi.python.org/pypi/mercoa)
[![fern shield](https://img.shields.io/badge/%F0%9F%8C%BF-SDK%20generated%20by%20Fern-brightgreen)](https://github.com/fern-api/fern)

## Documentation

API reference documentation is available [here](https://docs.mercoa.com/api-reference/).

## Installation

Add this dependency to your project's build file:

```bash
pip install mercoa
# or
poetry add mercoa
```

## Usage

```python
from mercoa.client import Mercoa

mercoa_client = Mercoa(token="YOUR_API_KEY")

entity = mercoa_client.entity.get(entity_id='YOUR_ENTITY_ID')

print(entity)
```

## Async client

This SDK also includes an async client, which supports the `await` syntax:

```python
import asyncio
from mercoa.client import AsyncMercoa

mercoa_client = AsyncMercoa(token="YOUR_API_KEY")

async def get_entity() -> None:
    entity = await mercoa_client.entity.get(entity_id='YOUR_ENTITY_ID')
    print(entity)

asyncio.run(get_entity())
```

## Beta status

This SDK is in beta, and there may be breaking changes between versions without a major version update. Therefore, we recommend pinning the package version to a specific version in your lock file. This way, you can install the same version each time without breaking changes unless you are intentionally looking for the latest version.

## Contributing

While we value open-source contributions to this SDK, this library is generated programmatically. Additions made directly to this library would have to be moved over to our generation code, otherwise they would be overwritten upon the next generated release. Feel free to open a PR as a proof of concept, but know that we will not be able to merge it as-is. We suggest [opening an issue](https://github.com/mercoa-finance/python/issues) first to discuss with us!

On the other hand, contributions to the README are always very welcome!
