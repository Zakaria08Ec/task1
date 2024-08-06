import tkinter as tk
from PIL import Image, ImageTk
import requests
import os
from datetime import datetime

DEFAULT_LAT = 31.9275
DEFAULT_LON = -4.4285


API_KEY = "6a6d7eafaa3bcff5ca967506d2e380d8"

def fetch_weather():
    city = city_entry.get()
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    weather_data = response.json()

    if weather_data['cod'] == 200:
        city_name = weather_data['name']
        country = weather_data['sys']['country']
        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        humidity = weather_data['main']['humidity']
        timestamp = weather_data['dt']

        location_label.config(text=f"{city_name}, {country}")


        photo = update_daytime_icon(description, timestamp) if is_daytime(timestamp) else update_nighttime_icon(description)
        weather_icon_label.config(image=photo)
        weather_icon_label.image = photo

        temp_label.config(text=f"Temperature: {temperature}°C")
        desc_label.config(text=f"Description: {description}")
        humidity_label.config(text=f"Humidity: {humidity}%")
        forecast_label.config(text="")  # Clear forecast label when fetching current weather
    else:
        location_label.config(text="City not found")
        temp_label.config(text="")
        desc_label.config(text="")
        humidity_label.config(text="")
        weather_icon_label.config(image="")
        forecast_label.config(text="")


def fetch_weather_current_location():
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={DEFAULT_LAT}&lon={DEFAULT_LON}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    weather_data = response.json()

    if weather_data['cod'] == 200:
        city_name = weather_data['name']
        country = weather_data['sys']['country']
        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        humidity = weather_data['main']['humidity']
        timestamp = weather_data['dt']

        location_label.config(text=f"{city_name}, {country}")

        photo = update_daytime_icon(description, timestamp) if is_daytime(timestamp) else update_nighttime_icon(description)
        weather_icon_label.config(image=photo)
        weather_icon_label.image = photo

        temp_label.config(text=f"Temperature: {temperature}°C")
        desc_label.config(text=f"Description: {description}")
        humidity_label.config(text=f"Humidity: {humidity}%")
        forecast_label.config(text="")  # Clear forecast label when fetching current weather
    else:
        location_label.config(text="Location not found")
        temp_label.config(text="")
        desc_label.config(text="")
        humidity_label.config(text="")
        weather_icon_label.config(image="")
        forecast_label.config(text="")

def update_daytime_icon(description, timestamp):
    description = description.lower()
    icon_map = {
        'clear': 'first app\sun.png',
        'clouds': 'first app\cloudy.png',
        'rain': 'first app\grainy.png',
        'snow': 'first app\SNOW.png',
        'storm': 'first app\storm.png',
    }

    icon_file = 'first app\sun.png'
    for key in icon_map:
        if key in description:
            icon_file = icon_map[key]
            break

    return load_and_resize_icon(icon_file)

def update_nighttime_icon(description):
    description = description.lower()
    icon_map = {
        'clear': 'first app\moon.png',
        'clouds': 'first app\cloudymoon.png',
        'rain': 'first app\grainymoonn.png',
        'snow': 'first app\snowmoon.png',
        'storm': 'first app\storm.png',
    }

    icon_file = 'first app\moon.png'
    for key in icon_map:
        if key in description:
            icon_file = icon_map[key]
            break

    return load_and_resize_icon(icon_file)

def load_and_resize_icon(icon_file):
    if not os.path.isfile(icon_file):
        print(f"File not found: {icon_file}")
        return ImageTk.PhotoImage(Image.new('RGB', (100, 100), color='grey'))

    img = Image.open(icon_file)
    img = img.resize((100, 100), Image.LANCZOS)  # Utilisation de Image.LANCZOS pour le redimensionnement avec lissage
    return ImageTk.PhotoImage(img)

def is_daytime(timestamp):
    dt = datetime.utcfromtimestamp(timestamp)
    return 6 <= dt.hour < 18

def on_focus_in(event):
    if city_entry.get() == "Enter a city":
        city_entry.delete(0, tk.END)
        city_entry.config(fg='black')

def on_focus_out(event):
    if city_entry.get() == "":
        city_entry.insert(0, "Enter a city")
        city_entry.config(fg='grey')

def fetch_forecast():
    city = city_entry.get()
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    
    response = requests.get(url)
    forecast_data = response.json()

    if forecast_data['cod'] == '200':
        forecasts = "Forecasts:\n"
        for i in range(0, 40, 8):  # Obtenir une prévision par jour
            date = forecast_data['list'][i]['dt_txt'].split(' ')[0]
            temp = forecast_data['list'][i]['main']['temp']
            desc = forecast_data['list'][i]['weather'][0]['description']
            forecasts += f"{date}: {temp}°C, {desc}\n"
        
        location_label.config(text="")
        temp_label.config(text="")
        desc_label.config(text="")
        humidity_label.config(text="")
        weather_icon_label.config(image="")
        forecast_label.config(text=forecasts)
        
        load_logo()
    else:
        forecast_label.config(text="No forecast available")

def load_logo():
    # Chargement et redimensionnement du logo
    logo_image = Image.open("first app\sun.png")  # Chemin vers votre fichier logo
    logo_image = logo_image.resize((100, 100), Image.LANCZOS)  # Redimensionnement du logo avec lissage
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(root, image=logo_photo, bg="#ADD8E6")
    logo_label.pack()

root = tk.Tk()
root.title("Weather Application")
root.geometry("400x600")
root.configure(bg="#ADD8E6")

title_label = tk.Label(root, text="Weather Application", font=("Helvetica", 24, "bold"), bg="#ADD8E6")
title_label.pack(pady=20)

search_frame = tk.Frame(root, bg="#ADD8E6")
search_frame.pack(pady=10)

city_entry = tk.Entry(search_frame, font=("Helvetica", 18), width=20, fg='grey')
city_entry.insert(0, "Enter a city")
city_entry.bind("<FocusIn>", on_focus_in)
city_entry.bind("<FocusOut>", on_focus_out)
city_entry.pack(side=tk.LEFT, padx=5)

search_button = tk.Button(search_frame, text="Search", font=("Helvetica", 14), bg="orange", command=fetch_weather)
search_button.pack(side=tk.LEFT, padx=5)

button_frame = tk.Frame(root, bg="#ADD8E6")
button_frame.pack(pady=10)

forecast_label = tk.Label(root, text="", font=("Helvetica", 14), bg="#ADD8E6", justify="left")
forecast_label.pack(pady=20)

forecast_button = tk.Button(button_frame, text="Forecasts", font=("Helvetica", 14), bg="orange", command=fetch_forecast)
forecast_button.pack(side=tk.LEFT, padx=5)

location_button = tk.Button(button_frame, text="Current Location", font=("Helvetica", 14), bg="orange", command=fetch_weather_current_location)
location_button.pack(side=tk.LEFT, padx=5)

location_label = tk.Label(root, text="", font=("Helvetica", 18), bg="#ADD8E6")
location_label.pack(pady=10)

weather_icon_label = tk.Label(root, bg="#ADD8E6")
weather_icon_label.pack(pady=10)

temp_label = tk.Label(root, text="", font=("Helvetica", 14), bg="#ADD8E6")
temp_label.pack(pady=10)

desc_label = tk.Label(root, text="", font=("Helvetica", 14), bg="#ADD8E6")
desc_label.pack(pady=10)

humidity_label = tk.Label(root, text="", font=("Helvetica", 14), bg="#ADD8E6")
humidity_label.pack(pady=10)

root.mainloop()

