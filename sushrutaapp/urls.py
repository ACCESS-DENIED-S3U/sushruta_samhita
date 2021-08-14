from django.urls import path
from . import views


urlpatterns = [
    path('', views.reg, name='reg'),
    path('dreg23', views.dreg23, name='dreg23'),
    path('dreg2/<str:username>', views.dreg2, name='dreg2'),
    path('login', views.login, name='login'),
]
