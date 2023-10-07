import os
import subprocess


env = os.environ.copy()
env["bot"] = "test"

this_dir = os.path.dirname(os.path.abspath(__file__))
bot_file = os.path.join(this_dir, "bot.csv")
chat_file = os.path.join(this_dir, "chat.csv")


def test_send_message():
    result = subprocess.run(
        ["telegrambot", "message",
         "-b", "MyTestBot",
         "-c", "MyTestChat",
         "-f", bot_file,
         "-cf", chat_file,
         "-m", "hello world"
         ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "Message sent successfully: hello world".strip()


def test_send_photo():
    photo_file = os.path.join(this_dir, "dog.jpg")
    result = subprocess.run(
        ["telegrambot", "photo",
         "-b", "MyTestBot",
         "-c", "MyTestChat",
         "-f", bot_file,
         "-cf", chat_file,
         "-p", photo_file,
         "-cp", "Cute dog"
         ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env
    )
    assert result.returncode == 0
    assert "Photo sent successfully:" in result.stdout
    assert "dog.jpg" in result.stdout


def test_get_updates():
    result = subprocess.run(
        ["telegrambot", "updates",
         "-b", "MyTestBot",
         "-f", bot_file
         ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env
    )
    assert result.returncode == 0
    assert "Bot updates" in result.stdout
