from typing import List, Any

import time
import atexit

import httpx
import litellm


class Client:
    def __init__(self, project: str, api_key: str, api_base="TODO"):
        self.project = project
        self.api_key = api_key
        self.api_base = api_base

    def ingest(self, records: List[dict[str, Any]]):
        headers = {"Authorization": f"Bearer {self.api_key}"}

        with httpx.Client(headers=headers) as client:
            for record in records:
                data = {"project": self.project, "record": record}
                client.post(f"{self.api_base}/log", json=data)


class Handler:
    client: Client
    buffer: List[dict[str, Any]]
    last_run: float

    def __init__(
        self,
        client: Client,
        max_emit_interval=1,
    ):
        self.client = client
        self.last_run = time.monotonic()
        self.buffer = []
        self.max_emit_interval = max_emit_interval

        def success_callback(kwargs, completion_response, start_time, end_time):
            self._emit(
                {
                    "success": True,
                    "input": kwargs,
                    "output": completion_response,
                    "start_time": start_time,
                    "end_time": end_time,
                }
            )

        def failure_callback(kwargs, completion_response, start_time, end_time):
            self._emit(
                {
                    "success": False,
                    "input": kwargs,
                    "output": completion_response,
                    "start_time": start_time,
                    "end_time": end_time,
                }
            )

        litellm.success_callback = success_callback
        litellm.failure_callback = failure_callback
        atexit.register(self._flush)

    def completion(self, *args, **kwargs):
        """https://docs.litellm.ai/docs/completion/input"""
        return litellm.completion(*args, **kwargs)

    def _emit(self, record: dict[str, Any]):
        self.buffer.append(record)

        if (
            len(self.buffer) >= 1000
            or time.monotonic() - self.last_run > self.max_emit_interval
        ):
            self._flush()

    def _flush(self):
        self.last_run = time.monotonic()

        if len(self.buffer) == 0:
            return

        self.client.ingest(self.buffer)
        self.buffer = []
