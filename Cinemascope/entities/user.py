from Cinemascope.api.api_manager import CinemaApiManager
from Cinemascope.utils.custom_requester import CustomRequester
class User:
    def __init__(self, email: str, password: str, roles: list, api: CinemaApiManager):
        self.email = email
        self.password = password
        self.roles = roles
        self.api = api  # Сюда будем передавать экземпляр API Manager для запросов

    @property
    def creds(self):
        """Возвращает кортеж (email, password)"""
        return self.email, self.password
class UserApi(CustomRequester):
    USER_BASE_URL = "https://auth.dev-cinescope.coconutqa.ru/"
    def __init__(self, session):
        self.session = session
        super().__init__(session, self.USER_BASE_URL)

    def get_user(self, user_locator):
        return self.send_request("GET", f"user/{user_locator}")

    def create_user(self, user_data, expected_status=201):
        return self.send_request(
            method="POST",
            endpoint="user",
            data=user_data,
            expected_status=expected_status
        )