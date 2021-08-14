from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey


class Users(models.Model):  # extended user model
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user')
    phone = models.IntegerField(default=0)
    Address = models.CharField(default='', max_length=50)
    u_are = models.CharField(default='', max_length=25)


class Doctor_data(models.Model):
    Users_D = ForeignKey(Users, on_delete=models.CASCADE)
    Degree = models.CharField(default='', max_length=50)
    # Speciality
    # tag optinal
    # ratings
    isVerifired = models.BooleanField(default=True, blank=True)


class Case(models.Model):
    Users_P = ForeignKey(Users, on_delete=models.CASCADE)
    # User foreign_key
    # doctor fore_k
    # Tags/Symptoms
    # Discription
    # age,weight,height
    # isaccepted dafault false
    # istreated
    # pricription


class Symptoms(models.Model):
    symptom_name = models.CharField(default="", max_length=500)
