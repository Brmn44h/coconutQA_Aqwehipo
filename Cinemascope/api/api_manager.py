from Cinemascope.api.movies_api import MoviesAPI

class CinemaApiManager:
	def __init__(self, session, base_url):
		self.session = session
		self.base_url = base_url
		self.movies_api = MoviesAPI(session, base_url)


