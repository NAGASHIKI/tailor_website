from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Dress, Measurement, Tailor
from django.contrib.auth.decorators import login_required


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def home(request):
    dresses = Dress.objects.all()
    return render(request, 'home.html', {'dresses': dresses})

@login_required
def submit_measurements(request, dress_id):
    if request.method == 'POST':
        measurements = request.POST.get('measurements')
        dress = Dress.objects.get(id=dress_id)
        Measurement.objects.create(user=request.user, dress=dress, measurements=measurements)
        return redirect('home')
    dress = Dress.objects.get(id=dress_id)
    return render(request, 'submit_measurements.html', {'dress': dress})

@login_required
def tailor_work(request, tailor_id):
    tailor = Tailor.objects.get(id=tailor_id)
    dresses = Dress.objects.filter(tailor=tailor)
    return render(request, 'tailor_work.html', {'tailor': tailor, 'dresses': dresses})
