from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseRedirect, request
from django.contrib.auth.models import User, auth
from .models import Doctor_data, Symptoms, Users
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail


def mail():
    Rid = request.Post['Rid']
    Prescription = request.Post['Prescription']
    Patient = Users.objects.get(Rid=Rid)
    Patient_email = Patient.user.email
    send_mail(
        'Prescription',
        Prescription,
        'from@example.com',
        [Patient_email],
        fail_silently=False,
    )


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
            auth.login(request, ouruser)
            request.session['_old_post'] = request.POST
            if u_are == "Doctor":
                return redirect("dreg2")
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


def dreg2(request):
    old_post = request.session.get('_old_post')
    if request.method == "POST":
        Degree = request.POST['Degree']
        newuser = Users.objects.get(user=request.user)
        Doctor_data.objects.create(Users_D=newuser, Degree=Degree)
        return HttpResponse("get lost")
    print(old_post)
    return render(request, "templates/D-reg2.html")


def pdash(request):
    Symp = Symptoms.objects.all()
    return render(request, "templates/P-Dashboard.html", {"Symps": Symp})
