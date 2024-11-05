import paramiko
import re
import json
from myapp.utils.vm_data import *

#Vm Kali
# kali_ip='192.168.79.113'
# kali_username = "openvas"
# kali_password = "openvas"
# private_key_path = '/home/gabrieledev/.ssh/id_rsa'


def get_main_interface_and_ip(ssh):
    """
    Ottiene l'interfaccia attiva e il suo indirizzo IP dalla VM remota.
    """
    # Esecuzione del comando per ottenere l'interfaccia di rete attiva e il suo indirizzo IP
    stdin, stdout, stderr = ssh.exec_command(
        'ip a | awk \'/state UP/ {gsub(":", "", $2); iface=$2} /inet / && iface {split($2, ip, "/"); print iface, ip[1]; iface=""}\''
    )
    result = stdout.read().decode().strip()

    if not result:
        print("Errore: Impossibile trovare un'interfaccia attiva o un indirizzo IP.")
        return None, None

    # Dividere la stringa per ottenere l'interfaccia e l'IP
    interface, ip_address = result.split()

    return interface, ip_address

def ipcalc(ssh,ip):
    ipcalc_command = f"ipcalc {ip} | grep -E 'Network|HostMin|HostMax|Broadcast' | awk '{{print $2}}'"
    stdin, stdout, stderr = ssh.exec_command(ipcalc_command)
    ipcalc_output = stdout.read().decode().splitlines()
    network_subnet,host_min,host_max,broadcast = ipcalc_output
    # print(ipcalc_output)
    network = network_subnet.split('/')[0]
    subnetmask = network_subnet.split('/')[1]
    print(network,subnetmask)
    return [network,subnetmask,host_min,host_max,broadcast]
    

def parse_netdiscover_output(output):
    """
    Funzione per parsare l'output di netdiscover.
    Estrae IP, MAC Address e MAC Vendor.
    """
    devices = []
    
    # Dividi l'output in righe
    lines = output.splitlines()
    for i, line in enumerate(lines[2:-1]):
        columns = line.split()  # Dividi la riga in colonne
        if len(columns) >= 6:  
            ip = columns[0]
            mac_address = columns[1]
            mac_vendor = " ".join(columns[4:])  # Cattura tutte le colonne del mac vendor
            device_info = {
                "IP": ip,
                "MAC_Address": mac_address,
                "MAC_Vendor": mac_vendor
            }
            devices.append(device_info)  # Aggiungi il dispositivo alla lista

    # Converti in JSON
    json_output = json.dumps(devices, indent=4)
    #print(json)
    #print(device_info)
    return json_output


def execute_netdiscover(ssh,interface,ipcalc):
    '''Lancia il comando netdiscover per visualizzare la lista dei dispositivi connessi alla rete'''
    # Step 3: Esegui 'netdiscover' sull'interfaccia principale
    #print(ipcalc)
    network,subnetmask,_ ,_ ,broadcast = ipcalc
    netdiscover_command = f'sudo netdiscover -i {interface} -r {network}/{subnetmask}-{broadcast}/{subnetmask} -P'
    stdin, stdout, stderr = ssh.exec_command(netdiscover_command)
    netdiscover_output = stdout.read().decode()
    #print(netdiscover_output)
    devices = parse_netdiscover_output(netdiscover_output)
    return devices


def execute_ssh_command(command,task_uuid=""):
    # Instanzia un client SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        
        # Connessione alla VM Kali
        ssh.connect(kali_ip, username=kali_username, key_filename=private_key_path)
        
        if command == "hosts":
            #Ottengo il nome dell'interfaccia e l'ip
            main_interface,ip_address = get_main_interface_and_ip(ssh)
            ipcalc_output = ipcalc(ssh,ip_address)
            devices_json = execute_netdiscover(ssh,main_interface,ipcalc_output)
            devices = json.loads(devices_json)
            

            return devices
        elif command == 'scan':
            scan_command = f"""sudo -u _gvm gvm-cli --gmp-username "admin" --gmp-password "password" socket --xml "<start_task task_id='{task_uuid}'/>" """
            
            stdin,stdout,stderr = ssh.exec_command(scan_command)
            
            #Recupera output e errori
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')
            
            if error:
                raise Exception(f"Errore esecuzione comando di scansione: {error}")
            return output.strip()
        
        elif command == 'status':
            status_command = f"""sudo -u _gvm gvm-cli --gmp-username "admin" --gmp-password "password"  socket --xml "<get_tasks task_id='{task_uuid}'/>" """
            
            stdin, stdout, stderr = ssh.exec_command(status_command)
            result = stdout.read().decode()
            return result
        
    except paramiko.SSHException as ssh_error:
        raise Exception(f"Errore di connessione SSH: {ssh_error}")

    except Exception as e:
        raise Exception(f"Errore generale: {e}")
    
    # Chiudi la connessione SSH
    finally:
        ssh.close()


def create_ssh_connection():
    '''
    Funzione per creare una connessione SSH alla VM, restituisce un oggetto Paramiko SSHClient
    '''
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        #Stabiliamo la connessione
        ssh.connect(kali_ip,kali_username,private_key_path)
        print("Connessione SSH stabilita")
        return ssh
    except Exception as e:
        print(f"Errore durante la connessione SSH: {e}")
        return None
    
def close_ssh_connection(ssh):
    """
    Funzione per chiudere la connessione SSH
    """
    
    if ssh:
        ssh.close()
        print("Connessione SSH chiusa con successo")