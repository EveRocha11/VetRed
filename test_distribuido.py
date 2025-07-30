"""
Script para probar el sistema de conexiones distribuidas
"""
from app.database_router import db_router
from app.repositories.cliente_info import ClienteInfoRepository
from app.repositories.cliente_contacto import ClienteContactoRepository
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_distributed_connections():
    """Probar el sistema de conexiones distribuidas"""
    
    print("🚀 Probando Sistema de Conexiones Distribuidas VetRed")
    print("=" * 60)
    
    # 1. Verificar estado de conexiones
    print("\n1️⃣ Estado de Conexiones:")
    health = db_router.health_check()
    print(f"   Guayaquil: {'✅ Conectado' if health['guayaquil'] else '❌ Desconectado'}")
    print(f"   Quito: {'✅ Conectado' if health['quito'] else '❌ Desconectado'}")
    print(f"   Total conexiones activas: {health['total_connections']}")
    
    # 2. Información detallada de conexiones
    print("\n2️⃣ Información de Servidores:")
    connections = db_router.get_available_connections()
    for location, info in connections.items():
        print(f"   {location.capitalize()}: {info['servidor']} / {info['base_datos']}")
    
    # 3. Probar Cliente_Info (Autenticación)
    print("\n3️⃣ Probando Cliente_Info (Autenticación):")
    try:
        auth_repo = ClienteInfoRepository()
        clientes_info = auth_repo.list()
        print(f"   ✅ {len(clientes_info)} registros en Cliente_Info")
        
        # Mostrar algunos registros
        for cliente in clientes_info[:3]:
            print(f"      - ID: {cliente.idCliente}, Email: {cliente.correo}, Nombre: {cliente.nombre}")
            
    except Exception as e:
        print(f"   ❌ Error con Cliente_Info: {e}")
    
    # 4. Probar Cliente_Contacto
    print("\n4️⃣ Probando Cliente_Contacto:")
    try:
        contacto_repo = ClienteContactoRepository()
        clientes_contacto = contacto_repo.list()
        print(f"   ✅ {len(clientes_contacto)} registros en Cliente_Contacto")
        
        # Mostrar algunos registros
        for cliente in clientes_contacto[:3]:
            print(f"      - ID: {cliente.idCliente}, Email: {cliente.correo}, Dir: {cliente.direccion}")
            
    except Exception as e:
        print(f"   ❌ Error con Cliente_Contacto: {e}")
    
    # 5. Resumen del enrutamiento
    print("\n5️⃣ Configuración de Enrutamiento:")
    print("   📋 Cliente_Info (Auth): ", end="")
    auth_db = db_router.get_auth_db()
    if auth_db:
        auth_info = auth_db.test_connection()
        print(f"{auth_info['servidor']}/{auth_info['base_datos']}")
    else:
        print("❌ No disponible")
    
    print("   📋 Cliente_Contacto: ", end="")
    contacto_db = db_router.get_cliente_contacto_db()
    if contacto_db:
        contacto_info = contacto_db.test_connection()
        print(f"{contacto_info['servidor']}/{contacto_info['base_datos']}")
    else:
        print("❌ No disponible")
    
    print("\n" + "=" * 60)
    print("🎯 Sistema configurado para:")
    print("   - Login/Registro: usa Cliente_Info")
    print("   - Gestión Contactos: usa Cliente_Contacto")
    print("   - Failover automático si Quito no está disponible")

if __name__ == "__main__":
    test_distributed_connections()
