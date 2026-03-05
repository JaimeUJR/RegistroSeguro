import os
import jwt
import datetime
from registro_logica import RegistroUsuario


def generate_jwt(user_id, role):
    secret = os.getenv('JWT_SECRET', 'dev-secret-change-me')
    payload = {
        'sub': user_id,
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }
    token = jwt.encode(payload, secret, algorithm='HS256')
    return token


def verify_jwt(token):
    secret = os.getenv('JWT_SECRET', 'dev-secret-change-me')
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        return payload
    except Exception:
        return None


def authenticate(email, password):
    reg = RegistroUsuario()
    user = reg.obtener_usuario(email)
    if not user:
        return None
    user_id, email_db, password_hash, role = user
    if reg.verificar_contrasena(password, password_hash):
        token = generate_jwt(user_id, role)
        return {'id': user_id, 'role': role, 'token': token}
    return None
