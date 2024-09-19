from myapp.authentication import GVMBackend
from django.db import connection

#Targets
def get_data_targets():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM targets")  # Modifica 'tua_tabella' con il nome corretto
        data = cursor.fetchall()
    return data