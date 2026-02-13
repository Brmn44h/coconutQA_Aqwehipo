from Cinemascope.utils.custom_requester import CustomRequester


class MoviesAPI(CustomRequester):
	def __init__(self, session, base_url=None):
		if base_url is None:
			from Cinemascope.constants import BASE_URL
			base_url = BASE_URL
		super().__init__(session=session, base_url=base_url)

	def create_movie(self, movie_data, expected_status=200):
		return self.send_request(
			method='POST',
			endpoint="/movies",
			data=movie_data,
			expected_status=expected_status
		)

	def get_movie(self, movie_id, expected_status=200):
		return self.send_request(
			method='GET',
			endpoint=f"/movies/{movie_id}",
			expected_status=expected_status
		)

	def update_movie(self, movie_id, update_data, expected_status=200):
		return self.send_request(
			method='PATCH',
			endpoint=f"/movies/{movie_id}",
			data=update_data,
			expected_status=expected_status
		)

	def delete_movie(self, movie_id, expected_status=200):
		return self.send_request(
			method='DELETE',
			endpoint=f"/movies/{movie_id}",
			expected_status=expected_status
		)

	def get_movies_list(self, params=None, expected_status=200):
		return self.send_request(
			method="GET",
			endpoint="/movies",
			params=params,
			expected_status=expected_status
		)
