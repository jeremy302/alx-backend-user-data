#!/usr/bin/env python3
''' session db auth module '''
import os
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    ''' session authentication with persistence '''
    def create_session(self, user_id=None):
        ''' creates new persistent session '''
        sess_id = super().create_session(user_id)
        if not sess_id:
            return None
        sess = UserSession(user_id=user_id, session_id=sess_id)
        sess.save()
        return sess_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieves the user id of the user associated with
        a given session id.
        """
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) <= 0:
            return None
        cur_time = datetime.now()
        time_span = timedelta(seconds=self.session_duration)
        exp_time = sessions[0].created_at + time_span
        if exp_time < cur_time:
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None):
        ''' destroys a session (logout) '''
        if request is None:
            return False
        sess_id = self.session_cookie(request)
        if not sess_id:
            return False
        sessions = None
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception as err:
            return None
        if not sessions:
            return None
        session = sessions[0]
        session.remove()
        return True
