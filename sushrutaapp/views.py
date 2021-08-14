from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, auth
from .models import Doctor_data, Users
from django.urls import reverse


def reg(request):
    if request.method == 'POST':
        data = request.POST
        Rid = data['Rid']
        firstname = data['firstname']
        lastname = data['lastname']
        email = data['email']
        phone = data['phone']
        u_are = data['u_are']
        Address = data['Address']

        password = data['password']
        conf_pass = data['confirm_password']
        if not str(firstname).isalpha():
            return render(request, 'templates/reg.html', {'msg': ["First Name is not Valid"]})
        if not str(lastname).isalpha():
            return render(request, 'templates/reggreg.html', {'msg': ["Last Name is not Valid"]})
        if not str(phone).isnumeric() and len(phone) == 10 and phone < 59999999999:
            return render(request, 'templates/reg.html', {'msg': ["Invalid Phone Number is Entered"]})
        if password != conf_pass:
            return render(request, 'templates/reg.html', {'msg': ["Passwords Don't match"]})
        if len(password) == 0:
            return render(request, 'templates/reg.html', {'msg': ["Please enter password"]})
        try:
            ouruser = User.objects.create_user(username=Rid, first_name=firstname, email=email, password=password,
                                               last_name=lastname)
            newuser = Users(user=ouruser, phone=phone, Address=Address,
                            u_are=u_are)

            ouruser.save()
            newuser.save()
            if u_are == "Doctor":
                return redirect(f"dreg2/{ouruser.username}")
            else:
                return render(request, 'templates/P-dashboard.html')

            # return render(request, 'templates/dashboard.html')
        except Exception as e:
            return render(request, 'templates/reg.html', {'msg': ['User already exists..!!']})
    return render(request, 'templates/reg.html', {'msg': ""})


def login(request):
    if request.method == 'POST':
        Rid = request.POST['Rid']
        password = request.POST['password']
        user = auth.authenticate(username=Rid, password=password)

        if user is not None:
            auth.login(request, user)
            return render(request, 'templates/dashboard.html')
        return render(request, 'templates/login.html', {'errors': 'Invalid Credentials!'})
    return render(request, 'templates/login.html')


def dreg2(request, username):
    newuser = User.objects.get(username=username)
    print(username)
    # if request.method == 'POST':
    #     data = request.POST
    #     degree = data['degree']
    #     newuser = User.objects.get(username=username)
    #     doctor_user = Users.objects.get(user=newuser)
    #     finaluser = Doctor_data.objects.create(
    #         Users_E=doctor_user, Degree=degree)
    #     return render(request, 'templates/dashboard.html')
    # finaluser.save()
    return render(request, 'templates/D-reg2.html')
    # return HttpResponse(f'alpha {username}')


def dreg23(request):
    # user_obj = User.objects.get(user=request.user)
    return HttpResponse(f'{request.user}')
    # finaluser = Doctor_data.objects.create(
    #     Users_E=doctor_user, Degree=degree)
    # if request.method == 'POST':
    #     data = request.POST
    #     degree = data['degree']
    #     finaluser = Doctor_data.objects.create(
    #         Users_E=user_obj, Degree=degree)
    #     return HttpResponse(f'alpha')
    #     # return render(request, 'templates/dashboard.html')
