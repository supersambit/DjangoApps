import string
import random
from math import floor
from django.utils import timezone
from .models import Vehicle, CustomUser
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash, authenticate
from django.contrib import messages


def index(request):
    return render(request, 'djapp/index.html', {})


@login_required
def home(request):
    return render(request, 'djapp/home.html', {'fname': request.user.first_name})


def signin(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        pwd = request.POST['pwd']
        user = authenticate(request, username=uname, password=pwd)
        if user is not None:
            login(request, user)
            messages.success(request, "Signed in Successfully.")
            return redirect('home')
        else:
            messages.error(request, "Bad Credentials!")
            return redirect('index')


@login_required
def signout(request):
    logout(request)
    messages.success(request, "Signed Out Successfully!!")
    return redirect('index')


@login_required
def add_user(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        phone_number = request.POST['phn']

        if CustomUser.objects.filter(username=fname):
            username = fname+str(phone_number)[-2:]
        else:
            username = fname

        all_characters = string.ascii_letters + string.digits + "@#$"
        pass1 = ''.join(random.choices(all_characters, k=9))
        myuser = CustomUser.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.phone_number = str(phone_number)
        myuser.save()
        messages.success(request, f"New User has been added successfully!! Password can be updated by the user. "
                                  f"current Username : {username} & password : {pass1}")
        return redirect('add_user')
    else:
        return render(request, 'djapp/add_user.html', {'fname': request.user.first_name})


@login_required
def change_password(request):
    if request.method == "POST":
        curr_pass = request.POST['curr_pass']
        np1 = request.POST['np1']
        np2 = request.POST['np2']
        user_auth = authenticate(username=request.user.username, password=curr_pass)
        if user_auth is None:
            messages.error(request, "Please Enter Your Current Password Correctly!!")
            return redirect('change_password')

        if np1 != np2:
            messages.error(request, "Password and Confirm Password DO NOT Match!!")
            return redirect('change_password')

        user_auth.set_password(np1)
        user_auth.save()
        update_session_auth_hash(request, user_auth)
        messages.success(request, "Password has been updated successfully.")
        return redirect('home')
    else:
        return render(request, 'djapp/change_password.html', {'user': request.user})


@login_required
def add_record(request):
    if request.method == "POST":
        vehicle_type = request.POST['type']
        vehicle_number = request.POST['number']
        if 'helmet' in request.POST:
            has_helmet = request.POST['helmet']
        else:
            has_helmet = 0
        entry_time = timezone.now()
        new_entry = Vehicle(
            user=request.user,
            vehicle_number=vehicle_number,
            vehicle_type=vehicle_type,
            has_helmet=has_helmet,
            entry_time=entry_time
        )
        if Vehicle.objects.filter(vehicle_number=vehicle_number):
            messages.error(request, "Entry already exists for the entered number/Id!!")
        else:
            new_entry.save()
            messages.success(request, "New Record has been added successfully!!")
        return redirect('home')


@login_required
def records(request):
    vehicles = Vehicle.objects.all()
    curr_vehicles = []
    billed_vehicles = []
    for v in vehicles:
        if "-billed" not in v.vehicle_number:
            curr_vehicles.append(v)
        else:
            billed_vehicles.append(v)
    curr_data = zip_adder_vehicle(curr_vehicles)
    billed_data = zip_adder_vehicle(billed_vehicles)
    print(curr_vehicles, billed_vehicles)
    return render(request, 'djapp/records.html', {'curr_data': curr_data, 'billed_data': billed_data})


@login_required
def check_out(request):
    if request.method == 'POST':
        num = request.POST.get('num')
        vehicles = Vehicle.objects.filter(vehicle_number=num)

        if len(vehicles) < 1:
            messages.error(request, "No Active Record found!!")
            return redirect('home')

        for vehicle in vehicles:
            vehicle.fare = calculate_duration(vehicle).fare
            vehicle.duration = calculate_duration(vehicle).duration
        data = zip_adder_vehicle(vehicles)
        messages.success(request, "Object/Vehicle Details Displayed.")
        return render(request, 'djapp/home.html', {'data': data, 'fname': request.user.first_name})
    else:
        return redirect('home')


def bill_out(request):
    if request.method == 'POST':
        v = request.POST['vehicle']
        vehicle = Vehicle.objects.get(id=v)
        vehicle = calculate_duration(vehicle)
        vehicle.vehicle_number = vehicle.vehicle_number + "-billed"
        vehicle.save()
        messages.success(request, f"Object/Vehicle {vehicle.vehicle_number} with Rs. {vehicle.fare}!")
        return redirect('home')
    else:
        v = request.GET['vehicle']
        vehicle = Vehicle.objects.get(id=v)
        vehicle = calculate_duration(vehicle)
        messages.error(request, f"Please collect the fare Rs. {vehicle.fare} for : {vehicle.vehicle_number}")
        return render(request, 'djapp/home.html', {'bo_vehicle': vehicle, 'fname': request.user.first_name})


def calculate_fare(v_type, duration, helmet):
    FARES = {
        "stuff": 5,
        "cycle": 10,
        "bike": 15,
        "auto": 30,
        "car": 50
    }
    if helmet:
        fare = FARES[v_type] * floor(duration / 12) + 10 + FARES[v_type]
    else:
        fare = FARES[v_type] * floor(duration / 12) + FARES[v_type]
    return fare


def calculate_duration(vehicle):
    vehicle.exit_time = timezone.now()
    time_diff = vehicle.exit_time - vehicle.entry_time
    vehicle.duration = int(time_diff.total_seconds() / 3600)
    vehicle.fare = calculate_fare(vehicle.vehicle_type, vehicle.duration, vehicle.has_helmet)
    return vehicle


def zip_adder_vehicle(vehicles):
    adders = []
    for v in vehicles:
        v_uid = v.user_id
        name = CustomUser.objects.get(id=v_uid).first_name + CustomUser.objects.get(id=v_uid).last_name
        adders.append(name)
    combo_data = zip(adders, vehicles)
    return combo_data
