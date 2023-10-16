import logging
import math
import time
from concurrent.futures import Future, ThreadPoolExecutor
from threading import Thread

from requests.exceptions import RequestException

from impaction_ai.api_client import APIClient
from impaction_ai.buffer_storage import BufferStorage
from impaction_ai.constants import (
    BUFFER_CONSUME_WAIT_TIME_MS,
    FLUSH_BATCH_SIZE,
    FLUSH_INTERVAL_MS,
)
from impaction_ai.exception import APIError


class Worker:
    def __init__(self, api_client: APIClient, logger: logging.Logger):
        self.api_client = api_client
        self.logger = logger
        self.api_pool = ThreadPoolExecutor(max_workers=1)

    def setup(self, buffer_storage: BufferStorage) -> None:
        self.buffer_storage = buffer_storage

    def start(self) -> None:
        self._running = True
        self._thread = Thread(target=self.consume_buffer, daemon=True)
        self._thread.start()

    def consume_buffer(self) -> None:
        while self._running:
            try:
                with self.buffer_storage.buffer_lock:
                    if self.buffer_storage.buffer_size == 0:
                        self.buffer_storage.not_empty_cv.wait(BUFFER_CONSUME_WAIT_TIME_MS / 1000)
                        continue
                    out = self.buffer_storage.pull(FLUSH_BATCH_SIZE)
                    future = self.api_pool.submit(self.api_client.send_events, out)
                    future.add_done_callback(self._handle_api_task_completion)
                    self.buffer_storage.not_empty_cv.wait(FLUSH_INTERVAL_MS / 1000)
            except Exception as e:
                self.logger.exception(e)

    def flush(self, timeout_seconds: int) -> None:
        start_time = time.time()
        try:
            with self.buffer_storage.buffer_lock:
                if self.buffer_storage.buffer_size == 0:
                    return
                out = self.buffer_storage.pull_all()
                chunks_len = math.ceil(len(out) / FLUSH_BATCH_SIZE)
                for i in range(chunks_len):
                    elapsed_time = time.time() - start_time
                    if elapsed_time > timeout_seconds:
                        self.logger.warning(
                            f"Flush operation timed out after sending {i * chunks_len}/{len(out)} events"
                        )
                        break
                    self.api_client.send_events(out[i * FLUSH_BATCH_SIZE : (i + 1) * FLUSH_BATCH_SIZE])
        except APIError as e:
            self.logger.exception(e)
        except RequestException as e:
            self.logger.exception(e)
        except Exception as e:
            self.logger.exception(e)

    def stop(self, timeout_seconds: int) -> None:
        self._running = False
        self._thread.join()
        self.flush(timeout_seconds)

    def _handle_api_task_completion(self, future: Future) -> None:
        try:
            future.result()
        except APIError as e:
            self.logger.exception(e)
        except RequestException as e:
            self.logger.exception(e)
        except Exception as e:
            self.logger.exception(e)
