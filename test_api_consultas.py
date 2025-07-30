import requests
import json
from datetime import date

def test_api_consultas():
    """Probar el endpoint de consultas del empleado"""
    
    base_url = "http://localhost:8000"
    empleado_id = 1  # Carlos Pérez
    
    print("🔍 Probando API de consultas...")
    
    try:
        # Probar consultas de hoy
        url = f"{base_url}/api/empleados/{empleado_id}/consultas-hoy"
        print(f"📡 Haciendo request a: {url}")
        
        response = requests.get(url, timeout=10)
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Respuesta exitosa:")
            print(json.dumps(data, indent=2, default=str))
            
            if 'consultas' in data:
                print(f"📋 Total consultas: {len(data['consultas'])}")
                for i, consulta in enumerate(data['consultas'], 1):
                    print(f"  {i}. ID: {consulta.get('idConsulta')}, Hora: {consulta.get('hora')}, Motivo: {consulta.get('motivo')}")
            else:
                print("⚠️  No se encontró la clave 'consultas' en la respuesta")
                
        else:
            print(f"❌ Error en la respuesta:")
            print(f"   Status: {response.status_code}")
            print(f"   Texto: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión - ¿Está el servidor corriendo?")
        print("   Intenta ejecutar: python -m uvicorn app.main:app --reload")
    except requests.exceptions.Timeout:
        print("❌ Timeout - El servidor tardó demasiado en responder")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    test_api_consultas()
