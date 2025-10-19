#!/usr/bin/env python3
"""
Script de pruebas para la API de Catálogo de Películas
Ejecutar después de que la API esté corriendo con docker-compose up
"""

import requests
import json
import time

# URL base de la API
BASE_URL = "http://localhost:5000"

def test_health():
    """Probar el endpoint de salud"""
    print("🔍 Probando endpoint de salud...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print("✅ Endpoint de salud funcionando\n")
    except Exception as e:
        print(f"❌ Error en endpoint de salud: {e}\n")

def test_get_all_movies():
    """Probar GET /peliculas"""
    print("🔍 Probando GET /peliculas (obtener todas las películas)...")
    try:
        response = requests.get(f"{BASE_URL}/peliculas")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Total de películas: {data.get('total', 0)}")
        if data.get('success') and data.get('data'):
            print(f"Primera película: {data['data'][0]['nombre']}")
        print("✅ GET /peliculas funcionando\n")
        return True
    except Exception as e:
        print(f"❌ Error en GET /peliculas: {e}\n")
        return False
    
def test_get_top_movies():
    """Probar GET /peliculas/top"""
    print("\n🔍 Probando GET /peliculas/top (top 5 mejor calificadas)...")
    try:
        response = requests.get(f"{BASE_URL}/peliculas/top")
        print(f"Status: {response.status_code}")
        data = response.json()
        if data.get('success'):
            print(f"Se obtuvieron {data['total']} películas del top correctamente ✅")
            if data['data']:
                print(f"Mejor calificada: {data['data'][0]['nombre']} ({data['data'][0]['calificacion']})")
            return True
        else:
            print(f"❌ Error: {data}")
            return False
    except Exception as e:
        print(f"❌ Error en GET /peliculas/top: {e}")
        return False


def test_get_movie_by_id():
    """Probar GET /peliculas/{id}"""
    print("🔍 Probando GET /peliculas/1 (obtener película por ID)...")
    try:
        response = requests.get(f"{BASE_URL}/peliculas/1")
        print(f"Status: {response.status_code}")
        data = response.json()
        if data.get('success'):
            print(f"Película encontrada: {data['data']['nombre']}")
            print("✅ GET /peliculas/{id} funcionando\n")
            return True
        else:
            print(f"❌ Error: {data}\n")
            return False
    except Exception as e:
        print(f"❌ Error en GET /peliculas/1: {e}\n")
        return False

def test_create_movie():
    """Probar POST /peliculas"""
    print("🔍 Probando POST /peliculas (crear nueva película)...")
    try:
        nueva_pelicula = {
            "nombre": "Inception",
            "categoria": "Ciencia Ficción",
            "año": 2010,
            "director": "Christopher Nolan",
            "duracion": 148,
            "calificacion": 8.8
        }
        
        response = requests.post(
            f"{BASE_URL}/peliculas",
            json=nueva_pelicula,
            headers={'Content-Type': 'application/json'}
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        
        if data.get('success'):
            print(f"Película creada: {data['data']['nombre']} (ID: {data['data']['id']})")
            print("✅ POST /peliculas funcionando\n")
            return data['data']['id']
        else:
            print(f"❌ Error: {data}\n")
            return None
    except Exception as e:
        print(f"❌ Error en POST /peliculas: {e}\n")
        return None

def test_update_movie(movie_id):
    """Probar PUT /peliculas/{id}"""
    print(f"🔍 Probando PUT /peliculas/{movie_id} (actualizar película)...")
    try:
        actualizacion = {
            "calificacion": 9.0,
            "duracion": 150
        }
        
        response = requests.put(
            f"{BASE_URL}/peliculas/{movie_id}",
            json=actualizacion,
            headers={'Content-Type': 'application/json'}
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        
        if data.get('success'):
            print(f"Película actualizada: {data['data']['nombre']}")
            print(f"Nueva calificación: {data['data']['calificacion']}")
            print("✅ PUT /peliculas/{id} funcionando\n")
            return True
        else:
            print(f"❌ Error: {data}\n")
            return False
    except Exception as e:
        print(f"❌ Error en PUT /peliculas/{movie_id}: {e}\n")
        return False

def test_delete_movie(movie_id):
    """Probar DELETE /peliculas/{id}"""
    print(f"🔍 Probando DELETE /peliculas/{movie_id} (eliminar película)...")
    try:
        response = requests.delete(f"{BASE_URL}/peliculas/{movie_id}")
        print(f"Status: {response.status_code}")
        data = response.json()
        
        if data.get('success'):
            print("Película eliminada exitosamente")
            print("✅ DELETE /peliculas/{id} funcionando\n")
            return True
        else:
            print(f"❌ Error: {data}\n")
            return False
    except Exception as e:
        print(f"❌ Error en DELETE /peliculas/{movie_id}: {e}\n")
        return False

def test_invalid_requests():
    """Probar casos de error"""
    print("🔍 Probando casos de error...")
    
    # Película no encontrada
    print("- Probando película no encontrada...")
    response = requests.get(f"{BASE_URL}/peliculas/9999")
    print(f"  Status: {response.status_code} (esperado: 404)")
    
    # Datos inválidos
    print("- Probando datos inválidos...")
    pelicula_invalida = {
        "nombre": "",  # Nombre vacío
        "año": "no_es_numero"  # Año inválido
    }
    response = requests.post(
        f"{BASE_URL}/peliculas",
        json=pelicula_invalida,
        headers={'Content-Type': 'application/json'}
    )
    print(f"  Status: {response.status_code} (esperado: 400)")
    
    # Endpoint no existente
    print("- Probando endpoint no existente...")
    response = requests.get(f"{BASE_URL}/no_existe")
    print(f"  Status: {response.status_code} (esperado: 404)")
    
    print("✅ Pruebas de casos de error completadas\n")

def main():
    """Ejecutar todas las pruebas"""
    print("🚀 Iniciando pruebas de la API de Catálogo de Películas")
    print("=" * 60)
    
    # Esperar un poco para que la API esté lista
    print("⏳ Esperando que la API esté lista...")
    time.sleep(2)
    
    # Ejecutar pruebas
    test_health()
    
    if test_get_all_movies():
        test_get_top_movies()
        test_get_movie_by_id()

        
        # Crear, actualizar y eliminar película
        movie_id = test_create_movie()
        if movie_id:
            test_update_movie(movie_id)
            test_delete_movie(movie_id)
        
        # Probar casos de error
        test_invalid_requests()
        
        print("🎉 ¡Todas las pruebas completadas!")
        print("📊 La API está funcionando correctamente con todas las operaciones CRUD")
    else:
        print("❌ No se pudieron ejecutar todas las pruebas debido a errores iniciales")

if __name__ == "__main__":
    main()

    