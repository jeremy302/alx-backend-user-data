#!/usr/bin/env python3
''' session auth view '''
import os
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


SESSION_COOKIE_NAME = os.environ.get('SESSION_NAME')


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    ''' login method '''
    from api.v1.app import auth

    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({'error': 'email missing'}), 400
    if not password:
        return jsonify({'error': 'password missing'}), 400
    users = User.search({'email': email})
    if not users:
        return jsonify({'error': 'no user found for this email'}), 404
    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    sess_id = auth.create_session(user.id)
    res = jsonify(user.to_json())
    res.set_cookie(SESSION_COOKIE_NAME, sess_id)
    return res


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout() -> str:
    ''' logout method '''
    from api.v1.app import auth

    success = auth.destroy_session(request)
    if not success:
        abort(404)
    else:
        return jsonify({}), 200
