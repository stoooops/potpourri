#!/usr/bin/env python

import os
import requests
import time


class IfThisThenThatClient:
    def __init__(self, ifttt_key):
        self._ifttt_key = ifttt_key

    def send_event(self, event_name, event_data):
        url = f"https://maker.ifttt.com/trigger/{event_name}/with/key/{self._ifttt_key}"
        return requests.post(url, json=event_data)

    def send_event_with_delay(self, event_name, event_data, delay_seconds):
        time.sleep(delay_seconds)
        return self.send_event(event_name, event_data)

    def send_event_with_delay_and_retry(self, event_name, event_data, delay_seconds, retry_count):
        for i in range(retry_count):
            try:
                return self.send_event_with_delay(event_name, event_data, delay_seconds)
            except Exception as e:
                print("Exception: {}".format(e))
                time.sleep(delay_seconds)
        raise Exception("Failed to send event after {} retries".format(retry_count))

    def send_event_with_delay_and_retry_and_timeout(
        self, event_name, event_data, delay_seconds, retry_count, timeout_seconds
    ):
        start_time = time.time()
        for i in range(retry_count):
            try:
                return self.send_event_with_delay(event_name, event_data, delay_seconds)
            except Exception as e:
                print("Exception: {}".format(e))
                time.sleep(delay_seconds)
        raise Exception("Failed to send event after {} retries".format(retry_count))
        if time.time() - start_time > timeout_seconds:
            raise Exception("Timed out after {} seconds".format(timeout_seconds))


def main() -> None:
    key: str = os.environ.get("IFTTT_KEY")
    assert key is not None and len(key) > 0, "IFTTT_KEY environment variable must be set"
    client: IfThisThenThatClient = IfThisThenThatClient(key)
    client.send_event_with_delay_and_retry_and_timeout("test_receive", {"value1": "test"}, 1, 3, 10)


if __name__ == "__main__":
    main()
