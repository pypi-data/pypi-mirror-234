import argparse


def add_bot_arguments(parser: argparse.PARSER) -> None:
    parser.add_argument(
        "--bot",
        "-b",
        type=str,
        help="Name or token of the bot that will be used (required)."
    )
    parser.add_argument(
        "--token",
        "-t",
        action="store_true",
        help="Whether a token was passed. If not it is assumed that the bot name"
             " was passed."
    )
    parser.add_argument(
        "--bot-file",
        "-f",
        type=str,
        default="",
        help="Name of the csv file containing the token(s) of the bot(s)."
             "  Required if the bot name was passed"
    )


def add_chat_arguments(parser: argparse.PARSER) -> None:
    parser.add_argument(
        "--chat",
        "-c",
        type=str,
        help="Name or id of the chat where the info will be sent (required)."
    )
    parser.add_argument(
        "--id",
        "-i",
        action="store_true",
        help="Whether a chat id was passed. If not it is assumed that the chat name"
             " was passed."
    )
    parser.add_argument(
        "--chat-file",
        "-cf",
        type=str,
        default="",
        help="Name of the csv file containing the id(s) of the chat(s)."
             "  Required if the bot name was passed"
    )


def create_parser() -> argparse.PARSER:
    parser = argparse.ArgumentParser(description="Telegram Bot to send messages or documents")
    subparsers = parser.add_subparsers(
        dest="mode",
        help="Choose what you want to do with your bot.\nValid arguments are:"
             "message, photo, updates.",
        required=True
    )
    message_parser = subparsers.add_parser(
        "message",
        help="Send a message through telegram using a bot"
    )
    photo_parser = subparsers.add_parser(
        "photo",
        help="Send a message through telegram using a bot"
    )
    updates_parser = subparsers.add_parser(
        "updates",
        help="Get the latest updates of the bot from telegram"
    )

    for par in [message_parser, photo_parser, updates_parser]:
        add_bot_arguments(par)

    add_chat_arguments(message_parser)
    add_chat_arguments(photo_parser)

    message_parser.add_argument(
        "--message",
        "-m",
        type=str,
        help="Text of the message (required)."
    )

    photo_parser.add_argument(
        "--photo",
        "-p",
        type=str,
        help="Path to the photo file (required)."
    )
    photo_parser.add_argument(
        "--caption",
        "-cp",
        type=str,
        default="",
        help="A caption for the photo (optional)."
    )

    return parser
