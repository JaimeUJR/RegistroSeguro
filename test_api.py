import requests

BASE_URL = 'http://localhost:5000'

def test_salud():
    print("=== TEST 1: Verificar que el servidor está vivo ===")
    response = requests.get(f'{BASE_URL}/salud')
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_registro_valido():
    print("=== TEST 2: Registrar usuario con credenciales válidas ===")
    datos = {
        "email": "usuario1@example.com",
        "password": "mipass123"
    }
    response = requests.post(f'{BASE_URL}/registro', json=datos)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    return response.status_code == 201

def test_registro_duplicado():
    print("=== TEST 3: Intentar registrar el mismo usuario (duplicado) ===")
    datos = {
        "email": "usuario1@example.com",
        "password": "mipass456"
    }
    response = requests.post(f'{BASE_URL}/registro', json=datos)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    return response.status_code == 409

def test_password_corto():
    print("=== TEST 4: Registrar con contraseña muy corta (7 caracteres) ===")
    datos = {
        "email": "usuario2@example.com",
        "password": "passcor"
    }
    response = requests.post(f'{BASE_URL}/registro', json=datos)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    return response.status_code == 400

def test_password_largo():
    print("=== TEST 5: Registrar con contraseña muy larga (11 caracteres) ===")
    datos = {
        "email": "usuario3@example.com",
        "password": "passlargo12"
    }
    response = requests.post(f'{BASE_URL}/registro', json=datos)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    return response.status_code == 400

def test_email_invalido():
    print("=== TEST 6: Registrar con email sin @ ===")
    datos = {
        "email": "usuarioinvalido",
        "password": "validpass9"
    }
    response = requests.post(f'{BASE_URL}/registro', json=datos)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    return response.status_code == 400

def test_campos_vacios():
    print("=== TEST 7: Registrar sin email y password ===")
    datos = {
        "email": "",
        "password": ""
    }
    response = requests.post(f'{BASE_URL}/registro', json=datos)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    return response.status_code == 400

if __name__ == '__main__':
    print("\n" + "="*60)
    print("PRUEBAS DEL API DE REGISTRO DE USUARIOS")
    print("="*60 + "\n")
    
    try:
        test_salud()
        
        # Test exitoso
        resultado1 = test_registro_valido()
        
        # Test duplicado
        resultado2 = test_registro_duplicado()
        
        # Test password corto
        resultado3 = test_password_corto()
        
        # Test password largo
        resultado4 = test_password_largo()
        
        # Test email inválido
        resultado5 = test_email_invalido()
        
        # Test campos vacíos
        resultado6 = test_campos_vacios()
        
        print("\n" + "="*60)
        print("RESUMEN DE RESULTADOS")
        print("="*60)
        print(f"✅ Registro válido (201): {'PASÓ' if resultado1 else 'FALLÓ'}")
        print(f"✅ Duplicado (409): {'PASÓ' if resultado2 else 'FALLÓ'}")
        print(f"✅ Password corto (400): {'PASÓ' if resultado3 else 'FALLÓ'}")
        print(f"✅ Password largo (400): {'PASÓ' if resultado4 else 'FALLÓ'}")
        print(f"✅ Email inválido (400): {'PASÓ' if resultado5 else 'FALLÓ'}")
        print(f"✅ Campos vacíos (400): {'PASÓ' if resultado6 else 'FALLÓ'}")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")
