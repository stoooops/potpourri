import json
import os
from argparse import ArgumentParser, Namespace
from typing import List

import tweepy

from python.twitter.client import TwitterClient, make_twitter_client

filedir: str = os.path.dirname(os.path.abspath(__file__))

# tweets should be written to a file in the following syntax:
"""
## @foo

foo text

## @bar

@foo bar reply

## @foo

@bar foo reply back

## @baz

@foo @bar baz joins the conversation
"""


def format_conversation(tweet: tweepy.Status, parents: List[tweepy.Status], replies: List[tweepy.Status]) -> str:
    conversation: str = ""

    # format parents
    for parent in parents:
        conversation += f"## @{parent.user.screen_name}\n\n{parent.text}\n"

    # format tweet
    conversation += f"\n## @{tweet.user.screen_name}\n\n{tweet.text}\n"

    # format replies
    for reply in replies:
        conversation += f"\n## @{reply.user.screen_name}\n\n@{tweet.user.screen_name} {reply.text}\n"

    return conversation


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "--secrets",
        type=str,
        default=os.path.join(filedir, "secret.json"),
        help="Path to JSON file containing Twitter API secrets",
    )
    # output file
    parser.add_argument(
        "--output",
        type=str,
        default=os.path.join(filedir, "conversation.md"),
        help="Path to output file",
    )
    # url is positional argument
    parser.add_argument("url", type=str, help="URL of tweet to retrieve conversation")
    return parser.parse_args()


def main() -> None:
    args: Namespace = parse_args()

    client: TwitterClient = make_twitter_client(args.secrets)

    # Split tweet URL to get tweet ID
    tweet_id: str = args.url.split("/")[-1] if "/" in args.url else args.url

    # Get tweet object
    tweet: tweepy.Status = client.get_status(tweet_id)

    # get parent tweets
    parents: list[tweepy.Status] = client.api.statuses_lookup([tweet.in_reply_to_status_id_str])

    # get replies
    replies: list[tweepy.Status] = client.api.search(q=f"to:{tweet.user.screen_name}", since_id=tweet.id)

    conversation: str = format_conversation(tweet, parents, replies=[])

    # Write conversation to file
    with open(args.output, "w") as f:
        f.write(conversation)

    # log to console
    print(conversation)


if __name__ == "__main__":
    main()
