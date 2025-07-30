import requests
import json

def test_vistas_unificadas():
    """Probar el sistema usando vistas unificadas"""
    
    base_url = "http://127.0.0.1:8000"
    
    print("🔧 PROBANDO SISTEMA CON VISTAS UNIFICADAS")
    print("=" * 60)
    
    # Lista de empleados a probar
    empleados_test = [
        {"id": 1, "nombre": "Carlos Pérez", "sede_esperada": "Quito"},
        {"id": 2, "nombre": "Ana Gómez", "sede_esperada": "Quito"},
        {"id": 3, "nombre": "Juan López", "sede_esperada": "Guayaquil"},
        {"id": 4, "nombre": "Maria Silva", "sede_esperada": "Guayaquil"},
        {"id": 6, "nombre": "Luis Martínez", "sede_esperada": "Quito"},
    ]
    
    for empleado in empleados_test:
        print(f"\n👨‍⚕️ Probando empleado: {empleado['nombre']} (ID: {empleado['id']})")
        print(f"   Sede esperada: {empleado['sede_esperada']}")
        
        try:
            # Obtener consultas de hoy
            url = f"{base_url}/api/empleados/{empleado['id']}/consultas-hoy"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                consultas = data.get('consultas', [])
                
                print(f"   ✅ Respuesta exitosa: {len(consultas)} consultas")
                
                if consultas:
                    # Mostrar algunas consultas
                    for i, consulta in enumerate(consultas[:2], 1):  # Solo las primeras 2
                        print(f"     {i}. {consulta.get('hora')} - {consulta.get('motivo')} ({consulta.get('estado')})")
                        print(f"        Mascota: {consulta.get('mascota_nombre')} ({consulta.get('mascota_tipo')})")
                    
                    # Probar actualización de estado con la primera consulta
                    if len(consultas) > 0:
                        consulta_test = consultas[0]
                        id_consulta = consulta_test['idConsulta']
                        estado_actual = consulta_test['estado']
                        nuevo_estado = "Completado" if estado_actual == "Pendiente" else "Pendiente"
                        
                        print(f"   🔄 Probando cambio de estado de consulta {id_consulta}: {estado_actual} → {nuevo_estado}")
                        
                        response_estado = requests.put(
                            f"{base_url}/api/empleados/consultas/{id_consulta}/estado",
                            json={"estado": nuevo_estado},
                            headers={"Content-Type": "application/json"}
                        )
                        
                        if response_estado.status_code == 200:
                            print(f"     ✅ Estado actualizado correctamente")
                            
                            # Verificar el cambio
                            response_verify = requests.get(url)
                            if response_verify.status_code == 200:
                                data_verify = response_verify.json()
                                consultas_verify = data_verify.get('consultas', [])
                                consulta_actualizada = next((c for c in consultas_verify if c['idConsulta'] == id_consulta), None)
                                
                                if consulta_actualizada and consulta_actualizada['estado'] == nuevo_estado:
                                    print(f"     ✅ Verificación exitosa: estado cambió a {nuevo_estado}")
                                else:
                                    print(f"     ❌ Verificación falló: estado no cambió")
                        else:
                            print(f"     ❌ Error actualizando estado: {response_estado.status_code}")
                            print(f"     📄 Respuesta: {response_estado.text}")
                        
                        # Probar actualización de observaciones
                        observaciones_test = f"Observación de prueba con vistas - {consulta_test['motivo']}"
                        
                        print(f"   📝 Probando actualización de observaciones...")
                        
                        response_obs = requests.put(
                            f"{base_url}/api/empleados/consultas/{id_consulta}/observaciones",
                            json={"observaciones": observaciones_test},
                            headers={"Content-Type": "application/json"}
                        )
                        
                        if response_obs.status_code == 200:
                            print(f"     ✅ Observaciones actualizadas correctamente")
                        else:
                            print(f"     ❌ Error actualizando observaciones: {response_obs.status_code}")
                else:
                    print(f"   ℹ️  Sin consultas para hoy")
                    
            else:
                print(f"   ❌ Error obteniendo consultas: {response.status_code}")
                print(f"   📄 Respuesta: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("   ❌ Error de conexión - ¿Está el servidor corriendo?")
            break
        except Exception as e:
            print(f"   ❌ Error inesperado: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Prueba de vistas unificadas completada")

if __name__ == "__main__":
    test_vistas_unificadas()
