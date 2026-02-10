# Auth/api/auth_api.py
from Cinemascope.constants import AUTH_URL, REGISTER_ENDPOINT, LOGIN_ENDPOINT
from Cinemascope.utils.custom_requester import CustomRequester


class AuthAPI(CustomRequester):
	"""
	Класс для работы с аутентификацией.
	"""

	def __init__(self, session, auth_url=None):
		if auth_url is None:
			auth_url = AUTH_URL
		super().__init__(session=session, base_url=auth_url)

	def authenticate(self, email, password):
		login_data = {
			"email": email,
			"password": password
		}

		response = self.login_user(login_data)
		response_json = response.json()

		if "accessToken" not in response_json:
			raise KeyError("token is missing")

		token = response_json["accessToken"]  # ← используем response_json!
		self._update_session_headers(**{"Authorization": f"Bearer {token}"})

		return token


	def login_user(self, login_data, expected_status=200):

		return self.send_request(
		method="POST",
		endpoint=LOGIN_ENDPOINT,
		data=login_data,
		expected_status=expected_status
	)


	def register_user(self, user_data, expected_status=201):

		return self.send_request(
		method="POST",
		endpoint=REGISTER_ENDPOINT,
		data=user_data,
		expected_status=expected_status
	)


