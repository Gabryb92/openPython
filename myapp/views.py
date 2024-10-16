from django.shortcuts import render,redirect
from django.db import connection
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from myapp.authentication import GVMBackend
from myapp.utils.ssh_connection import execute_ssh_command
from myapp.services.targets_service import get_data_targets, create_target
from myapp.services.tasks_service import get_data_tasks, create_task
#from myapp.services.gvm_service import get_scanners
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
            

            
            
    return render(request,'myapp/login_view.html')
def logout_view(request):
    logout(request)
    return redirect('login')


def dashboard_view(request):
    return render(request, 'myapp/dashboard.html')


def tasks_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        target = request.POST.get('scan_targets')
        scanner = request.POST.get('scanner')
        config = request.POST.get('config')
        
        try:
            #Crea il task
            create_task(name,target,scanner,config)
            messages.success(request,"Task aggiunto con successo!")
        except Exception as e:
            #Se c'è un errore, aggiungi un messaggio di errore
            messages.error(request,f"Errore durante l'aggiunta del task :{e}")
            
    tasks = get_data_tasks()
    targets = get_data_targets()
    
    
    # scanners = get_scanners()
    return render(request,'myapp/tasks.html', {'tasks':tasks,'targets':targets})


def get_hosts(request):
    if request.method == "GET":
        devices = execute_ssh_command()
        
        
        return JsonResponse({'devices':devices})



def hosts_view(request):
    #Prendo gli hosts da netdiscover
    #devices = execute_ssh_command()
    #print(devices)
    return render(request,'myapp/hosts.html')




def targets_view(request):
    if request.method == 'POST':
        
        referrer = request.META.get('HTTP_REFERER','')
        if '/targets' in referrer:
            # Richiesta proveniente dalla pagina targets
            name = request.POST.get('name')
            hosts = request.POST.get('hosts')
            allow_simultaneous_ips = request.POST.get('allow_simultaneous_ips')
            port_list = request.POST.get('port_list')
            alive_test = request.POST.get('alive_test')
            reverse_lookup_only = request.POST.get('reverse_lookup_only')
            reverse_lookup_unify = request.POST.get('reverse_lookup_unify')
            comment = request.POST.get('comment')
            exclude_hosts = request.POST.get('exclude_hosts')
            
            try:
                create_target(
                                name=name,
                                hosts=hosts,
                                allow_simultaneous_ips=allow_simultaneous_ips,
                                port_list=port_list,
                                alive_test=alive_test,
                                reverse_lookup_only=reverse_lookup_only,
                                reverse_lookup_unify=reverse_lookup_unify,
                                comment=comment,
                                exclude_hosts=exclude_hosts
                                )
                messages.success(request,"Host aggiunto con successo!")
            except Exception as e:
                messages.error(request,f"Errore durante l'aggiunta del task :{e}")
            
            targets = get_data_targets()
            return render(request, 'myapp/targets.html', {'targets': targets})
        
        selected_hosts = request.POST.getlist('selected_hosts')
        mac_vendors = []
        #print(request.POST)
        

        # Per ogni IP selezionato, cerca il MAC Vendor corrispondente
        for ip in selected_hosts:
            mac_vendor = request.POST.get(f'mac_vendors_{ip}')
            mac_vendors.append(mac_vendor)

        # Crea una lista di tuple (IP, MAC Vendor)
        devices = list(zip(selected_hosts, mac_vendors))

        # print("Selected Hosts:", selected_hosts)
        # print("MAC Vendors:", mac_vendors)
        # print("Devices (IP, MAC Vendor):", devices)
        
        # Recupera i campi aggiuntivi dalla modale
        allow_simultaneous_ips = request.POST.get('allow_simultaneous_ips')
        port_list = request.POST.get('port_list')
        alive_test = request.POST.get('alive_test')
        reverse_lookup_only = request.POST.get('reverse_lookup_only')
        reverse_lookup_unify = request.POST.get('reverse_lookup_unify')
        comment = request.POST.get('comment')
        exclude_hosts = request.POST.get('exclude_hosts')
        

        # Salva nel database
        if selected_hosts:
            for device in devices:
                try:
                    create_target(
                                    name=device[1],
                                    hosts=device[0],
                                    allow_simultaneous_ips=allow_simultaneous_ips,
                                    port_list=port_list,
                                    alive_test=alive_test,
                                    reverse_lookup_only=reverse_lookup_only,
                                    reverse_lookup_unify=reverse_lookup_unify,
                                    comment=comment,
                                    exclude_hosts=exclude_hosts
                                )
                    messages.success(request,"Host aggiunto con successo!")
                    
                    # print(f"Target {device[0]}aggiunto correttamente")
                except Exception as e:
                    messages.error(request,f"Errore durante l'aggiunta del task :{e}")
                    
                    #print(f"Errore durante l'aggiunta del target {device[0]}: {e}")

    targets = get_data_targets()
    return render(request, 'myapp/targets.html', {'targets': targets})
