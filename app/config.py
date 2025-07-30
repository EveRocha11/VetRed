class ConfigGuayaquil:
    """Configuración para la base de datos de Guayaquil"""
    DRIVER   = '{ODBC Driver 17 for SQL Server}'
    SERVER   = 'DESKTOP-N4G4IF1'        
    DATABASE = 'VetRedGuayaquil'       
    UID      = 'Guayaquil'
    PWD      = 'Guayaquil'

    @classmethod
    def conn_str(cls):
        return (
            f"DRIVER={cls.DRIVER};"
            f"SERVER={cls.SERVER};"
            f"DATABASE={cls.DATABASE};"
            f"UID={cls.UID};PWD={cls.PWD}"
        )

class ConfigQuito:
    """Configuración para la base de datos de Quito"""
    DRIVER   = '{ODBC Driver 17 for SQL Server}'
    SERVER   = 'Geovanny'              # Servidor de Quito
    DATABASE = 'VetRedQuito'           # Base de datos de Quito
    UID      = 'Guayaquil'             # Usar credenciales que funcionan
    PWD      = 'Guayaquil'             # Usar credenciales que funcionan

    @classmethod
    def conn_str(cls):
        return (
            f"DRIVER={cls.DRIVER};"
            f"SERVER={cls.SERVER};"
            f"DATABASE={cls.DATABASE};"
            f"UID={cls.UID};PWD={cls.PWD}"
        )

# Mantener Config como alias de ConfigGuayaquil para compatibilidad
class Config(ConfigGuayaquil):
    """Alias para ConfigGuayaquil para mantener compatibilidad"""
    pass
