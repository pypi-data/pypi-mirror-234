import os
from telegrambot.bot import TestBot


def test_get_updates():
    bot = TestBot("TestToken")
    success, status_code, updates = bot.get_updates()
    assert success
    assert status_code == 200
    assert updates == [{"update_id": 1234}]


def test_send_message():
    bot = TestBot("TestToken")
    success, status_code, message = bot.send_message("TestMessage", "ChatId")
    assert success
    assert status_code == 200
    assert message == "TestMessage"

    assert len(bot.responses) == 1
    res = bot.responses[0].json()
    assert res["result"]["text"] == "TestMessage"


def test_send_photo():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    photo_file = os.path.join(this_dir, "dog.jpg")
    bot = TestBot("TestToken")
    success, status_code, photo = bot.send_photo(photo_file, "ChatId")
    assert success
    assert status_code == 200
    assert photo == photo_file
