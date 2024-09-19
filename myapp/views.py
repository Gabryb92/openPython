from django.shortcuts import render,redirect
from django.db import connection
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from myapp.authentication import GVMBackend
from django.contrib.auth.decorators import login_required
from myapp.utils.ssh_connection import execute_ssh_command
from myapp.services.targets_service import get_data_targets
import crypt



def index(request):
    # data = get_data()  # Ottieni i dati dal DB
    return render(request, 'myapp/index.html',)  # {'data': data} Passa i dati al template


#Login

def login_view(request):
    #Se il metodo è POST
    print(request.POST)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        backend = GVMBackend()
        #entra nel modello request e prenditi username e password e salvali in due variabili
        user = backend.authenticate(request, username=username,password=password)
        #Se le credenziali sono corrette viene autenticato l'utente e reindirizzato alla home
        if user is not None:
            login(request,user,backend='myapp.authentication.GVMBackend')
            return redirect('dashboard')
        else:
            messages.error(request, "Username o password non corretti")
            # Mostra gli hash nella pagina per debugging
            # stored_hash = request.session.get('stored_hash', 'N/A')
            # generated_hash = request.session.get('generated_hash', 'N/A')

            # messages.error(request, f"Stored Hash: {stored_hash}")
            # messages.error(request, f"Generated Hash: {generated_hash}")

            # Pulisci i valori di debug dalla sessione
            # request.session.pop('stored_hash', None)
            # request.session.pop('generated_hash', None)

            
            
    return render(request,'myapp/login_view.html')
def logout_view(request):
    logout(request)
    return redirect('login')


def dashboard_view(request):
    return render(request, 'myapp/dashboard.html')


def tasks_view(request):
    return render(request,'myapp/tasks.html')


def hosts_view(request):
    #Prendo gli hosts da netdiscover
    devices = execute_ssh_command()
    #print(devices)
    return render(request,'myapp/hosts.html',{'devices': devices})

def targets_view(request):
    targets = get_data_targets()
    return render(request,'myapp/targets.html',{'targets':targets})