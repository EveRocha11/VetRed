import requests
import json

def test_actualizacion_consulta():
    """Probar la actualización de estado y observaciones de consultas"""
    
    base_url = "http://127.0.0.1:8000"
    
    print("🧪 PROBANDO ACTUALIZACIÓN DE CONSULTAS")
    print("=" * 50)
    
    # Primero obtener algunas consultas para Carlos Pérez
    print("📋 Obteniendo consultas del empleado 1...")
    
    try:
        response = requests.get(f"{base_url}/api/empleados/1/consultas-hoy")
        if response.status_code == 200:
            data = response.json()
            consultas = data.get('consultas', [])
            
            if consultas:
                consulta_test = consultas[0]  # Tomar la primera consulta
                id_consulta = consulta_test['idConsulta']
                estado_actual = consulta_test['estado']
                
                print(f"  ✅ Consulta seleccionada: ID {id_consulta}")
                print(f"  📊 Estado actual: {estado_actual}")
                print(f"  🕐 Hora: {consulta_test['hora']}")
                print(f"  📝 Motivo: {consulta_test['motivo']}")
                
                # Test 1: Cambiar estado
                print(f"\n🔄 PROBANDO CAMBIO DE ESTADO...")
                nuevo_estado = "Completado" if estado_actual == "Pendiente" else "Pendiente"
                
                response_estado = requests.put(
                    f"{base_url}/api/empleados/consultas/{id_consulta}/estado",
                    json={"estado": nuevo_estado},
                    headers={"Content-Type": "application/json"}
                )
                
                print(f"  📡 Request a: /api/empleados/consultas/{id_consulta}/estado")
                print(f"  📤 Enviando estado: {nuevo_estado}")
                print(f"  📊 Status Code: {response_estado.status_code}")
                
                if response_estado.status_code == 200:
                    print(f"  ✅ Estado actualizado exitosamente")
                    result = response_estado.json()
                    print(f"  📄 Respuesta: {result}")
                else:
                    print(f"  ❌ Error actualizando estado: {response_estado.text}")
                
                # Test 2: Actualizar observaciones
                print(f"\n📝 PROBANDO ACTUALIZACIÓN DE OBSERVACIONES...")
                observaciones_test = f"Observación de prueba - {consulta_test['motivo']} - Actualizado correctamente"
                
                response_obs = requests.put(
                    f"{base_url}/api/empleados/consultas/{id_consulta}/observaciones",
                    json={"observaciones": observaciones_test},
                    headers={"Content-Type": "application/json"}
                )
                
                print(f"  📡 Request a: /api/empleados/consultas/{id_consulta}/observaciones")
                print(f"  📤 Enviando observaciones: {observaciones_test[:50]}...")
                print(f"  📊 Status Code: {response_obs.status_code}")
                
                if response_obs.status_code == 200:
                    print(f"  ✅ Observaciones actualizadas exitosamente")
                    result = response_obs.json()
                    print(f"  📄 Respuesta: {result}")
                else:
                    print(f"  ❌ Error actualizando observaciones: {response_obs.text}")
                
                # Verificar que los cambios se guardaron
                print(f"\n🔍 VERIFICANDO CAMBIOS...")
                response_verify = requests.get(f"{base_url}/api/empleados/1/consultas-hoy")
                if response_verify.status_code == 200:
                    data_verify = response_verify.json()
                    consultas_verify = data_verify.get('consultas', [])
                    
                    consulta_actualizada = next((c for c in consultas_verify if c['idConsulta'] == id_consulta), None)
                    if consulta_actualizada:
                        print(f"  📊 Estado verificado: {consulta_actualizada['estado']}")
                        print(f"  📝 Observaciones verificadas: {consulta_actualizada['observaciones'][:50] if consulta_actualizada['observaciones'] else 'Sin observaciones'}...")
                        
                        if consulta_actualizada['estado'] == nuevo_estado:
                            print(f"  ✅ Estado se actualizó correctamente")
                        else:
                            print(f"  ❌ Estado no se actualizó (esperado: {nuevo_estado}, actual: {consulta_actualizada['estado']})")
                    else:
                        print(f"  ❌ No se encontró la consulta actualizada")
                
            else:
                print("  ❌ No hay consultas para probar")
        else:
            print(f"  ❌ Error obteniendo consultas: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión - ¿Está el servidor corriendo?")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    test_actualizacion_consulta()
