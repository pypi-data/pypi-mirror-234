import abc
import requests
from typing import Any, Optional, Union


class FakeResponse:

    def __init__(
            self,
            res_type: str = "updates",
            files: Optional[dict[str, Any]] = None,
            msg: str = ""
    ):
        self.ok = True
        self.status_code = 200
        self.res_type = res_type
        self.files = files
        self.msg = msg

    def json(self) -> Any:
        if self.res_type == "updates":
            return {
                "ok": True,
                "result": [{"update_id": 1234}]
            }
        elif self.res_type == "message":
            return {
                "ok": True,
                "result": {
                    "text": self.msg
                }
            }
        else:
            return {"ok": True}


class AbstractBot(abc.ABC):

    def __init__(self, token: str, name: str = ""):
        self._token = token
        self.name = name
        self._base_url = f"https://api.telegram.org/bot{self._token}/"

    @property
    def token(self) -> str:
        return self._token

    def get_updates(self) -> tuple[bool, int, list[dict]]:
        """ Get updates for the current bot.
        """
        url = self._base_url + "getUpdates?timeout=100"
        res = self._get_request(url, "updates")
        if res is None:
            return False, 500, []
        updates = {}
        if res.ok:
            updates = res.json()["result"]
        return res.ok, res.status_code, updates

    def send_message(self, msg: str, chat_id: str) -> tuple[bool, int, str]:
        """ Send a message to the specified chat.
        """
        url = f"{self._base_url}sendMessage?chat_id={chat_id}&text={msg}"
        res = self._get_request(url, "message")
        if res is None:
            return False, 500, ""
        message = ""
        if res.ok:
            message = res.json()["result"]["text"]
        return res.ok, res.status_code, message

    def send_photo(
            self,
            photo_path: str,
            chat_id: str,
            caption: str = "") -> tuple[bool, int, str]:
        url = f"{self._base_url}sendPhoto?chat_id={chat_id}"
        if caption:
            url += f"&caption={caption}"

        with open(photo_path, "rb") as fp:
            res = self._post_request(url, {"photo": fp})

        if res is None:
            return False, 500, ""
        return res.ok, res.status_code, photo_path

    @abc.abstractmethod
    def _post_request(self, url: str, files: dict[str, Any]) -> Union[requests.Response, FakeResponse]:
        pass

    @abc.abstractmethod
    def _get_request(self, url: str, *args) -> Union[requests.Response, FakeResponse]:
        pass


class TelegramBot(AbstractBot):
    """ Class to interact with the telegram bot API.
    """

    def _post_request(self, url: str, files: dict[str, Any]) -> Optional[requests.Response]:
        try:
            return requests.post(url, files=files)
        except requests.ConnectionError:
            return

    def _get_request(self, url: str, *args) -> Optional[requests.Response]:
        try:
            return requests.get(url)
        except requests.ConnectionError:
            return


class TestBot(AbstractBot):
    """ Class used for testing purposes. Doesn't send requests
        to telegram API.
    """
    __test__ = False  # Prevent pytest from treating it like a test class

    def __init__(self, token: str, name: str = ""):
        super().__init__(token, name)
        self.responses = []  # type: list[FakeResponse]

    def _post_request(self, url: str, files: dict[str, Any]) -> FakeResponse:
        res = FakeResponse("photo", files)
        self.responses.append(res)
        return res

    def _get_request(self, url: str, *args) -> FakeResponse:
        msg = url.split("text=")[-1]
        res = FakeResponse(args[0], msg=msg)
        self.responses.append(res)
        return res

    def send_photo(
            self,
            photo_path: str,
            chat_id: str,
            caption: str = "") -> tuple[bool, int, str]:
        url = f"{self._base_url}sendPhoto?chat_id={chat_id}"
        if caption:
            url += f"&caption={caption}"

        res = self._post_request(url, {"photo": photo_path})

        if res is None:
            return False, 500, ""

        return res.ok, res.status_code, photo_path
