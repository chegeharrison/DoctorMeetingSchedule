from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from . models import Doctor
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Doctor, Meeting
from .forms import MeetingForm, AddProfileForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib import messages
import datetime

# Create your views here.

def home(request):
    return render(request, 'home/index.html')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
        
            return redirect('dashboard')
        else:
            return render(request, 'home/login.html', {'error_message': 'Invalid username or password.'})

    return render(request, 'home/login.html')

def admin_logout(request):
    logout(request)
    # Redirect to the desired view after logout
    return redirect('home')


def doctor_page(request):
    doctors = Doctor.objects.all()
    context = {'doctors': doctors}
    return render(request, 'doctor/doctor.html', context)


@login_required(login_url='/login/')
def dashboard(request):
    doctors = Doctor.objects.all()
    parameters = {'doctors': doctors}
    return render(request, 'doctor/dashboard.html', parameters)



@login_required(login_url='/login/')
def meeting_manager(request):
    if request.method == 'POST':
        if request.POST.get("visitor"): 
            meeting_id = request.POST.get("visitor")
            meeting = Meeting.objects.get(id=meeting_id)
            doctor = Doctor.objects.get(current_meeting_id=meeting_id)
            meeting_details = {'meeting': meeting, 'doctor': doctor}
            return render(request, 'doctor/visitor_details.html', meeting_details)

        elif request.POST.get("meeting"): 
            doctor_id = request.POST.get("meeting")
            doctor = Doctor.objects.get(id=doctor_id)
            form = MeetingForm()
            param = {'form': form, 'doctor': doctor}
            return render(request, 'doctor/meeting_form.html', param)

    else:
        return redirect('/dashboard')
    
@login_required(login_url='/login/')
def save_meeting(request):
    if request.method == 'POST':
        doctor_name = request.POST.get('doctor')
        doctor = get_object_or_404(Doctor, doctor_name=doctor_name)
        form = MeetingForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.time_in = datetime.datetime.now()
            instance.doctor = doctor  # Assign the Doctor instance, not the name
            instance.date = instance.time_in.date()  # Set the date field
            instance.save()

            doctor.current_meeting_id = instance.id
            doctor.status = False
            doctor.save()

            messages.success(request, 'Information sent to Doctor, You will be called shortly !!')
            return redirect('/dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
            return redirect('/dashboard')
    else:
        return redirect('/dashboard')

def meeting_history(request):
    # Get today's meetings
    today = datetime.date.today()
    meetings = Meeting.objects.filter(date=today).order_by('-time_in')

    # Render the meeting history template with the fetched meetings
    return render(request, 'doctor/meeting_history.html', {'meetings': meetings})    
    
def checkout(request):
    if request.method == 'GET':
        meeting_id = request.GET['mid']
        meeting = Meeting.objects.get(id=meeting_id)
        doctor = next(iter(Doctor.objects.filter(current_meeting_id=meeting_id)), None)
        if (meeting.time_out is not None) and (doctor is None):
            return HttpResponse(meeting.visitor_name + ', Already Checked Out !!')
        doctor.status = True
        doctor.current_meeting_id = None 
        meeting.time_out = datetime.datetime.now()
        doctor.save()
        meeting.save()
        return HttpResponse(meeting.visitor_name + ', Checked Out Successfully !!')

# @login_required(login_url='/login/')
# def dashboard(request):
#     if request.method == 'POST':
#         form = AddProfileForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('/dashboard')
#     else:
#         return redirect('/dashboard')

@login_required(login_url='/login/')
def profile_manager(request):
    if request.method == 'POST':
        form = AddProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/dashboard')



def edit_profile(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('editing')
        instance = Doctor.objects.filter(id=doctor_id).first()
        form = AddProfileForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('/dashboard')
    else:
        return redirect('/dashboard')
    

@login_required(login_url='/login/')
def edit_delete(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('id')
        if doctor_id == '':
            messages.warning(request, 'Please enter a valid profile Id first !!')
            form = AddProfileForm()
            return render(request, 'doctor/profile_manage.html', {'form': form})
        doctor = Doctor.objects.filter(id=doctor_id).first()
        if doctor:
            if request.POST.get('edit'):
                form = AddProfileForm(instance=doctor)
                context = {'form': form, 'edit': True, 'info': doctor_id}
                return render(request, 'doctor/profile_manage.html', context)
            elif request.POST.get('delete'):
                doctor.delete()
                return redirect('/dashboard')
        else:
            messages.warning(request, 'Profile not found !!')
            form = AddProfileForm()
            return render(request, 'doctor/profile_manage.html', {'form': form})
    
    # Redirect to the profile_manage.html page for doctors
    return render(request, 'doctor/profile_manage.html')



