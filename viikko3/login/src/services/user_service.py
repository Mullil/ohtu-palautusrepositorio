from entities.user import User
from repositories.user_repository import (
    user_repository as default_user_repository
)
import re


class UserInputError(Exception):
    pass


class AuthenticationError(Exception):
    pass


class UserService:
    def __init__(self, user_repository=default_user_repository):
        self._user_repository = user_repository

    def check_credentials(self, username, password):
        if not username or not password:
            raise UserInputError("Username and password are required")

        user = self._user_repository.find_by_username(username)

        if not user or user.password != password:
            raise AuthenticationError("Invalid username or password")

        return user

    def create_user(self, username, password, password_confirmation):
        self.validate(username, password, password_confirmation)

        user = self._user_repository.create(
            User(username, password)
        )

        return user

    def validate(self, username, password, password_confirmation):
        if not username or not password:
            raise UserInputError("Username and password are required")
        if len(username) < 3:
            raise UserInputError("too short username")
        if len(password) < 8:
            raise UserInputError("too short password")
        if (password != password_confirmation):
            raise UserInputError("passwords do not match")
        if re.fullmatch(r'[a-zA-Z]+', password):
            raise UserInputError("password cannot only consist of letters")
        if (default_user_repository.find_by_username(username)):
            raise UserInputError("username already in use")
user_service = UserService()
