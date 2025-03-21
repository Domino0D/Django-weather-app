from django.shortcuts import render
from django.views import View 
from django.contrib.auth.views import LoginView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from .models import City, Profile
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .forms import ProfileForm, LoginForm, RegisterForm
import requests
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from decimal import *

from django.contrib.messages.views import SuccessMessageMixin


from django.views.generic.edit import CreateView

from rest_framework import generics
from .serializers import CitySerializer
from rest_framework import permissions

from django.http import HttpResponse
import requests


class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')  # Przekierowanie po wylogowaniu


class SignUpView(FormView):
    template_name = 'register.html'  # Szablon HTML dla rejestracji
    form_class = RegisterForm  # Formularz rejestracji
    success_url = reverse_lazy('homeView')  # Przekierowanie po udanej rejestracji

    def form_valid(self, form):
        # Zapisz nowego użytkownika
        user = form.save()
        # Automatyczne logowanie użytkownika po rejestracji (opcjonalne)
        login(self.request, user)
        return super().form_valid(form)

class LoginView(LoginView):
    template_name = 'login.html'
    form_class = LoginForm
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('homeView')

class homeView(View):
    template_name = 'home.html'

    def get(self, request):
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=#your api key' 
        
        city_name = request.GET.get('city_name', 'Warsaw')
        weather = None
        profile_form = None
        context = {}
        context2 = {}
        wrong_city_message = ''

        if request.user.is_authenticated:
            UserScale, created = Profile.objects.get_or_create(user=request.user)
            
        if request.user.is_authenticated and Profile.objects.get_or_create(user=self.request.user): 
            profile_form = ProfileForm(instance=request.user.profile)
        else:
            profile_form = ProfileForm()
        
        if city_name:
            try:
                city_weather = requests.get(url.format(city_name)).json()
                if 'main' in city_weather:
                    if not request.user.is_authenticated or UserScale.Temp_scale == 'C':
                        weather = {
                            'city': city_name,
                            "temperature": round(Decimal(city_weather['main']['temp'] -32 ) * 5 / 9, 1),
                            "description": city_weather['weather'][0]['description'],
                            "icon": city_weather['weather'][0]['icon'],
                            "country": city_weather['sys']['country'],
                            "maxtemp": round(Decimal(city_weather['main']['temp_max'] -32 ) * 5 / 9, 1),
                            "mintemp": round(Decimal(city_weather['main']['temp_min'] -32 ) * 5 / 9, 1),
                        }
                    elif request.user.is_authenticated and UserScale.Temp_scale == 'F':
                        weather = {
                            'city': city_name,
                            "temperature": round(Decimal(city_weather['main']['temp']), 1),
                            
                            "description": city_weather['weather'][0]['description'],
                            "icon": city_weather['weather'][0]['icon'],
                            "country": city_weather['sys']['country'],
                            "maxtemp": round(Decimal(city_weather['main']['temp_max']), 1),
                            "mintemp": round(Decimal(city_weather['main']['temp_min']), 1),
                        }

                    if request.user.is_authenticated:
                        # Dodawanie miasta tylko jeśli API zwróciło kod 200 i miasto nie jest jeszcze zapisane
                        response = requests.get(url.format(city_name))
                        if response.status_code == 200 and not City.objects.filter(city=city_name, user=request.user).exists():
                            City.objects.create(city=city_name, user=request.user)
                else:
                    wrong_city_message = f'City not found: {city_name}' # Komunikat, gdy nie ma 'main' w odpowiedzi
            except requests.exceptions.RequestException as e:
                wrong_city_message = f"Error fetching weather data: {e}"  #Komunikat, gdy jest problem z API
        else:
            wrong_city_message = 'Please enter a city name.' # Komunikat, gdy nie podano nazwy miasta

        if request.user.is_authenticated:
            SavedCitys = City.objects.filter(user=request.user)
            weather_info = []
            for city in SavedCitys:
                response = requests.get(url.format(city.city))    
                if response.status_code == 200:
                    data = response.json()
                    if UserScale.Temp_scale == "F":
                        city_weather_info = {
                            "id": city.id,
                            "test": "test",
                            "City_name": city.city,
                            "temperature": round(Decimal(data['main']['temp']), 1),
                            "description": data['weather'][0]['description'],
                            "icon": data['weather'][0]['icon'],
                            "country": data['sys']['country'],
                            "maxtemp": round(Decimal(data['main']['temp_max']), 1),
                            "mintemp": round(Decimal(data['main']['temp_min']), 1),
                       
                        }
                        weather_info.append(city_weather_info)
                        
                    if UserScale.Temp_scale == "C":
                        city_weather_info = {   
                            "id": city.id,
                            "City_name": city.city,
                            "temperature": round(Decimal(data['main']['temp'] -32 ) * 5 / 9, 1),
                            "description": data['weather'][0]['description'],
                            "icon": data['weather'][0]['icon'],
                            "country": data['sys']['country'],
                            "maxtemp": round(Decimal(data['main']['temp_max'] -32 ) * 5 / 9, 1),
                            "mintemp": round(Decimal(data['main']['temp_min'] -32 ) * 5 / 9, 1),
                       
                    }
                        weather_info.append(city_weather_info)
                context = {
                    'weather': weather, 
                    'weather_info': weather_info,
                    'profile_form': profile_form,  # Dodaj formularz do kontekstu
                    'wrong_city_message': wrong_city_message,
                }
        if not request.user.is_authenticated :
                context = {
                    'weather': weather, 
                    'wrong_city_message': wrong_city_message,
                }
            
        return render(request, self.template_name, context, context2.update(context))               
                                            
    def post(self, request):
        # Przetwarzanie danych z formularza
        profile_form = ProfileForm(request.POST, instance=request.user.profile)  # Przekazanie danych profilu użytkownika

        if profile_form.is_valid(): # Sprawdź, czy formularz jest poprawny
            profile_form.save()  # Zapisz zmiany w profilu
            return redirect('homeView')  # Przekierowanie po zapisaniu
        else:
            # W przypadku błędów, przekazujemy formularz z powrotem do kontekstu
            context = {
                'profile_form': profile_form,
                # Możesz dodać inne dane do kontekstu, jeśli potrzebujesz
            }
            return render(request, self.template_name, context) # Zwróć szablon z błędami
    
    
    
class CityListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CitySerializer
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return City.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
            
class CityDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CitySerializer
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return City.objects.filter(user=self.request.user)
    
    def perform_destroy(self, instance):
        instance.delete()
