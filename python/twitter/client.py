import json
import time
from logging import getLogger
from typing import Optional

import tweepy

LOG = getLogger(__name__)

MAX_RETRIES = 3


class TwitterClient:
    """
    A basic client for Twitter
    """

    def __init__(
        self,
        consumer_key: str,
        consumer_secret: str,
        access_token: str,
        access_secret: str,
    ) -> None:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)

        self._api = tweepy.API(auth)

        try:
            self._api.verify_credentials()
            LOG.info("Authentication OK")
        except Exception:
            LOG.error("Error during authentication")

    def tweet(self, s: str, media_filepath: Optional[str] = None) -> bool:
        attempt = 0
        while attempt < MAX_RETRIES:
            try:
                if media_filepath is None:
                    self._api.update_status(s)
                else:
                    self._api.update_with_media(media_filepath, s)

                return True
            except tweepy.error.TweepError as e:
                LOG.error("Tweet failed.")
                LOG.exception(e)
            attempt += 1
            time.sleep(attempt ** 2)

        return False

    def delete_all(self) -> None:
        for status in tweepy.Cursor(self._api.user_timeline).items():
            self._api.destroy_status(status.id)
            LOG.info(f"Deleted tweet {status.id}")


def make_twitter_client(secrets_json_filepath: str) -> TwitterClient:
    with open(secrets_json_filepath, "r") as f:
        content = json.loads(f.read())

        return TwitterClient(
            consumer_key=content["consumer_key"],
            consumer_secret=content["consumer_secret"],
            access_token=content["access_token"],
            access_secret=content["access_secret"],
        )
