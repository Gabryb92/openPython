"""
URL configuration for bbros_vas_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from myapp import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('',views.login_view,name='login'),
    path('logout/',login_required(views.logout_view),name='logout'),
    path('dashboard/',login_required(views.dashboard_view),name='dashboard'),
    path('tasks/',login_required(views.tasks_view),name='tasks'),
    path('hosts/',login_required(views.hosts_view),name='hosts'),
    path('get_hosts/',login_required(views.get_hosts)),
    path('targets/',login_required(views.targets_view),name='targets'),
    path('tasks/start_scan/<task_uuid>/', views.start_scan_view, name='start_scan'),
    path('tasks/status/<str:task_uuid>/',views.task_status_view, name="tasks_status")
    
    
    #path('login/', views.login_view,name='login'),
    #path('',views.index,name='index')
    
]
