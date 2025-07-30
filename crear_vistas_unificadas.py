import pyodbc
from app.config import ConfigQuito, ConfigGuayaquil

def crear_vistas_unificadas():
    """Crear vistas unificadas para consultas y empleados"""
    
    print("🔧 CREANDO VISTAS UNIFICADAS...")
    
    try:
        # VISTA EN QUITO
        print("\n📊 Creando vistas en base de datos de Quito...")
        conn_quito = pyodbc.connect(ConfigQuito.conn_str())
        cursor = conn_quito.cursor()
        
        # Vista para Empleados unificada
        vista_empleados_quito = """
        IF OBJECT_ID('dbo.Empleado', 'V') IS NOT NULL
            DROP VIEW dbo.Empleado;
        """
        
        crear_vista_empleados_quito = """
        CREATE VIEW dbo.Empleado AS
        SELECT 
            idEmpleado,
            nombre,
            direccion,
            salario,
            fechaContratacion,
            idClinica,
            'Quito' as sede
        FROM Empleado_Quito
        """
        
        # Vista para Consultas unificada
        vista_consultas_quito = """
        IF OBJECT_ID('dbo.Consulta', 'V') IS NOT NULL
            DROP VIEW dbo.Consulta;
        """
        
        crear_vista_consultas_quito = """
        CREATE VIEW dbo.Consulta AS
        SELECT 
            c.idConsulta,
            c.fecha,
            c.hora,
            c.motivo,
            c.estado,
            c.observaciones,
            c.idClinica,
            c.idEmpleado,
            c.idMascota,
            m.nombre as mascota_nombre,
            m.especie as mascota_tipo,
            'Cliente de ' + m.nombre as cliente_nombre,
            'Quito' as sede
        FROM Consulta_Quito c
        LEFT JOIN Mascota m ON m.idMascota = c.idMascota
        """
        
        try:
            cursor.execute(vista_empleados_quito)
            cursor.execute(crear_vista_empleados_quito)
            print("  ✅ Vista dbo.Empleado creada en Quito")
            
            cursor.execute(vista_consultas_quito)
            cursor.execute(crear_vista_consultas_quito)
            print("  ✅ Vista dbo.Consulta creada en Quito")
            
            conn_quito.commit()
        except Exception as e:
            print(f"  ❌ Error creando vistas en Quito: {e}")
        
        cursor.close()
        conn_quito.close()
        
        # VISTA EN GUAYAQUIL
        print("\n📊 Creando vistas en base de datos de Guayaquil...")
        try:
            conn_guayaquil = pyodbc.connect(ConfigGuayaquil.conn_str())
            cursor = conn_guayaquil.cursor()
            
            # Vista para Empleados unificada
            vista_empleados_guayaquil = """
            IF OBJECT_ID('dbo.Empleado', 'V') IS NOT NULL
                DROP VIEW dbo.Empleado;
            """
            
            crear_vista_empleados_guayaquil = """
            CREATE VIEW dbo.Empleado AS
            SELECT 
                idEmpleado,
                nombre,
                direccion,
                salario,
                fechaContratacion,
                idClinica,
                'Guayaquil' as sede
            FROM Empleado_Guayaquil
            """
            
            # Vista para Consultas unificada
            vista_consultas_guayaquil = """
            IF OBJECT_ID('dbo.Consulta', 'V') IS NOT NULL
                DROP VIEW dbo.Consulta;
            """
            
            crear_vista_consultas_guayaquil = """
            CREATE VIEW dbo.Consulta AS
            SELECT 
                c.idConsulta,
                c.fecha,
                c.hora,
                c.motivo,
                c.estado,
                c.observaciones,
                c.idClinica,
                c.idEmpleado,
                c.idMascota,
                m.nombre as mascota_nombre,
                m.especie as mascota_tipo,
                'Cliente de ' + m.nombre as cliente_nombre,
                'Guayaquil' as sede
            FROM Consulta_Guayaquil c
            LEFT JOIN Mascota m ON m.idMascota = c.idMascota
            """
            
            cursor.execute(vista_empleados_guayaquil)
            cursor.execute(crear_vista_empleados_guayaquil)
            print("  ✅ Vista dbo.Empleado creada en Guayaquil")
            
            cursor.execute(vista_consultas_guayaquil)
            cursor.execute(crear_vista_consultas_guayaquil)
            print("  ✅ Vista dbo.Consulta creada en Guayaquil")
            
            conn_guayaquil.commit()
            cursor.close()
            conn_guayaquil.close()
            
        except Exception as e:
            print(f"  ❌ Error creando vistas en Guayaquil: {e}")
        
        print("\n✅ Vistas unificadas creadas exitosamente")
        
        # Verificar las vistas
        print("\n🔍 VERIFICANDO VISTAS CREADAS...")
        
        # Verificar en Quito
        conn_quito = pyodbc.connect(ConfigQuito.conn_str())
        cursor = conn_quito.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM dbo.Empleado")
        empleados_quito = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM dbo.Consulta WHERE fecha = '2025-07-30'")
        consultas_quito = cursor.fetchone()[0]
        
        print(f"  📊 Quito - Empleados en vista: {empleados_quito}")
        print(f"  📊 Quito - Consultas hoy en vista: {consultas_quito}")
        
        cursor.close()
        conn_quito.close()
        
        # Verificar en Guayaquil
        try:
            conn_guayaquil = pyodbc.connect(ConfigGuayaquil.conn_str())
            cursor = conn_guayaquil.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM dbo.Empleado")
            empleados_guayaquil = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM dbo.Consulta WHERE fecha = '2025-07-30'")
            consultas_guayaquil = cursor.fetchone()[0]
            
            print(f"  📊 Guayaquil - Empleados en vista: {empleados_guayaquil}")
            print(f"  📊 Guayaquil - Consultas hoy en vista: {consultas_guayaquil}")
            
            cursor.close()
            conn_guayaquil.close()
            
        except Exception as e:
            print(f"  ❌ Error verificando Guayaquil: {e}")
        
    except Exception as e:
        print(f"❌ Error general: {e}")

if __name__ == "__main__":
    crear_vistas_unificadas()
