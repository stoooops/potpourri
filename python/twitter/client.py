from logging import getLogger

import tweepy

LOG = getLogger(__name__)


class TwitterClient:
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
        except:
            LOG.error("Error during authentication")

    def tweet(self, s: str) -> None:
        self._api.update_status(s)

    def delete_all(self) -> None:
        for status in tweepy.Cursor(self._api.user_timeline).items():
            self._api.destroy_status(status.id)
            LOG.info(f"Deleted tweet {status.id}")
