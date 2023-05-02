#!/usr/bin/env python3
''' basic auth module '''
import base64
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    ''' basic auth '''
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        ''' extract base64 authorization header '''
        if (authorization_header is None or (
                type(authorization_header) is not str) or (
                not authorization_header.startswith('Basic '))):
            return None
        else:
            return authorization_header[len('Basic '):]

    def decode_base64_authorization_header(
                self, base64_authorization_header: str) -> str:
        ''' decode base64 authorization header '''
        if (base64_authorization_header is None or (
                type(base64_authorization_header) is not str)):
            return None
        try:
            return base64.b64decode(base64_authorization_header).decode()
        except Exception as ex:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        ''' extract user credentials '''
        if (decoded_base64_authorization_header is None or
            type(decoded_base64_authorization_header) is not str or (
                ':' not in decoded_base64_authorization_header)):
            return None, None
        # print(tuple(decoded_base64_authorization_header.split(':', 1)))
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        ''' user object from credentials '''
        if (user_email is None or type(user_email) is not str) or (
                user_pwd is None or type(user_pwd) is not str):
            return None
        users = None
        try:
            users = User.search({'email': user_email})
        except Exception as err:
            users = None
        if not users:
            return None
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        ''' current user '''
        auth_header = self.authorization_header(request)
        auth_b64 = self.extract_base64_authorization_header(auth_header)
        raw_creds = self.decode_base64_authorization_header(auth_b64)
        creds = self.extract_user_credentials(raw_creds)
        user = self.user_object_from_credentials(creds[0], creds[1])
        return user
