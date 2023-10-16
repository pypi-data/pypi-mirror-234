import httpx
import logging
from . import __user_agent__

logger = logging.getLogger(__name__)


class NetworkClient(httpx.Client):
    def __init__(self, url="https://e621.net", username=None, api_key=None):
        if url != "https://e621.net" and url != "http://127.0.0.1:3000":
            logger.warn(
                "Using other websites is not supported, so some features may break or not work at all"
            )

        super().__init__(base_url=url)
        self.headers.update({'user-agent': __user_agent__})
        self.logged_in = False
        if username != None and api_key != None:
            self.log_in(username, api_key)

    def log_in(self, username, api_key) -> bool:
        request = self.get(url="/favorites.json", auth=(username, api_key))

        if request.status_code == 401:
            logger.error("Username/api_key not valid")
            return False

        self.auth = (username, api_key)
        self.logged_in = True
        logger.info(f"Now logged in as {username}")
        return True
