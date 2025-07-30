"""
Script para verificar que ambas tablas funcionan correctamente
"""
from app.repositories.cliente_contacto import ClienteContactoRepository
from app.repositories.cliente_info import cliente_info_repository
from app.models import ClienteContacto, ClienteInfo
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_both_tables():
    """Probar ambas tablas en VetRedGuayaquil"""
    try:
        # 1. Probar Cliente_Info (para login/registro)
        logger.info("🔍 Probando Cliente_Info...")
        clientes_info = cliente_info_repository.list()
        logger.info(f"✅ Cliente_Info: {len(clientes_info)} registros")
        for cliente in clientes_info[:3]:
            logger.info(f"  - ID: {cliente.idCliente}, Email: {cliente.correo}, Nombre: {cliente.nombre}")
        
        # 2. Probar Cliente_Contacto (para gestión de contactos)
        logger.info("\n🔍 Probando Cliente_Contacto...")
        repo_contacto = ClienteContactoRepository()
        clientes_contacto = repo_contacto.list()
        logger.info(f"✅ Cliente_Contacto: {len(clientes_contacto)} registros")
        for cliente in clientes_contacto[:3]:
            logger.info(f"  - ID: {cliente.idCliente}, Email: {cliente.correo}, Dirección: {cliente.direccion}")
        
        # 3. Probar crear un nuevo contacto
        logger.info("\n🔍 Probando crear nuevo contacto...")
        nuevo_contacto = ClienteContacto(
            idCliente=999,
            correo="test@contacto.com",
            direccion="Dirección de prueba",
            telefono="0999999999"
        )
        
        try:
            resultado = repo_contacto.create(nuevo_contacto)
            logger.info(f"✅ Contacto creado: {resultado.correo}")
            
            # Verificar que se guardó
            clientes_actualizado = repo_contacto.list()
            logger.info(f"✅ Total contactos después de crear: {len(clientes_actualizado)}")
            
        except Exception as e:
            logger.warning(f"⚠️ No se pudo crear contacto de prueba (posiblemente ya existe): {e}")
        
        logger.info("\n🎯 Resumen:")
        logger.info("  ✅ Cliente_Info: Para autenticación (login/registro)")
        logger.info("  ✅ Cliente_Contacto: Para gestión de información de contacto")
        logger.info("  ✅ Ambas tablas están en VetRedGuayaquil")
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")

if __name__ == "__main__":
    test_both_tables()
