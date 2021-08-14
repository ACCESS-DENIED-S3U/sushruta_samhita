from django.contrib import admin

from .models import Users, Doctor_data, Symptoms

admin.site.register(Users)
admin.site.register(Doctor_data)
admin.site.register(Symptoms)
