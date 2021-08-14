from django.urls import path
from . import views

urlpatterns = [
    path('doctordash/', views.test1, name ='test1'),
    path('requests/', views.test2, name ='test2'),
  
]

