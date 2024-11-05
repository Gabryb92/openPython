# OpenVAS Web Interface Project

This project provides a web interface to interact with OpenVAS. The interface is developed in Django and allows you to manage targets and scan tasks. This README will guide you through the necessary steps to set up and start the project.

## Prerequisites

- **Python 3.8+**
- **Django**: Ensure that Django is installed on your machine.
- **Python**: Version 3.12 or later.
- **PostgreSQL**: Make sure the database is properly configured and running.
- **OpenVAS**: This project is designed to interface with OpenVAS.

## Installation

1. **Clone the repository**

    ```bash
    git clone <REPOSITORY_URL>
    cd <REPOSITORY_FOLDER_NAME>
    ```

2. **Create a virtual environment**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

### Configure Environment Variables

Copy the `.env.example` file and rename it to `.env` in the root of the project with the following variables to configure the SSH connection to the OpenVAS machine and PostgreSQL database details:

```dotenv
# OpenVAS SSH Configuration
VM_IP='192.168.xx.xx'
VM_USERNAME='openvas'
PRIVATE_KEY_PATH='/path/to/private_key'

# PostgreSQL Configuration
DB_NAME='database_name'
DB_USER='username'
DB_PASSWORD='password'
DB_HOST='database_ip_address' # usually the same as the VM
DB_PORT='database_port'
```

### PostgreSQL Configuration

In the `postgresql.conf` file, set the value for `listen_addresses` as follows:
```bash
listen_addresses = '*'
```

In the `pg_hba.conf` file under IPv4 local connections, add a line structured like this:

```bash
host    all             all             ip_host/32       trust
```

## Starting the Project

Once the configurations are complete, you can run the following commands to test it:

```bash
python3 manage.py runserver
python3 manage.py livereload
```
