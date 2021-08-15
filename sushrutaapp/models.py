from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey


class Users(models.Model):  # extended user model
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user')
    phone = models.IntegerField(default=0)
    address = models.CharField(default='', max_length=50)
    designation = models.CharField(default='', max_length=25)

    def __str__(self):
        return f"{self.user.first_name} |{self.user.username}|"

class Doctor_data(models.Model):
    Users_D = ForeignKey(Users, on_delete=models.CASCADE)
    degree = models.CharField(default='', max_length=50)
    license_no = models.CharField(unique=True, blank=True, max_length=300)
    speciality = models.CharField(default='', max_length=100)
    tags = models.CharField(default='[]', max_length=500)
    rating = models.IntegerField(default=0, null=True)
    isVerified = models.BooleanField(default=True, blank=True, null=True)

    def __str__(self):
        return f"{self.Users_D.user.username} - {self.license_no}"


class Case(models.Model):
    user_patient = ForeignKey(Users, on_delete=models.CASCADE)
    user_doctor_fk = ForeignKey(Doctor_data, on_delete=models.CASCADE, null=True)
    tags = models.CharField(default='[]', max_length=500)
    description = models.TextField(default="", max_length=1000)
    age = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    is_accepted = models.BooleanField(default=False)
    is_treated = models.BooleanField(default=False)
    prescription = models.TextField(max_length=1000,default="")

    def __str__(self):
        return f"{self.user_patient} {self.user_doctor_fk}"


class Symptoms(models.Model):
    symptom_name = models.CharField(default="", max_length=500)

    def __str__(self):
        return self.symptom_name
