from Cinemascope.api.movies_api import MoviesAPI
from Cinemascope.api.auth_api import AuthAPI



class CinemaApiManager:
	def __init__(self, session, base_url):
		from Cinemascope.entities.user import UserApi
		self.session = session
		self.base_url = base_url
		self.auth_api = AuthAPI(self.session)
		self.movies_api = MoviesAPI(session, base_url)
		self.user_api = UserApi(session)


	def close_session(self):
		self.session.close()
