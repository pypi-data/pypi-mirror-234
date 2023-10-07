import os
import pprint
import sys
from typing import Union

from telegrambot.bot import TestBot, TelegramBot


def validate_file(name: str, verify: bool) -> bool:
    if verify:
        return os.path.isfile(name)
    return True


def read_token_file(file: str, bot_name: str) -> str:
    with open(file) as fp:
        for line in fp.readlines():
            name, token = line.split(",")
            if name == bot_name:
                return token.strip()
    return ""


def get_bot(name: str, is_token: bool, file: str) -> Union[TestBot, TelegramBot, None]:
    token = name
    if not is_token:
        token = read_token_file(file, name)

    if not token:
        return

    bot_type = os.environ.get("bot", "telegram")
    if bot_type == "telegram":
        return TelegramBot(token)
    return TestBot(token)


def get_chat_id(
        chat_name: str, file: str = "", is_id: bool = False, bot_name: str = ""
) -> str:
    if not is_id:
        with open(file) as fp:
            for line in fp.readlines():
                chat, chat_id, bot = line.split(",")
                bot = bot.strip()
                if chat == chat_name:
                    if bot_name == bot or not bot_name:
                        return chat_id
        # The chat was not found
        return ""
    return chat_name


def find_file_or_exit(file: str, verify: bool) -> None:
    if not validate_file(file, verify):
        print(f"Could not find file {file}")
        sys.exit(1)


def send_message(
        bot: str,
        is_token: bool,
        bot_file: str,
        chat: str,
        is_id: bool,
        chat_file: str,
        message: str,
) -> None:
    find_file_or_exit(bot_file, is_token)
    find_file_or_exit(chat_file, is_id)

    telegram_bot = get_bot(bot, is_token, bot_file)
    bot_name = bot if not is_token else ""
    chat_id = get_chat_id(chat, is_id, chat_file, bot_name)
    if not chat_id:
        print(f"Failed to find chat id of {chat}")
        sys.exit(1)

    success, status_code, message = telegram_bot.send_message(message, chat_id)
    if not success:
        print(f"Failed to send message. Status code {status_code}")
        sys.exit(1)

    print(f"Message sent successfully: {message}")


def send_photo(
        bot: str,
        is_token: bool,
        bot_file: str,
        chat: str,
        is_id: bool,
        chat_file: str,
        photo_path: str,
        caption: str = ""
) -> None:
    find_file_or_exit(bot_file, is_token)
    find_file_or_exit(chat_file, is_id)
    find_file_or_exit(photo_path, True)

    telegram_bot = get_bot(bot, is_token, bot_file)
    bot_name = bot if not is_token else ""
    chat_id = get_chat_id(chat, is_id, chat_file, bot_name)
    if not chat_id:
        print(f"Failed to find chat id of {chat}.")
        sys.exit(1)

    success, status_code, photo_path = telegram_bot.send_photo(photo_path, chat_id, caption)
    if not success:
        print(f"Failed to send photo. Status code {status_code}")
        sys.exit(1)
    print(f"Photo sent successfully: {photo_path}")


def get_updates(
        bot: str,
        is_token: bool,
        bot_file: str,
) -> None:
    telegram_bot = get_bot(bot, is_token, bot_file)
    success, status_code, updates = telegram_bot.get_updates()
    if not success:
        print(f"Failed to get updates. Status code {status_code}")
        sys.exit(1)
    print(f"Bot updates:")
    pprint.pprint(updates)
