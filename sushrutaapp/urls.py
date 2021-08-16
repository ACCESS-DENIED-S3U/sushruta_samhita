from django.urls import path
from . import views


urlpatterns = [
    path('', views.register_user, name='register_user'),
    path('login', views.login, name='login'),
    path('doctor_registration_phase2', views.doctor_registration_phase2,name='doctor_registration_phase2'),
    path('patient_dashboard', views.patient_dashboard, name='patient_dashboard'),
    path('doctor_dashboard', views.doctor_dashboard, name='doctor_dashboard'),
    path('logout', views.logoutfunc, name='logout'),
    path('pending_request', views.pending_request, name='pending_request'),
    path('prescripton_request', views.prescription_request, name='prescription_request'),
    path('canva', views.canva, name='canva'),
    path('whiteboard', views.whiteboard, name='whiteboard'),
]
