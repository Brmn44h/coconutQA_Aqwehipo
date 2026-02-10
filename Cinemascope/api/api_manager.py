from Auth.constants import BASE_URL





class CinemaApiManager:


	def __init__(self, session, base_url):
		"""
		session: авторизованная сессия (auth_session)
		base_url: базовый URL API
		"""
		self.session = session
		self.base_url = base_url



	def create_movie(self, movie_data):
		"""Создать новый фильм"""
		return self.session.post(f"{self.base_url}/movies", json=movie_data)

	def get_movie(self, movie_id):
		"""Получить фильм по ID"""
		return self.session.get(f"{self.base_url}/movies/{movie_id}")

	def update_movie(self, movie_id, update_data):
		"""Обновить фильм (частично)"""
		return self.session.patch(f"{self.base_url}/movies/{movie_id}", json=update_data)

	def delete_movie(self, movie_id):
		"""Удалить фильм"""
		return self.session.delete(f"{self.base_url}/movies/{movie_id}")

	def get_movies_list(self, params=None):
		"""Получить список фильмов с фильтрами"""
		return self.session.get(f"{self.base_url}/movies", params=params)



	def create_and_validate(self, movie_data, expected_status=201):
		"""Создать фильм и проверить статус"""
		response = self.create_movie(movie_data)
		assert response.status_code == expected_status, \
			f"Ошибка создания фильма: {response.status_code}"
		return response

	def get_and_validate(self, movie_id, expected_status=200):
		"""Получить фильм и проверить статус"""
		response = self.get_movie(movie_id)
		assert response.status_code == expected_status, \
			f"Фильм не найден: {response.status_code}"
		return response
