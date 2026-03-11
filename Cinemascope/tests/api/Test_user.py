import pytest
from Cinemascope.api.api_manager import CinemaApiManager
from Cinemascope.models.base_models import TestUser, RegisterUserResponse
class TestUserAPI:

    def test_create_user(self, super_admin, creation_user_data):
        response = super_admin.api.user_api.create_user(user_data=creation_user_data)
        created_user = RegisterUserResponse(**response.json())
        assert created_user.email == creation_user_data.email
        assert created_user.fullName == creation_user_data.fullName
        assert created_user.roles == creation_user_data.roles
        assert created_user.verified is True

    def test_get_user_by_locator(self, super_admin, creation_user_data):
        created_user_response = super_admin.api.user_api.create_user(user_data=creation_user_data)
        created_user = RegisterUserResponse(**created_user_response.json())
        response_by_id_data = super_admin.api.user_api.get_user(created_user.id).json()
        user_by_id = RegisterUserResponse(**response_by_id_data)
        response_by_email_data = super_admin.api.user_api.get_user(creation_user_data.email).json()
        user_by_email = RegisterUserResponse(**response_by_email_data)
        assert user_by_id == user_by_email, "Содержание ответов должно быть идентичным"


    def test_get_user_by_id_common_user(self, common_user):
        common_user.api.user_api.get_user(common_user.email, expected_status=403)

    def test_register_user(self, api_manager: CinemaApiManager, registration_user_data):
        response = api_manager.auth_api.register_user(user_data=registration_user_data)
        register_user_response = RegisterUserResponse(**response.json())
        assert register_user_response.email == registration_user_data["email"]



