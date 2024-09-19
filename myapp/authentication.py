#Autenticazione con utente GVM di openvas
import crypt
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.db import connection

class GVMBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        # Connessione al database GVM per ottenere l'hash della password
        with connection.cursor() as cursor:
            cursor.execute('SELECT password FROM users WHERE name=%s', [username])
            row = cursor.fetchone()

            if row:
                stored_hash = row[0]  # Ottieni l'hash della password dal database
                
                # Genera l'hash della password inserita dall'utente
                generated_hash = crypt.crypt(password, stored_hash)

                # Confronta gli hash e autentica l'utente
                if generated_hash == stored_hash:
                    try:
                        # Verifica se l'utente esiste nel database Django
                        user = User.objects.get(username=username)
                    except User.DoesNotExist:
                        # Se l'utente non esiste, crealo nel database Django
                        user = User(username=username)
                        user.set_password(password)  # Salva la password per Django
                        user.save()
                    return user

        # Le credenziali non corrispondono, ritorna None
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None