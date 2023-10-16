# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import threading as th
import typing as t
from logging import getLogger

import pytermor as pt

from .exception import DataCollectionError
from .threads import ThreadSafeCounter


class Requester:
    DEFAULT_TIMEOUT = 10
    HTTP_RESPONSE_FILTERS = [
        pt.StringLinearizer(),
    ]

    network_request_id = ThreadSafeCounter()

    def __init__(self, network_req_event: th.Event = None):
        self._network_req_event: th.Event = network_req_event or th.Event()

    def make_request(
        self,
        url: str,
        timeout: float = DEFAULT_TIMEOUT,
        request_fn: t.Callable[[], 'requests.Response'] = None,
        log_response_body: bool = True,
    ) -> 'requests.Response':
        import requests
        try:
            request_id = self.network_request_id.next()
            self._network_req_event.set()
            self._log_http_request(request_id, url)
            if not request_fn:
                request_fn = lambda: requests.get(url, timeout=timeout)
            response = request_fn()
            self._log_http_response(request_id, response, with_body=log_response_body)
        except requests.exceptions.ConnectionError as e:
            getLogger(__package__).error(e)
            raise DataCollectionError()
        except requests.RequestException as e:
            getLogger(__package__).exception(e)
            raise DataCollectionError()
        finally:
            self._network_req_event.clear()

        if not response.ok:
            getLogger(__package__).warning(f"Request failed: HTTP {response.status_code}")
            raise DataCollectionError()

        getLogger(__package__).debug("Remote service response:\n"+response.text)
        return response

    def _log_http_request(self, req_id: int | str, url: str, method: str = "GET"):
        getLogger(__package__).info(f"[#{req_id}] > {method} {url}")

    def _log_http_response(self, req_id: int | str, response: "requests.Response", with_body: bool):
        msg_resp = f"[#{req_id}] < HTTP {response.status_code}"
        msg_resp += ", " + pt.format_si(response.elapsed.total_seconds(), "s")
        msg_resp += ", " + pt.format_si_binary(len(response.text))
        if with_body:
            msg_resp += ': "'
            msg_resp += pt.apply_filters(response.text, *self.HTTP_RESPONSE_FILTERS)
            msg_resp += '"'
        getLogger(__package__).info(msg_resp)
