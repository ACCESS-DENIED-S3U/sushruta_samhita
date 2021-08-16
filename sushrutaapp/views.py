from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseRedirect, request
from django.contrib.auth.models import User, auth
from .models import Doctor_data, Symptoms, Users, Case
import json
from django.urls import reverse
from django.contrib import messages
from .tasks import send_review_email_task
from django.db import IntegrityError


def checkFullname(fullName):
    setbool = True
    for name in fullName.split():
        if(not name.isalpha()):
            setbool = False
            break
    return setbool

def checkLicense(license_no):
    setbool = True
    for name in license_no.split():
        if(not name.isalnum()):
            setbool = False
            break
    return setbool

def register_user(request):
    if request.user.is_authenticated:
        return redirect("login")
    register_user_page_path = 'templates/commonregistration.html'
    if request.method == 'POST':
        data = request.POST
        registration_id = data['registration_id']
        firstname = data['firstname']
        lastname = ""
        email = data['email']
        phone = data['phone']
        designation = data['designation']
        address = data['address']
        password = data['password']
        conf_pass = data['confirm_password']

        if not checkFullname(firstname):
            return render(request, register_user_page_path, {'msg': ["First Name is not Valid"]})
        if not str(phone).isnumeric() and len(phone) == 10 and phone < 59999999999:
            return render(request, register_user_page_path, {'msg': ["Invalid Phone Number is Entered"]})
        if password != conf_pass:
            return render(request, register_user_page_path, {'msg': ["Passwords Don't match"]})
        if len(password) == 0:
            return render(request, register_user_page_path, {'msg': ["Please enter password"]})
        try:
            ouruser = User.objects.create_user(username=registration_id, first_name=firstname,last_name=lastname, email=email, password=password)
            Users.objects.create(user=ouruser, phone=phone, address=address, designation=designation)
            ouruser.save()

            auth.login(request, ouruser)
            request.session['base_user_register_post'] = request.POST
            request.session["login_user_data"] = request.POST
            send_email(ouruser.username, email, "hey you have registered successfully")
            if designation == "Doctor":
                return redirect("doctor_registration_phase2")
            else:
                return redirect("patient_dashboard")
        except Exception as e:
            return render(request, register_user_page_path, {'msg': [f'User already exists..!!{e}']})
    return render(request, register_user_page_path, {'msg': ""})


def login(request):
    login_page_path = 'templates/commonregistration.html'
    if request.user.is_authenticated:
        data = request.session.get("login_user_data")
        if data:
            user_object = User.objects.get(username=data.get('registration_id'))
            prev_object = Users.objects.get(user=user_object)
            if prev_object.designation == "Doctor":
                return redirect("doctor_dashboard")
            else:
                return redirect("patient_dashboard")
    

    if request.method == 'POST':
        data = request.POST
        registration_id  = data['registration_id']
        password = data['password']
        designation = data['designation']
        user = auth.authenticate(username=registration_id, password=password)
        
        if user is not None:
            custom_user_object = Users.objects.get(user=user)
            if not str(designation)==custom_user_object.designation:
                return render(request, login_page_path, {'msg': f'No {designation} with this credentials!'})
            request.session["login_user_data"] = request.POST
            auth.login(request, user)
            if designation == "Doctor":
                return redirect("doctor_dashboard")
            else:
                return redirect("patient_dashboard")
        return render(request, login_page_path, {'msg': 'Invalid Credentials!'})
    return render(request, login_page_path)


