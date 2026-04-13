# API Segura de Registro de Usuarios

Esta es una API REST segura para el registro de usuarios con contraseñas hasheadas usando bcrypt.

## Características

- ✅ Validación de credenciales (email y password)
- ✅ Constraseña debe tener entre 8-10 caracteres
- ✅ Verificación de usuarios duplicados
- ✅ Hash de contraseñas con bcrypt
- ✅ Base de datos SQLite3
- ✅ Autenticación con JWT
- ✅ Respuestas HTTP estándar
- ✅ Sistema de logging completo con niveles jerárquicos

## Requisitos

- Python 3.7+
- pip

## Instalación

1. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

2. Crear la base de datos (ejecutar una sola vez):
```bash
python init_db.py
```

## Uso

1. Iniciar el servidor:
```bash
python app.py
```

El servidor estará disponible en `http://localhost:5000`

2. Registrar un usuario:
```bash
curl -X POST http://localhost:5000/registro \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@example.com",
    "password": "mipass123"
  }'
```

## Endpoints

### POST /registro

Registra un nuevo usuario.

**Request:**
```json
{
  "email": "usuario@example.com",
  "password": "mipass123"
}
```

**Respuestas:**

- **201 Created**: Usuario registrado exitosamente
```json
{
  "mensaje": "Usuario Registrado"
}
```

- **400 Bad Request**: Credenciales inválidas
```json
{
  "error": "Credenciales Invalidas"
}
```

- **409 Conflict**: Usuario ya existe
```json
{
  "error": "El usuario ya existe"
}
```

- **500 Internal Server Error**: Error en el servidor
```json
{
  "error": "Error interno del servidor"
}
```

### POST /login

Autentica un usuario y devuelve un JWT.

**Request:**
```json
{
  "email": "usuario@example.com",
  "password": "mipass123"
}
```

**Respuestas:**

- **200 OK**: Credenciales correctas
```json
{
  "token": "<JWT>",
  "role": "cliente"
}
```

- **400 Bad Request**: Credenciales inválidas
```json
{
  "error": "Credenciales Invalidas"
}
```

- **401 Unauthorized**: Credenciales incorrectas
```json
{
  "error": "Credenciales incorrectas"
}
```

### POST /crear_reserva

Crea una reserva protegida con JWT.

**Headers:**
```
Authorization: Bearer <JWT>
```

**Request:**
```json
{
  "cantidad": 2,
  "descripcion": "Reserva segura"
}
```

**Respuestas:**

- **201 Created**: Reserva creada exitosamente
```json
{
  "mensaje": "Reserva creada",
  "reserva": {
    "usuario_id": 1,
    "cantidad": 2,
    "descripcion": "Reserva segura"
  }
}
```

- **400 Bad Request**: Datos inválidos
```json
{
  "error": "Datos inválidos"
}
```

- **401 Unauthorized**: No autorizado o token inválido
```json
{
  "error": "No autorizado"
}
```

### GET /salud

Verifica que el servidor esté funcionando.

**Response:**
```json
{
  "estado": "El servidor está funcionando correctamente"
}
```

## Estructura de la Base de Datos

```sql
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'cliente'
)
```

## Seguridad

- Las contraseñas se hashean con bcrypt usando 12 rounds
- Se valida la longitud de la contraseña (8-10 caracteres)
- Se previene SQL injection usando prepared statements
- Se verifica la unicidad del email antes de registrar
- Sistema de logging que NO registra información sensible (contraseñas, tokens JWT)

## Logging

El sistema implementa un completo sistema de logging con los siguientes niveles:

- **DEBUG**: Información técnica y de depuración
- **INFO**: Eventos exitosos del sistema (registros, logins exitosos)
- **WARNING**: Errores causados por el usuario (credenciales inválidas, datos incorrectos)
- **ERROR**: Errores del sistema (fallos de base de datos, excepciones)

Los logs se guardan en el archivo `app.log` con el formato:
```
[Fecha y Hora] | [Nivel de Severidad] | Mensaje
```

Ejemplo:
```
[2026-04-13 08:06:28] | [INFO] | Usuario registrado exitosamente: usuario@example.com
[2026-04-13 08:06:28] | [WARNING] | Credenciales incorrectas para email: usuario@example.com
```
