import requests
import json

def test_consultas_empleados():
    """Probar consultas para diferentes empleados"""
    
    base_url = "http://127.0.0.1:8000"
    
    # Lista de empleados a probar (según lo que vimos en el script anterior)
    empleados_test = [
        {"id": 1, "nombre": "Carlos Pérez", "sede": "Quito"},
        {"id": 2, "nombre": "Ana Gómez", "sede": "Quito"},
        {"id": 6, "nombre": "Luis Martínez", "sede": "Quito"},
        {"id": 3, "nombre": "Juan López", "sede": "Guayaquil"},
        {"id": 4, "nombre": "Maria Silva", "sede": "Guayaquil"},
    ]
    
    print("🔍 PROBANDO CONSULTAS PARA DIFERENTES EMPLEADOS")
    print("=" * 60)
    
    for empleado in empleados_test:
        print(f"\n👨‍⚕️ Empleado: {empleado['nombre']} (ID: {empleado['id']}) - {empleado['sede']}")
        
        try:
            url = f"{base_url}/api/empleados/{empleado['id']}/consultas-hoy"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                consultas = data.get('consultas', [])
                
                if consultas:
                    print(f"  ✅ {len(consultas)} consultas encontradas:")
                    for i, consulta in enumerate(consultas, 1):
                        print(f"    {i}. {consulta.get('hora')} - {consulta.get('motivo')} ({consulta.get('estado')})")
                        print(f"       Mascota: {consulta.get('mascota_nombre')} ({consulta.get('mascota_tipo')})")
                else:
                    print(f"  ❌ Sin consultas para hoy")
                    
            else:
                print(f"  ❌ Error {response.status_code}: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"  ❌ Error de conexión - ¿Está el servidor corriendo?")
            break
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_consultas_empleados()
