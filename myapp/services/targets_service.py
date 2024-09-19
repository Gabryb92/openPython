#from myapp.authentication import GVMBackend
from django.db import connection
import datetime

#Targets
def get_data_targets():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM targets")  # Modifica 'tua_tabella' con il nome corretto
        targets = cursor.fetchall()
        targets_dict = [{'name': row[3],'host': row[4],'portLists':row[9],'create':datetime.datetime.fromtimestamp(row[12])} for row in targets]
    return targets_dict

