#!/usr/bin/env python3
''' auth module '''
from flask import request
from typing import TypeVar, List


class Auth:
    ''' auth class '''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        ''' require auth '''
        path = (path.rstrip('/') + '/') if path else path
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        for p in excluded_paths:
            if path == p or (p.endswith('*') and path.startswith(p[:-1])):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        ''' authorization header '''
        if request is None or not request.headers.get('Authorization'):
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        ''' current user '''
        return None
