from app.db import db_guayaquil
from app.repositories.cliente_contacto import ClienteContactoRepository

# Probar conexión directa a la tabla
try:
    cursor = db_guayaquil.cursor()
    cursor.execute('SELECT COUNT(*) FROM Cliente_Contacto')
    count = cursor.fetchone()[0]
    print(f'Total clientes en tabla: {count}')
    
    if count > 0:
        cursor.execute('SELECT * FROM Cliente_Contacto')
        rows = cursor.fetchall()
        print('Datos en la tabla:')
        for row in rows:
            print(row)
    else:
        print('La tabla está vacía')
        
    # Probar a través del repository
    repo = ClienteContactoRepository()
    clientes = repo.list()
    print(f'\nClientes desde repository: {len(clientes)}')
    for cliente in clientes:
        print(cliente)
        
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
