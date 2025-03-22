# Django Weather App

A weather application built with Django that allows users to search for weather information for different cities.

## Features

- Search for weather information by city name.
- Display current weather conditions (temperature, max temp, min temp, icon, Country).
- User authentication (login, registration, logout).
- Saving favorite cities.
- Temperature scale selection (Celsius/Fahrenheit).

## Technologies

- Python
- Django
- HTML
- CSS
- JavaScript/Ajax
- OpenWeatherMap API

## Installation

1. Clone the repository:
   
git clone https://github.com/Domino0D/weather3.0.git

2. Create a virtual environment:
3. Activate the virtual environment:
- On Windows:
  ```
  venv\Scripts\activate
  ```
- On macOS and Linux:
  ```
  source venv/bin/activate
  ```
4. Install dependencies (you must to have python already):
pip install -r requirements.txt

5. Run migrations
   python manage.py migrate

6. Add your secure key in settings.py
   
8. Log in and generate your OpenWeatherApi key on https://openweathermap.org/api and put them in url in main class in views.py
   
10. run sever:
 python manage.py runserver

11. and enjoy!




