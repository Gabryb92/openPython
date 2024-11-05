'''
kali_ip='192.168.99.116'
kali_username = "openvas"
kali_password = "openvas"
private_key_path = '/home/gabrieledev/.ssh/id_rsa'
'''

import os
from dotenv import load_dotenv

load_dotenv()

kali_ip = os.getenv('KALI_IP')
kali_username = os.getenv('KALI_USERNAME')
kali_password = os.getenv('KALI_PASSWORD')
private_key_path = os.getenv('PRIVATE_KEY_PATH')