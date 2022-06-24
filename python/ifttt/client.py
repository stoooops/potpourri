#!/usr/bin/env python

from argparse import ArgumentParser, Namespace
import os
import requests
import time


class IfThisThenThatClient:
    def __init__(self, ifttt_key):
        self._ifttt_key = ifttt_key

    def send_event(self, event_name, event_data):
        url = f"https://maker.ifttt.com/trigger/{event_name}/with/key/{self._ifttt_key}"
        return requests.post(url, json=event_data)

    def send_event_with_delay(self, event_name, event_data, delay_sec):
        time.sleep(delay_sec)
        return self.send_event(event_name, event_data)

    def send_event_with_delay_and_retry(self, event_name, event_data, delay_sec: int, retries: int):
        for i in range(retries):
            try:
                return self.send_event_with_delay(event_name, event_data, delay_sec)
            except Exception as e:
                print("Exception: {}".format(e))
                time.sleep(delay_sec)
        raise Exception("Failed to send event after {} retries".format(retries))

    def send_event_with_delay_and_retry_and_timeout(
        self, event_name, event_data, delay_sec: int, retries: int, timeout_sec: int
    ):
        start_time = time.time()
        for i in range(retries):
            if time.time() - start_time > timeout_sec:
                raise Exception(f"Timed out after {timeout_sec} seconds")
            try:
                return self.send_event_with_delay(event_name, event_data, delay_sec=delay_sec)
            except Exception as e:
                print("Exception: {}".format(e))
                time.sleep(delay_sec)
        raise Exception("Failed to send event after {} retries".format(retries))


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "--key",
        type=str,
        default=os.environ.get("IFTTT_KEY"),
        help="IFTTT key",
    )
    parser.add_argument(
        "--event",
        type=str,
        required=True,
        help="IFTTT event name",
    )
    return parser.parse_args()


def main() -> None:
    args: Namespace = parse_args()
    client: IfThisThenThatClient = IfThisThenThatClient(args.key)
    client.send_event_with_delay_and_retry_and_timeout(
        event_name=args.event, event_data={}, delay_sec=1, retries=3, timeout_sec=10
    )


if __name__ == "__main__":
    main()
