import requests
from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from .forms import ProfileForm
from .models import SearchHistory
from .models import Profile
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('API_KEY')

def register (request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def home(request):
    weather = None
    if request.method == 'POST':
        city = request.POST.get('city')
        api_key = API_KEY
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # print(data)
            weather = {
                'city': city,
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity']
            }
            if request.user.is_authenticated:
                SearchHistory.objects.create(
                    user=request.user,
                    city=city,
                    temperature=weather['temperature'],
                    description=weather['description'],
                    humidity=weather['humidity']
                )
    return render(request, 'home.html', {'weather': weather})

def search_history(request):
    if request.user.is_authenticated:
        history = SearchHistory.objects.filter(user=request.user)
        return render(request, 'history.html', {'history': history})
    else:
        return redirect('login')


@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'profile': profile})
