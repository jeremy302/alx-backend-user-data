#!/usr/bin/env python3
''' session auth module '''
from api.v1.auth.auth import Auth
from models.user import User
import uuid
import datetime


class SessionAuth(Auth):
    ''' session auth class '''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        ''' creates a session '''
        if user_id is None or type(user_id) is not str:
            return None
        sess_id = str(uuid.uuid4())
        self.user_id_by_session_id[sess_id] = user_id
        return sess_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        ''' gets user id for a session'''
        if session_id is None or type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        ''' gets current user from session cookie '''
        sess_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(sess_id)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        ''' deletes a session (logout) '''
        if request is None:
            return False
        sess_id = self.session_cookie(request)
        if not sess_id:
            return False
        user_id = self.user_id_for_session_id(sess_id)
        if not user_id:
            return False
        del self.user_id_by_session_id[sess_id]
        return True