def doctor_registration_phase2(request):
    if not request.user.is_authenticated:
        return redirect('register_user')
    doctor_registration_page_path = "templates/doctorregistration.html"
    base_user_register_post = request.session.get('base_user_register_post')        
    registration_id = base_user_register_post.get('registration_id')
    symptoms_list = Symptoms.objects.all()
    if request.method == "POST":
        data = request.POST
        try:
            degree = data['degree']
            license_no = data['license_no']
            speciality = data['speciality']
            tags = str(json.dumps(data.getlist('tags')))
        except KeyError as keyerr:
            return render(request, doctor_registration_page_path, {'msg': f"Key error (key not found) {keyerr}"})
        if not checkFullname(degree):
            return render(request, doctor_registration_page_path, {'msg': "Put a valid Degree Name"})
        if not checkLicense(license_no):
            return render(request, doctor_registration_page_path, {'msg': "Put a valid License Number"})
        if not checkFullname(speciality):
            return render(request, doctor_registration_page_path, {'msg': "Put a valid Speciality name"})
        base_user = User.objects.get(username=registration_id)
        any_user = Users.objects.get(user=base_user)
        request.session['doctor_user_register_post'] = request.POST
        try:
            Doctor_data.objects.create(Users_D=any_user, degree=str(degree), license_no=str(license_no), speciality=str(speciality), tags=tags)
            return redirect("doctor_dashboard")
        except IntegrityError as ie:
            return render(request, doctor_registration_page_path, {'msg': f"License number Already Exists..!"})
        except Exception as e:
            return render(request, doctor_registration_page_path, {'msg': f"User creation problem occurred..!"})
    # print(base_user_register_post)
    return render(request, doctor_registration_page_path, {'symptoms_list':symptoms_list})


def patient_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('register_user')
    patient_registration_page_path = "templates/sympform.html"
    symptoms_list = Symptoms.objects.all()
    doctors_list = Users.objects.filter(designation="Doctor")
    doctor_data_list = Doctor_data.objects.filter(Users_D__in=doctors_list)
    speciality_list = [""]
    for doctor in doctor_data_list:
        speciality_list.append(f"{doctor.Users_D} ({doctor.speciality})")

    if request.method == 'POST':
        data = request.POST
        user_patient_fk = Users.objects.get(user=request.user)
        description = request.POST.get('description')
        symptoms = str(json.dumps(data.getlist('symptoms')))
        age = data.get('age')
        weight = data.get('weight')
        height = data.get('height')
        doctor_selected_username = data.get('doctor_selected').split('|')[1]
        doctor_selected = Doctor_data.objects.get(Users_D__user__username=doctor_selected_username)
        print(doctor_selected)
        Case.objects.create(user_patient=user_patient_fk, user_doctor_fk=doctor_selected,
        tags=symptoms,description=description,weight=weight,height=height)
        return render(request, patient_registration_page_path, {"symptoms_list": symptoms_list, "speciality_list" : speciality_list, "msg":"You have successfully registered..!!"})

    return render(request, patient_registration_page_path, {"symptoms_list": symptoms_list, "speciality_list" : speciality_list})

def doctor_dashboard(request):
    patient_registration_page_path = "templates/doctordashboard.html"
    doctor_user_register_post = request.session.get('doctor_user_register_post')
    base_doctor_register_post = request.session.get('base_user_register_post')
    login_doctor_data_username = request.session.get('login_user_data').get('registration_id')
    elevated_doctor = Users.objects.get(user__username=login_doctor_data_username)
    base_user = User.objects.get(username=login_doctor_data_username)
    pro_elevated_doctor = Doctor_data.objects.get(Users_D__user__username=login_doctor_data_username)
    cases = Case.objects.filter(user_doctor_fk=pro_elevated_doctor)
    print(cases)
    index = 0
    case_user_list = []
    for case in cases:
        index+=1
        case_user_list.append({'index':index, 'name' : case.user_patient.user.first_name, 'date' : case.date_meeting, 'status' : case.is_treated})
    try:
        name = base_doctor_register_post.get('firstname')
    except:
        name = base_user.first_name
    try:
        education = base_doctor_register_post.get('degree')
    except:
        education = pro_elevated_doctor.degree
    try:
        address = base_doctor_register_post.get('address')
    except:
        address = elevated_doctor.address
    try:
        email = base_doctor_register_post.get('email')
    except:
        email = base_user.email
    try:
        phone = base_doctor_register_post.get('phone')
    except:
        phone = elevated_doctor.phone
    
    context = {
        'name' : name,
        'education' : education,
        'address' : address,
        'email' : email,
        'mobile' : phone,
        'case_user_list' : case_user_list[::-1]
    }
    return render(request, patient_registration_page_path, context)


