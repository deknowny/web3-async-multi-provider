import logging
import typing

import web3.providers.async_base
import web3.types


class AllNodesAreDownError(Exception):
    def __init__(self, errors: typing.List[Exception]):
        self.errors = errors
        super().__init__()


class AsyncHTTPMultiProvider(web3.providers.async_base.AsyncJSONBaseProvider):
    logger = logging.getLogger(
        "web3_async_multi_provider.provider.AsyncHTTPMultiProvider"
    )

    def __init__(
        self,
        providers: typing.List[web3.providers.async_base.AsyncBaseProvider],
    ):
        self._providers = providers
        super().__init__()

    async def make_request(
        self, method: web3.types.RPCEndpoint, params: typing.Any
    ) -> web3.types.RPCResponse:
        happened_error = []
        for provider in self._providers.copy():
            self.logger.debug(
                f"Making request HTTP. Provider: {provider}, Method: {method}"
            )
            try:
                result_response = await provider.make_request(method, params)
            except Exception as err:
                self.logger.warning(
                    f"Error occurred for Provider: {provider}: {err}"
                )
                this_url = self._providers.pop(0)
                self._providers.append(this_url)
                happened_error.append(err)
            else:
                self.logger.debug(
                    f"Getting response HTTP. Provider: {provider}, "
                    f"Method: {method}, Response: {result_response}"
                )
                return result_response
        else:
            raise AllNodesAreDownError(happened_error)


class AsyncWSMultiProvider(web3.providers.async_base.AsyncJSONBaseProvider):
    logger = logging.getLogger(
        "web3_async_multi_provider.provider.AsyncWSMultiProvider"
    )

    def __init__(
        self, providers: typing.List[web3.providers.WebsocketProvider]
    ):
        self._providers = providers
        super().__init__()

    async def make_request(
        self, method: web3.types.RPCEndpoint, params: typing.Any
    ) -> web3.types.RPCResponse:
        happened_error = []
        for provider in self._providers.copy():
            self.logger.debug(
                f"Making request HTTP. Provider: {provider}, Method: {method}"
            )
            request_data = self.encode_rpc_request(method, params)
            try:
                result_response = await provider.coro_make_request(
                    request_data
                )
            except Exception as err:
                self.logger.warning(
                    f"Error occurred for URI: {provider}: {err}"
                )
                this_provider = self._providers.pop(0)
                self._providers.append(this_provider)
                happened_error.append(err)
            else:
                self.logger.debug(
                    f"Getting response HTTP. URI: {provider}, "
                    f"Method: {method}, Response: {result_response}"
                )
                return result_response
        else:
            raise AllNodesAreDownError(happened_error)
