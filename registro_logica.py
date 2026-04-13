import sqlite3
import bcrypt
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class RegistroUsuario:
    """Módulo de lógica para el registro seguro de usuarios"""
    
    def __init__(self, db_name='usuarios.db'):
        self.db_name = db_name
    
    def validar_credenciales(self, email, password):
        """
        Valida que las credenciales cumplan con los requisitos
        
        Args:
            email: Email del usuario
            password: Contraseña del usuario
        
        Returns:
            tuple: (es_valido, mensaje_error)
        """
        # Validar email
        if not email or '@' not in email:
            return False, "Email inválido"
        
        # Validar longitud de contraseña (8-10 caracteres)
        if not password or len(password) < 8 or len(password) > 10:
            return False, "Credenciales Invalidas"
        
        return True, ""
    
    def usuario_existe(self, email):
        """
        Verifica si un usuario con el email especificado ya existe
        
        Args:
            email: Email a verificar
        
        Returns:
            bool: True si existe, False si no existe
        """
        try:
            connection = sqlite3.connect(self.db_name)
            cursor = connection.cursor()
            cursor.execute('SELECT id FROM usuarios WHERE email = ?', (email,))
            resultado = cursor.fetchone()
            connection.close()
            return resultado is not None
        except sqlite3.Error as e:
            logger.error(f"Error de base de datos al verificar existencia de usuario {email}: {e}")
            return False

    def obtener_usuario(self, email):
        """
        Devuelve la tupla (id, email, password_hash, role) del usuario si existe
        """
        try:
            connection = sqlite3.connect(self.db_name)
            cursor = connection.cursor()
            cursor.execute('SELECT id, email, password, role FROM usuarios WHERE email = ?', (email,))
            row = cursor.fetchone()
            connection.close()
            return row
        except sqlite3.Error as e:
            logger.error(f"Error de base de datos al obtener usuario {email}: {e}")
            return None
    
    def hashear_contrasena(self, password):
        """
        Genera el hash de la contraseña usando bcrypt
        
        Args:
            password: Contraseña en texto plano
        
        Returns:
            str: Hash de la contraseña
        """
        salt = bcrypt.gensalt(rounds=12)
        hash_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hash_password.decode('utf-8')

    def verificar_contrasena(self, password, password_hash):
        """
        Verifica una contraseña en texto plano contra el hash almacenado
        """
        try:
            return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
        except Exception:
            return False
    
    def registrar_usuario(self, email, password):
        """
        Registra un nuevo usuario en la base de datos
        
        Args:
            email: Email del usuario
            password: Contraseña en texto plano
        
        Returns:
            dict: Respuesta con status, codigo y mensaje
        """
        logger.debug(f"Iniciando registro de usuario: {email}")
        
        # Validar credenciales
        es_valido, mensaje_error = self.validar_credenciales(email, password)
        if not es_valido:
            logger.warning(f"Validación fallida para usuario {email}: {mensaje_error}")
            return {
                'status': False,
                'codigo': 400,
                'mensaje': mensaje_error
            }
        
        # Verificar si el usuario ya existe
        if self.usuario_existe(email):
            logger.warning(f"Intento de registro de usuario ya existente: {email}")
            return {
                'status': False,
                'codigo': 409,
                'mensaje': 'El usuario ya existe'
            }
        
        # Hashear la contraseña
        password_hash = self.hashear_contrasena(password)
        logger.debug(f"Contraseña hasheada para usuario: {email}")
        
        # Guardar en la base de datos
        try:
            connection = sqlite3.connect(self.db_name)
            cursor = connection.cursor()
            cursor.execute(
                'INSERT INTO usuarios (email, password, role) VALUES (?, ?, ?)',
                (email, password_hash, 'cliente')
            )
            connection.commit()
            connection.close()
            
            logger.info(f"Usuario registrado exitosamente en base de datos: {email}")
            return {
                'status': True,
                'codigo': 201,
                'mensaje': 'Usuario Registrado'
            }
        except sqlite3.Error as e:
            logger.error(f"Error al guardar usuario {email} en base de datos: {str(e)}")
            return {
                'status': False,
                'codigo': 500,
                'mensaje': f'Error en la base de datos: {str(e)}'
            }
