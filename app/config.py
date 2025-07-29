class Config:
    DRIVER   = '{ODBC Driver 17 for SQL Server}'
    SERVER   = 'DESKTOP-N4G4IF1'        # o 'Geovanny' según uses
    DATABASE = 'VetRedGuayaquil'       # o 'VetRedQuito'
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
