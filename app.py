from flask import Flask, request, jsonify
from registro_logica import RegistroUsuario
from auth import authenticate, verify_jwt
import bleach

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
        # Obtener datos del request
        datos = request.get_json()
        
        if not datos:
            return jsonify({
                'error': 'Credenciales Invalidas'
            }), 400
        
        email = datos.get('email', '').strip()
        password = datos.get('password', '').strip()
        
        # Validar que los campos existan
        if not email or not password:
            return jsonify({
                'error': 'Credenciales Invalidas'
            }), 400
        
        # Registrar el usuario
        resultado = registro.registrar_usuario(email, password)
        
        # Retornar respuesta según el resultado
        if resultado['status']:
            return jsonify({
                'mensaje': resultado['mensaje']
            }), resultado['codigo']
        else:
            return jsonify({
                'error': resultado['mensaje']
            }), resultado['codigo']
    
    except Exception as e:
        return jsonify({
            'error': 'Error interno del servidor'
        }), 500


@app.route('/login', methods=['POST'])
def login():
    """Endpoint para autenticación. Devuelve JWT si credenciales válidas."""
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({'error': 'Credenciales Invalidas'}), 400

        email = datos.get('email', '').strip()
        password = datos.get('password', '').strip()

        if not email or not password:
            return jsonify({'error': 'Credenciales Invalidas'}), 400

        auth_result = authenticate(email, password)
        if not auth_result:
            return jsonify({'error': 'Credenciales incorrectas'}), 401

        return jsonify({'token': auth_result['token'], 'role': auth_result['role']}), 200
    except Exception:
        return jsonify({'error': 'Error interno del servidor'}), 500


def require_auth(request):
    """Extrae y verifica JWT del header Authorization. Retorna payload o None."""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return None
    token = auth_header.split(' ', 1)[1].strip()
    return verify_jwt(token)


@app.route('/crear_reserva', methods=['POST'])
def crear_reserva():
    """Endpoint central de ejemplo que requiere JWT y valida inputs."""
    try:
        payload = require_auth(request)
        if not payload:
            return jsonify({'error': 'No autorizado'}), 401

        datos = request.get_json()
        if not datos:
            return jsonify({'error': 'Datos inválidos'}), 400

        # Validar cantidad
        try:
            cantidad = int(datos.get('cantidad', 0))
        except Exception:
            return jsonify({'error': 'Cantidad debe ser un número entero'}), 400

        if cantidad <= 0:
            return jsonify({'error': 'Cantidad debe ser positiva'}), 400

        descripcion = datos.get('descripcion', '')
        # Sanitizar descripción para evitar HTML/JS
        descripcion_segura = bleach.clean(str(descripcion), strip=True)

        # Nota: aquí se podría insertar en BD usando consultas parametrizadas.
        resultado = {
            'usuario_id': payload.get('sub'),
            'cantidad': cantidad,
            'descripcion': descripcion_segura
        }

        return jsonify({'mensaje': 'Reserva creada', 'reserva': resultado}), 201
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500


@app.route('/salud', methods=['GET'])
def salud():
    """Endpoint de verificación de salud del servidor"""
    return jsonify({
        'estado': 'El servidor está funcionando correctamente'
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
