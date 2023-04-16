import pytest
import web3
import web3.eth

from web3_async_multi_provider import AllNodesAreDownError, AsyncWSMultiProvider


@pytest.mark.skip
@pytest.mark.asyncio
async def test_multi_nodes():
    provider = AsyncWSMultiProvider(
        providers=[
            web3.providers.WebsocketProvider("wss://example.com/"),
            web3.providers.WebsocketProvider("wss://mainnet.infura.io/ws")
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
    provider = AsyncWSMultiProvider(
        providers=[
            web3.providers.WebsocketProvider("wss://example.com/"),
            web3.providers.WebsocketProvider("wss://google.com/"),
        ]
    )
    w3 = web3.Web3(
        provider,  # noqa
        modules={"eth": [web3.eth.AsyncEth]},
        middlewares=[]
    )
    with pytest.raises(AllNodesAreDownError):
        await w3.eth.chain_id  # noqa

