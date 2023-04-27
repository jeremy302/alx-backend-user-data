#!/usr/bin/env python3
''' session exp auth module '''
import os
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    ''' session authentication with expiration date '''
    def __init__(self):
        ''' class constructor '''
        super().__init__()
        try:
            self.session_duration = int(os.environ['SESSION_DURATION'])
        except Exception as err:
            self.session_duration = 0

    def create_session(self, user_id=None):
        ''' creates a session '''
        sess_id = super().create_session(user_id)
        if sess_id is None:
            return None
        self.user_id_by_session_id[sess_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return sess_id

    def user_id_for_session_id(self, session_id=None):
        ''' gets the user_id belonging to a session '''
        duration = timedelta(seconds=self.session_duration)

        if session_id is None:
            return None
        sess = self.user_id_by_session_id.get(session_id)
        if sess is None or type(sess) is not dict:
            return None
        elif self.session_duration <= 0:
            return sess['user_id']
        elif 'created_at' not in sess:
            return None
        elif (sess['created_at'] + duration) < datetime.now():
            return None
        else:
            return sess['user_id']
