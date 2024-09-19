#from myapp.authentication import GVMBackend
from django.db import connection
import datetime
import uuid

#Targets
def get_data_targets():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM targets")  # Modifica 'tua_tabella' con il nome corretto
        targets = cursor.fetchall()
        #targets_dict = [{'name': row[3],'host': row[4],'portLists':row[9],'create':datetime.datetime.fromtimestamp(row[12])} for row in targets]
        targets_dict = []
        
        for row in targets:
            target_data = {}
            
            target_data['name'] = row[3] if row[3] else 'Unknown' # Nome del target
            target_data['host'] = row[4] if row[4] else 'No Host' # Host non associato
            target_data['portLists'] = row[9] if len(row) > 9 and row[9] else 'No PortList'
            
            try:
                creation_time = row[12]
                if creation_time:
                    target_data['creation_time'] = datetime.datetime.fromtimestamp(creation_time)
                else:
                    target_data['creation_time'] = 'Data non disponibile'
            except (IndexError,ValueError,TypeError):
                target_data['creation_time'] = "Data non disponibile"

            targets_dict.append(target_data)
    return targets_dict

def create_target(name,hosts):
    target_uuid = str(uuid.uuid4())
    """
    Funzione che esegue una query SQL per inserire un nuovo target nel database
    """
    with connection.cursor() as cursor:
        owner = 1
        query = """
        INSERT INTO targets (uuid,owner,hosts,name)
        VALUES (%s, %s ,%s , %s)
        """
        cursor.execute(query,[target_uuid,owner,name,hosts])