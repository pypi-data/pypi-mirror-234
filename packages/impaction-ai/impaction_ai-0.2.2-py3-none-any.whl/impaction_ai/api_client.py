from __future__ import annotations

import time
import uuid
from urllib.parse import urljoin

import requests
from requests.exceptions import RequestException

from impaction_ai.constants import API_MAX_RETIRES
from impaction_ai.exception import APIError
from impaction_ai.ingestion.v1alpha.event_pb2 import Event
from impaction_ai.ingestion.v1alpha.ingestion_pb2 import CollectEventsRequest


class APIClient:
    def __init__(self, api_host: str, api_key: str):
        self.endpoint = urljoin(api_host, "/ingestion.v1alpha.IngestionService/CollectEvents")
        self.api_key = api_key

    def send_events(self, events: list[Event]) -> None:
        pb_payload = CollectEventsRequest(request_id=uuid.uuid4().hex, events=events)
        payload = pb_payload.SerializeToString()
        for attempt in range(API_MAX_RETIRES):
            try:
                resp = requests.post(
                    url=self.endpoint,
                    data=payload,
                    headers={"Content-Type": "application/proto", "Authorization": f"Bearer {self.api_key}"},
                    timeout=10,
                )
                status_code = resp.status_code
                if status_code == 200:
                    return
                else:
                    raise APIError(status_code=status_code, err_msg=resp.text)
            except (RequestException, APIError) as e:
                if isinstance(e, APIError) and (400 <= e.status_code < 500) and e.status_code != 429:
                    raise
                if attempt < API_MAX_RETIRES - 1:
                    time.sleep(2**attempt)  # exponential back-off
                    continue
                else:
                    raise
