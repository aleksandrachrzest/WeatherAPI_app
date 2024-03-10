import requests
import pandas as pd
from unidecode import unidecode
from translate import Translator

# Prepare variables
api_key = "0e74c67c50a245aeaf391426240903"

# Connect to API
while True:
    city = input("Enter the city to get weather data from: ")  # zmienna, która zawiera polskie znaki, np. Łódź
    city_unidecoded = unidecode(city) # zmienna, która nie zawiera polskich znaków, będzie służyła do komunikacji z API (bo API nie wspiera polskich znaków)
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city_unidecoded}&aqi=yes"

# try:
    response = requests.get(url) # get = select
    if response.status_code == 200:
        response = response.json()
        break
    else:
     if response.status_code == 400:
         print("Error! Invalid city input.")
# except:
# print("Unable to connect API.")
exit()

menu_message =  f"Select what you want to display for {city}: " \
                "\n1) Temperature" \
                "\n2) Pressure" \
                "\n3) Humidity" \
                "\n4) All above" \
                "\nYour choice: "

while True:
    try:
        # Jeżeli użytkownik poda wartość, którą uda się skonwertować do integera, to przechodzimy do linijki 21
        user_choice = int(input(menu_message))
        # jeżeli użytkownik wpisze liczbę z zakresu 1-4
        if 0 < user_choice < 5:
            break #wychodzimy z pętli nieskończoności
        else:
            print (f"\n{user_choice} is not supported option. Try again.")
    except ValueError:
        print("\nInvalid input. Try again.")

#api.weatherapi.com/v1/current.json?key=7d164510ae104c8fa46212207230112&q=Warsaw&aqi=yes

#Prepare variables with weather information
temp_c = response['current']['temp_c']
pressure = response['current']['pressure_mb']
humidity = response['current']['humidity']

# Display general weather overview message

translator = Translator(to_lang='pl')
weather_text = response ['current']['condition']['text']
weather_text_pl=translator.translate(weather_text)

print("Weather overview:{weather_text} (PL: {weather_text_pl}).")

# Prepare function to display emojis

def display_weather_icon(temp):
    if temp > 15:
        print("☀️")
    elif temp <= 0:
        print("☃️")
    elif 15 > temp > 0:
        print("🍃")

# Display weather data based on user's input
if user_choice == 1:
    print(f"Temperature for {city} is: {temp_c} degrees.")
elif user_choice == 2:
    print(f"Pressure for {city} is: {pressure} mb.")

elif user_choice == 3:
    print(f"Humidity for {city} is: {humidity} %.")

elif user_choice == 4:
    display_weather_icon(temp=temp_c)
    print(f"Temperature for {city} is: {temp_c} degrees.")
    print(f"Pressure for {city} is: {pressure} mb.")
    print(f"Humidity for {city} is: {humidity} %.")
else:
    print("Invalid data.")

# Save weather data to file
data = { 'City': city,
         'Temperature': temp_c,
         'Pressure': pressure,
         'Humidity': humidity,
         'Weather state': weather_text_pl
         }
df = pd.DataFrame([data])
excel_filename = f'dane_pogoda_{city.lower()}.xlsx' # lower () - changes city name to lowercase
df.to_excel(excel_filename, index=False, engine='openpyxl')