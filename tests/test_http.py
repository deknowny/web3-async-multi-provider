import pytest
import web3
import web3.eth

from web3_async_multi_provider import AsyncHTTPMultiProvider, AllNodesAreDownError


@pytest.mark.asyncio
async def test_multi_nodes():
    provider = AsyncHTTPMultiProvider(
        providers=[
            web3.AsyncHTTPProvider("https://example.com/"),
            web3.AsyncHTTPProvider("https://eth.llamarpc.com"),
        ]
    )
    w3 = web3.Web3(
        provider,  # noqa
        modules={"eth": [web3.eth.AsyncEth]},
        middlewares=[]
    )
    assert (await w3.eth.chain_id) == 1  # noqa


@pytest.mark.asyncio
async def test_check_failed():
    provider = AsyncHTTPMultiProvider(
        providers=[
            web3.AsyncHTTPProvider("https://example.com/"),
            web3.AsyncHTTPProvider("https://google.com/"),
        ]
    )
    w3 = web3.Web3(
        provider,  # noqa
        modules={"eth": [web3.eth.AsyncEth]},
        middlewares=[]
    )
    with pytest.raises(AllNodesAreDownError):
        await w3.eth.chain_id  # noqa

