from django.db import connection
import datetime, time
import uuid

def get_data_tasks():
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM tasks')
        tasks = cursor.fetchall()
        tasks_dict = []
        # print(tasks)
        for row in tasks:
            tasks_data = {}
            if(row[4] == 0):
                # print(row)
                # print(row[4])
                tasks_data['id'] = row[0]
                tasks_data['name'] = row[3] if row[3] else 'Unknown'
                tasks_data['run_status'] = row[6] if row[6] else 0
                tasks_data['scanner'] = row[14] if row[14] else 0
                
                
                try:
                    end_time = row[8]
                    if end_time is None :
                        tasks_data['end_time'] = 'Data non disponibile'
                    elif end_time:
                        tasks_data['end_time'] = datetime.datetime.fromtimestamp(end_time)
                    else:
                        tasks_data['end_time'] = 'Data non disponibile'
                except (IndexError,ValueError,TypeError):
                    tasks_data['end_time'] = 'Data non disponibile'
                tasks_dict.append(tasks_data)
        
    return tasks_dict


# def create_task(name,target,scanner,config=12):
#     """
#     Crea un nuovo task di scansione e lo salva nel database
#     """
    
#     creation_time=int(time.time()) + 7200
#     target_uuid = str(uuid.uuid4()) 
#     with connection.cursor() as cursor:
#         owner=1
#         hidden=0
#         query = """
#         INSERT INTO tasks(uuid,owner,name,hidden,target,scanner,config,creation_time)
#         VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
#         """
#         cursor.execute(query,[target_uuid,owner,name,hidden,target,scanner,config,creation_time])

def create_task(name, target, scanner_id, config_id, schedule=0,schedule_next_time=0,schedule_periods=0,config_location=0,target_location=0,schedule_location=0,scanner_location=0,alterable=0, hosts_ordering='sequential',run_status=2):
    """
    Crea un nuovo task di scansione e lo salva nel database
    """
    creation_time = int(time.time()) + 7200
    target_uuid = str(uuid.uuid4())

    with connection.cursor() as cursor:
        owner = 1
        hidden = 0
        schedule = 0
        query = """
        INSERT INTO tasks (uuid, owner, name, hidden, comment,run_status, target, schedule,schedule_next_time,schedule_periods, config, scanner,config_location,target_location,schedule_location,scanner_location, hosts_ordering, alterable, creation_time, modification_time, usage_type) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, [target_uuid, owner, name, hidden, '',run_status, target, schedule,schedule_next_time,schedule_periods, config_id, scanner_id,config_location,target_location,schedule_location,scanner_location, hosts_ordering,alterable,creation_time, creation_time, 'scan'])
