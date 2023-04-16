import logging
import typing

import reqsnaked
import web3
import web3.providers.async_base
import web3.types


class AllNodesAreDownError(Exception):
    def __init__(self, errors: typing.List[Exception]):
        self.errors = errors
        super().__init__()


class AsyncMultiProvider(web3.providers.async_base.AsyncJSONBaseProvider):
    logger = logging.getLogger(
        "web3_async_multi_provider.provider.AsyncMultiProvider"
    )

    def __init__(
        self,
        urls: typing.List[str],
        session: typing.Optional[reqsnaked.Client] = None,
        request_extra: typing.Optional[typing.Dict[str, typing.Any]] = None,
    ):
        self._urls = urls
        self._session = session or reqsnaked.Client()
        self._request_extra = request_extra or {}

        super().__init__()

    async def make_request(
        self, method: web3.types.RPCEndpoint, params: typing.Any
    ) -> web3.types.RPCResponse:
        happened_error = []
        for url in self._urls.copy():
            self.logger.debug(
                f"Making request HTTP. URI: {url}, Method: {method}"
            )
            request_data = self.encode_rpc_request(method, params)
            request = reqsnaked.Request(
                "POST",
                url=url,
                body=request_data,
                headers={"Content-Type": "application/json"},
            )
            try:
                response = await self._session.send(request)
                raw_response = await response.read()
                result_response = self.decode_rpc_response(
                    raw_response.as_bytes()
                )
            except Exception as err:
                self.logger.warning(f"Error occurred for URI: {url}: {err}")
                this_url = self._urls.pop(0)
                self._urls.append(this_url)
                happened_error.append(err)
            else:
                self.logger.debug(
                    f"Getting response HTTP. URI: {url}, "
                    f"Method: {method}, Response: {response}"
                )
                return result_response
        else:
            raise AllNodesAreDownError(happened_error)
