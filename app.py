from flask import Flask, request, jsonify
from registro_logica import RegistroUsuario
from auth import authenticate, verify_jwt
import bleach
import logging

# Configuración del logging
logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='[%(asctime)s] | [%(levelname)s] | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

app = Flask(__name__)
registro = RegistroUsuario()

@app.route('/registro', methods=['POST'])
def registro_usuario():
    """
    Endpoint POST para registrar un nuevo usuario
    
    Body esperado:
    {
        "email": "usuario@example.com",
        "password": "contraseña"
    }
    """
    try:
        logger.debug("Iniciando proceso de registro de usuario")
        
        # Obtener datos del request
        datos = request.get_json()
        
        if not datos:
            logger.warning("Intento de registro con datos JSON inválidos")
            return jsonify({
                'error': 'Credenciales Invalidas'
            }), 400
        
        email = datos.get('email', '').strip()
        password = datos.get('password', '').strip()
        
        # Validar que los campos existan
        if not email or not password:
            logger.warning(f"Intento de registro con campos vacíos para email: {email}")
            return jsonify({
                'error': 'Credenciales Invalidas'
            }), 400
        
        logger.debug(f"Procesando registro para email: {email}")
        
        # Registrar el usuario
        resultado = registro.registrar_usuario(email, password)
        
        # Retornar respuesta según el resultado
        if resultado['status']:
            logger.info(f"Usuario registrado exitosamente: {email}")
            return jsonify({
                'mensaje': resultado['mensaje']
            }), resultado['codigo']
        else:
            logger.warning(f"Registro fallido para email {email}: {resultado['mensaje']}")
            return jsonify({
                'error': resultado['mensaje']
            }), resultado['codigo']
    
    except Exception as e:
        logger.error(f"Error interno del servidor durante registro: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor'
        }), 500


@app.route('/login', methods=['POST'])
def login():
    """Endpoint para autenticación. Devuelve JWT si credenciales válidas."""
    try:
        logger.debug("Iniciando proceso de autenticación")
        
        datos = request.get_json()
        if not datos:
            logger.warning("Intento de login con datos JSON inválidos")
            return jsonify({'error': 'Credenciales Invalidas'}), 400

        email = datos.get('email', '').strip()
        password = datos.get('password', '').strip()

        if not email or not password:
            logger.warning(f"Intento de login con campos vacíos para email: {email}")
            return jsonify({'error': 'Credenciales Invalidas'}), 400

        logger.debug(f"Procesando autenticación para email: {email}")
        
        auth_result = authenticate(email, password)
        if not auth_result:
            logger.warning(f"Credenciales incorrectas para email: {email}")
            return jsonify({'error': 'Credenciales incorrectas'}), 401

        logger.info(f"Login exitoso para usuario: {email}")
        return jsonify({'token': '[TOKEN_REDACTED]', 'role': auth_result['role']}), 200
    except Exception as e:
        logger.error(f"Error interno del servidor durante login: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500


def require_auth(request):
    """Extrae y verifica JWT del header Authorization. Retorna payload o None."""
    logger.debug("Verificando autenticación en request")
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        logger.debug("Header Authorization no presente o malformado")
        return None
    token = auth_header.split(' ', 1)[1].strip()
    return verify_jwt(token)


@app.route('/crear_reserva', methods=['POST'])
def crear_reserva():
    """Endpoint central de ejemplo que requiere JWT y valida inputs."""
    try:
        logger.debug("Iniciando proceso de creación de reserva")
        
        payload = require_auth(request)
        if not payload:
            logger.warning("Intento de acceso no autorizado a crear_reserva")
            return jsonify({'error': 'No autorizado'}), 401

        logger.debug(f"Usuario autorizado: {payload.get('sub')}")
        
        datos = request.get_json()
        if not datos:
            logger.warning(f"Usuario {payload.get('sub')}: Datos JSON inválidos en crear_reserva")
            return jsonify({'error': 'Datos inválidos'}), 400

        # Validar cantidad
        try:
            cantidad = int(datos.get('cantidad', 0))
        except Exception:
            logger.warning(f"Usuario {payload.get('sub')}: Cantidad no es un número entero")
            return jsonify({'error': 'Cantidad debe ser un número entero'}), 400

        if cantidad <= 0:
            logger.warning(f"Usuario {payload.get('sub')}: Cantidad no positiva: {cantidad}")
            return jsonify({'error': 'Cantidad debe ser positiva'}), 400

        descripcion = datos.get('descripcion', '')
        # Sanitizar descripción para evitar HTML/JS
        descripcion_segura = bleach.clean(str(descripcion), strip=True)

        logger.debug(f"Usuario {payload.get('sub')}: Creando reserva con cantidad {cantidad}")
        
        # Nota: aquí se podría insertar en BD usando consultas parametrizadas.
        resultado = {
            'usuario_id': payload.get('sub'),
            'cantidad': cantidad,
            'descripcion': descripcion_segura
        }

        logger.info(f"Reserva creada exitosamente para usuario {payload.get('sub')}: cantidad {cantidad}")
        return jsonify({'mensaje': 'Reserva creada', 'reserva': resultado}), 201
    except Exception as e:
        logger.error(f"Error interno del servidor durante creación de reserva: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500


@app.route('/salud', methods=['GET'])
def salud():
    """Endpoint de verificación de salud del servidor"""
    logger.debug("Verificación de salud del servidor solicitada")
    logger.info("Servidor funcionando correctamente")
    return jsonify({
        'estado': 'El servidor está funcionando correctamente'
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