def pending_request(request):
    pending_request_page_path = 'templates/pendingrequest.html'
    doctor_user_register_post = request.session.get('doctor_user_register_post')
    base_doctor_register_post = request.session.get('base_user_register_post')
    login_doctor_data_username = request.session.get('login_user_data').get('registration_id')
    elevated_doctor = Users.objects.get(user__username=login_doctor_data_username)
    base_user = User.objects.get(username=login_doctor_data_username)
    pro_elevated_doctor = Doctor_data.objects.get(Users_D__user__username=login_doctor_data_username)
    cases = Case.objects.filter(user_doctor_fk=pro_elevated_doctor)
    pending_request = cases.filter(is_treated=False).filter(is_accepted=False)
    treated_users = cases.filter(is_accepted=True).filter(is_treated=False)
    index = 0
    pending_user_list = []
    treated_user_list = []
    for case in pending_request:
        index+=1
        pending_user_list.append({
        'index':index, 
        'username':case.user_patient.user.username,
        'phone':case.user_patient.phone,
        'name' : case.user_patient.user.first_name, 
        'transcript' : f"Age : {case.age} years \n Weight : {case.weight} kg \n Height : {case.height}cm \n Description : {case.description}", 
        'status' : case.is_treated})
    index = 0
    for treated_user in treated_users:
        index+=1
        treated_user_list.append({
        'index':index, 
        'username':treated_user.user_patient.user.username,
        'phone':treated_user.user_patient.phone,
        'name' : treated_user.user_patient.user.first_name})

    try:
        name = base_doctor_register_post.get('firstname')
    except:
        name = base_user.first_name
    try:
        education = base_doctor_register_post.get('degree')
    except:
        education = pro_elevated_doctor.degree
    try:
        address = base_doctor_register_post.get('address')
    except:
        address = elevated_doctor.address
    try:
        email = base_doctor_register_post.get('email')
    except:
        email = base_user.email
    try:
        phone = base_doctor_register_post.get('phone')
    except:
        phone = elevated_doctor.phone
    
    context = {
        'name' : name,
        'education' : education,
        'address' : address,
        'email' : email,
        'mobile' : phone,
        'pending_user_list':pending_user_list,
        'treated_user_list' : treated_user_list
    }

    if request.method == 'POST':
        data = request.POST
        meet_time = str(data['meetdatetime'])
        meetlink = str(data['meetlink'])
        submit_value = str(data['submit'])
        fetch_user = Users.objects.get(user__username=submit_value)
        case = Case.objects.filter(user_patient=fetch_user).first()
        case.is_accepted=True
        case.save()
        send_email(fetch_user.user.first_name, fetch_user.user.email, 
        f"The meeting Time is : {meet_time}\n Link : {meetlink}")
        return redirect('pending_request')

    return render(request, pending_request_page_path, context)


def prescription_request(request):
    data = request.POST
    prescription = str(data['prescription'])
    submit_value = str(data['submit'])
    fetch_user = Users.objects.get(user__username=submit_value)
    case = Case.objects.get(user_patient=fetch_user)
    case.is_treated=True
    case.is_accepted=True
    case.save()
    send_email(fetch_user.user.first_name, fetch_user.user.email, 
        f"Prescription : {prescription}")
    return redirect('pending_request')


def send_email(username, email, data):
    send_review_email_task.delay(username, email, data)


def logoutfunc(request):
    auth.logout(request)
    return redirect('register_user')
