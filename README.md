# Progetto OpenVAS Web Interface

Questo progetto fornisce un'interfaccia web per interagire con OpenVAS. L'interfaccia è sviluppata in Django e consente di gestire target, task di scansione. Questo README ti guiderà attraverso i passaggi necessari per configurare e avviare il progetto.

## Prerequisiti

1. **Python 3.8+**
2. **PostgreSQL** come database per OpenVAS.
3. **OpenVAS** configurato e funzionante sulla stessa rete, consiglio una macchina Virtuale.
4. **Chiavi SSH** configurate per la connessione alla VM con OpenVAS.

## Installazione

1. **Clona il repository**

    ```bash
    git clone <URL_DEL_REPOSITORY>
    cd <NOME_CARTELLA_REPOSITORY>
    ```

2. **Crea un ambiente virtuale**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Installa le dipendenze**:


    ```bash
    pip install -r requirements.txt
    ```

## Configurazione

### Configura le Variabili d'Ambiente

Copia il file `.env.exaple` e rinominalo `.env` nella root del progetto con le seguenti variabili per configurare la connessione SSH alla macchina OpenVAS e i dettagli del database PostgreSQL:

```dotenv
# Configurazione OpenVAS SSH
VM_IP='192.168.xx.xx'
VM_USERNAME='openvas'
PRIVATE_KEY_PATH='/path/to/private_key'

# Configurazione PostgreSQL
DB_NAME='nome_database'
DB_USER='nome_utente'
DB_PASSWORD='password'
DB_HOST='indirizzo_ip_database' # di solito lo stesso della VM
DB_PORT='porta_database'
```

### Configurazione di PostreSQL

Nel file postgresql.conf nella voce listen_addresses inserire il valore:

listen_addresses = '*'

Nel file pg_hba.conf nella voce IPv4 local connections inserire una stringa cosi strutturata:

host    all             all             ip_host/32       trust

## Avvio Progetto

Una volta effettuata le configurazioni puoi lanciare i seguenti comandi per provarlo:

```bash
    python3 manage.py runserver
    python3 manage.py livereload
    ```
