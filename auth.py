import os
import jwt
import datetime
from registro_logica import RegistroUsuario
import logging

logger = logging.getLogger(__name__)


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
    logger.debug("Verificando token JWT")
    secret = os.getenv('JWT_SECRET', 'dev-secret-change-me')
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        logger.debug("Token JWT válido")
        return payload
    except Exception as e:
        logger.warning(f"Token JWT inválido: {str(e)}")
        return None


def authenticate(email, password):
    logger.debug(f"Iniciando autenticación para usuario: {email}")
    
    reg = RegistroUsuario()
    user = reg.obtener_usuario(email)
    if not user:
        logger.warning(f"Usuario no encontrado: {email}")
        return None
    
    user_id, email_db, password_hash, role = user
    logger.debug(f"Usuario encontrado: {email}, verificando contraseña")
    
    if reg.verificar_contrasena(password, password_hash):
        token = generate_jwt(user_id, role)
        logger.info(f"Autenticación exitosa para usuario: {email}")
        return {'id': user_id, 'role': role, 'token': token}
    
    logger.warning(f"Contraseña incorrecta para usuario: {email}")
    return None
