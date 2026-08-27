import os
import datetime
from functools import wraps
from flask import request, jsonify
from jose import jwt, JWTError

SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
ALGORITHM = "HS256"

# generates JWT
def encode_token(customer_id):
    issued_at = datetime.datetime.now(datetime.timezone.utc)
    payload = {
        "exp": issued_at + datetime.timedelta(hours=24),
        "iat": issued_at,
        "sub": str(customer_id)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# decodes the token with the secret key
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"message": "Token is missing or invalid"}), 401
        
        token = auth_header.split(" ")[1]
        try: # decodes the hash
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            customer_id = int(payload["sub"])
        except JWTError:
            return jsonify({"message": "Invalid or expired token"}), 401
        
        return f(customer_id, *args, **kwargs)
    return decorated