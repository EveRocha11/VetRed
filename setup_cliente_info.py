"""
Script para configurar la tabla Cliente_Info en la base de datos
"""
from app.db import db_guayaquil
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_cliente_info_table():
    """Crear la tabla Cliente_Info y insertar datos de prueba"""
    cursor = None
    try:
        cursor = db_guayaquil.cursor()
        
        # 1. Crear la tabla Cliente_Info
        logger.info("Creando tabla Cliente_Info...")
        create_table_sql = """
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Cliente_Info' AND xtype='U')
        CREATE TABLE Cliente_Info (
            idCliente INT,
            correo VARCHAR(100),
            nombre VARCHAR(100) NOT NULL,
            PRIMARY KEY (idCliente, correo)
        );
        """
        cursor.execute(create_table_sql)
        cursor.commit()
        logger.info("✅ Tabla Cliente_Info creada exitosamente")
        
        # 2. Verificar si ya hay datos
        cursor.execute("SELECT COUNT(*) FROM Cliente_Info")
        count = cursor.fetchone()[0]
        
        if count == 0:
            logger.info("Insertando datos de prueba...")
            
            # 3. Insertar datos de prueba
            test_data = [
                (1, 'lucia@example.com', 'Lucia García'),
                (2, 'carlos@example.com', 'Carlos Mendoza'),
                (3, 'ana@example.com', 'Ana Rodriguez'),
                (4, 'pedro@example.com', 'Pedro Santos'),
                (5, 'maria@example.com', 'María López'),
                (6, 'juan@example.com', 'Juan Pérez'),
                (7, 'sofia@example.com', 'Sofía Martín'),
                (8, 'diego@example.com', 'Diego Fernández'),
                (9, 'laura@example.com', 'Laura González'),
                (10, 'admin@vetclinic.com', 'Christian Puchaicela')
            ]
            
            insert_sql = "INSERT INTO Cliente_Info (idCliente, correo, nombre) VALUES (?, ?, ?)"
            
            for data in test_data:
                cursor.execute(insert_sql, data)
            
            cursor.commit()
            logger.info(f"✅ {len(test_data)} registros insertados exitosamente")
        else:
            logger.info(f"La tabla ya contiene {count} registros")
        
        # 4. Mostrar algunos datos para verificación
        cursor.execute("SELECT TOP 5 idCliente, correo, nombre FROM Cliente_Info")
        rows = cursor.fetchall()
        
        logger.info("Primeros 5 registros en Cliente_Info:")
        for row in rows:
            logger.info(f"  ID: {row[0]}, Correo: {row[1]}, Nombre: {row[2]}")
            
    except Exception as e:
        logger.error(f"Error configurando Cliente_Info: {e}")
        raise
    finally:
        if cursor:
            cursor.close()

if __name__ == "__main__":
    setup_cliente_info_table()
    print("\n🎉 Configuración completada. Puedes probar el login con:")
    print("   Correo: lucia@example.com")
    print("   ID Cliente: 1")
    print("\n   O con:")
    print("   Correo: admin@vetclinic.com")
    print("   ID Cliente: 10")
