from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.reg, name='reg'),
    path('dreg2', views.dreg2, name='dreg2'),
    # path('dreg2/<str:username>', views.dreg2, name='dreg2'),
    path('login', views.login, name='login'),
    path('pdash', views.pdash, name='pdash'),
]
