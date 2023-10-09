from datetime import datetime
from flask import redirect, request, jsonify, session, url_for
from functools import wraps
from ..models.todo import Users
import jwt

# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in session:
            token = session['x-access-token']

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        # return 401 if token is not passed
        if not token:
            # return jsonify({'message' : 'Token is missing !!'}), 401
            return redirect(url_for("login"))
  
        try:
            data = jwt.decode(token, 'secret-key', ["HS256"])
            if datetime.utcnow() > datetime.utcfromtimestamp(data['exp']):
                return redirect(url_for("login"))
            # decoding the payload to fetch the stored details
            current_user = Users.getOne(data['email'])
        except BaseException as e:
            print(e)
            return redirect(url_for("login"))
        # returns the current logged in users context to the routes
        return  f(current_user, *args, **kwargs)
  
    return decorated