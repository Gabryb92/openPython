import paramiko
from gvm.protocols.gmp import Gmp
from gvm.connections import SSHConnection
from gvm.transforms import EtreeTransform
from gvm.errors import GvmError
from utils.ssh_connection import create_ssh_connection, close_ssh_connection


# Credenziali per OpenVAS
openvas_username = 'admin'
openvas_password = 'password'

# Percorso del socket di OpenVAS (modifica se necessario)
socket_path = '/var/run/gvmd.sock'

def get_scanners():
    """ Funzione per ottenere la lista degli scanner da OpenVAS """
    
    scanners = []
    try:
        # Usa SSHConnection per connettersi a OpenVAS
        connection = SSHConnection(hostname=hostname, username=username, private_key_file=private_key_path)
        
        # Usa Gmp per autenticarsi e ottenere gli scanner
        with Gmp(connection=connection) as gmp:
            gmp.authenticate(username, password)  # Autenticazione
            response = gmp.get_scanners()  # Ottieni gli scanner
            
            # Parso la risposta per ottenere i dettagli degli scanner
            for scanner in response.xpath('scanner'):
                scanner_id = scanner.get('id')
                scanner_name = scanner.findtext('name')
                scanners.append({'id': scanner_id, 'name': scanner_name})

    except Exception as e:
        print(f"Errore nella connessione: {e}")
    
    return scanners
