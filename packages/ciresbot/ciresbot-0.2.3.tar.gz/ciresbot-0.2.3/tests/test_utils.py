import os
from telegrambot import utils


this_dir = os.path.dirname(os.path.abspath(__file__))


class TestValidateFile:

    def test_file_not_found(self):
        assert not utils.validate_file("not-a-file.txt", True)

    def test_do_not_verify(self):
        assert utils.validate_file("not-a-file.txt", False)

    def test_file_found(self):
        file = os.path.join(this_dir, "bot.csv")
        assert utils.validate_file(file, True)


class TestGetBotToken:

    def test_token_is_passed(self):
        bot = utils.get_bot("TestToken", True, "")
        assert bot.token == "TestToken"

    def test_finds_token_with_bot_name(self):
        file = os.path.join(this_dir, "bot.csv")
        bot = utils.get_bot("MyTestBot", False, file)
        assert bot.token == "testToken"

    def test_returns_null_if_token_not_found(self):
        file = os.path.join(this_dir, "bot.csv")
        bot = utils.get_bot("BadBot", False, file)
        assert bot is None


class TestGetChatID:

    def test_id_is_passed(self):
        chat_id = utils.get_chat_id("TestID", "", True)
        assert chat_id == "TestID"

    def test_finds_id_with_chat_name(self):
        file = os.path.join(this_dir, "chat.csv")
        chat_id = utils.get_chat_id(
            "MyTestChat", file, bot_name="MyTestBot")
        assert chat_id == "12345"

    def test_returns_empty_if_bot_does_not_belong_to_chat(self):
        file = os.path.join(this_dir, "chat.csv")
        chat_id = utils.get_chat_id(
            "MyTestChat", file, bot_name="OtherBot")
        assert chat_id == ""

