# Web3 async multi provider
> Web3.py compatible async providers that supports multiply RPC URLs
This library allows to create a `w3` instance with multiply RPC URLs to prevent failures when a node is down by choosing another one by cycle.

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/web3_async_multi_provider)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/web3_async_multi_provider)
![PyPI](https://img.shields.io/pypi/v/web3_async_multi_provider)
[![Coverage Status](https://coveralls.io/repos/github/deknowny/web3-async-multi-provider/badge.svg?branch=main)](https://coveralls.io/github/deknowny/web3-async-multi-provider?branch=main)
***

# Features
* HTTP async provider
* WebSockets async provider
## Overview
HTTP w3 provider
```python
provider = AsyncHTTPMultiProvider(
    providers=[
        web3.AsyncHTTPProvider("https://eth.llamarpc.com"),
        web3.AsyncHTTPProvider("https://rpc.flashbots.net"),
    ]
)
```

WebSockets provider
```python
import web3
from web3_async_multi_provider import AsyncWSMultiProvider

provider = AsyncWSMultiProvider(
    providers=[
        web3.providers.WebsocketProvider("wss://example.com/"),
        web3.providers.WebsocketProvider("wss://google.com/"),
    ]
)
```

And then add it into `Web3`:
```python
w3 = web3.Web3(
    provider
    modules={"eth": [web3.eth.AsyncEth]},
    middlewares=[]
)
print(await web3.eth.chain_id)
```

# Installation
Via PyPI:
```shell
python -m pip install web3_async_multi_provider
```
Or via GitHub
```shell
python -m pip install https://github.com/deknowny/web3-async-multi-provider/archive/main.zip
```
# Contributing
Check out [site Contributing section](https://deknowny.github.io/web3-async-multi-provider/latest/contributing/)
