import os
import requests
import math
from bs4 import BeautifulSoup
import googlemaps
import time
import csv

fuel_type_names = ["Natural 95", "Natural 95+", "Natural 98", "Diesel", "Diesel+"]

os.system('cls' if os.name == 'nt' else 'clear')

def read_config(file_name, prompt_message, is_fuel_type=False):
   if os.path.exists(file_name):
      with open(file_name, 'r') as file:
         value = file.read().strip()
         if value:
               return value
   if is_fuel_type:
      for i, type_name in enumerate(fuel_type_names, start=1):
         print(f"{i}. {type_name}")
   value = input(prompt_message)
   with open(file_name, 'w') as file:
      file.write(value)
   return value

def change_config(file_name, prompt_message, is_fuel_type=False):
   os.system('cls' if os.name == 'nt' else 'clear')
   if is_fuel_type:
      for i, type_name in enumerate(fuel_type_names, start=1):
         print(f"{i}. {type_name}")
      print("")
   value = input(prompt_message)
   with open(file_name, 'w') as file:
      file.write(value)
   print("")
   print("Změna proběhla vpořádku")
   time.sleep(1)
   os.system('cls' if os.name == 'nt' else 'clear')
   return value

def get_distance_km(start, end):
   try:
      gmap = map_client.directions(start, end, mode="driving", avoid="tolls", departure_time="now", language="cs", units="metric")
      metres = gmap[0]['legs'][0]['distance']['value']
      distance = gmap[0]['legs'][0]['distance']['text']
      duration = gmap[0]['legs'][0]['duration']['text']
      seconds = gmap[0]['legs'][0]['duration']['value']
      return metres, distance, seconds, duration
   except ValueError:
      print("Nastala chyba! Pravděpodobně špatné město.")
      return 0

def calculate_distance():
   url = "https://tank-ono.cz/cz/index.php?page=cenik"
   response = requests.get(url)

   if response.status_code == 200:
      soup = BeautifulSoup(response.content, 'html.parser')
      raw_price_element = soup.find("body").find_all("div")[4].find_all("table")[0].find_all("tr")[3].find_all("td")[fuel_type]
      price_string = raw_price_element.get_text()
      price = float(price_string.replace(",", "."))
      print("")
      start_destination = input("Napiš z jakého města jedeš: ")
      end_destination = input("Napiš do jakého města jedeš: ")
      metres, distance, seconds, duration = get_distance_km(start_destination, end_destination)
      km = float(metres) / 1000
      fuel_price = ((km / 100) * consumption) * price
      os.system('cls' if os.name == 'nt' else 'clear')
      print("")
      print("Trvání: ", duration)
      print("Vzdálenost: ", distance)
      print("Cena: ", (math.ceil(fuel_price / 10) * 10), "Kč")
      print("")

      with open('cesty.csv', mode='a', newline='') as file:
         writer = csv.writer(file)
         if os.stat('cesty.csv').st_size == 0:
            writer.writerow(["Datum", "Start", "Cil", "Vzdalenost", "Trvani", "Cena"])
         writer.writerow([time.strftime("%Y-%m-%d"), start_destination, end_destination, metres, seconds, (math.ceil(fuel_price / 10) * 10)])
   else:
      print("Chyba při načítání stránky. Zkus to později, nebo to oprav.")

def menu():
    while True:
      print("")
      print("")
      print("1. Vypočítat vzdálenost")
      print("")
      print("2. Změnit API klíč")
      print("3. Změnit spotřebu")
      print("4. Změnit typ paliva")
      print("")
      print("5. Vypnout")
      print("")
      choice = input("Výběr: ")

      if choice == '1':
         os.system('cls' if os.name == 'nt' else 'clear')
         calculate_distance()
      elif choice == '2':
         global api_key
         api_key = change_config('api_key.txt', 'Vlož svůj Google API klíč: ')
         global map_client
         map_client = googlemaps.Client(api_key)
      elif choice == '3':
         global consumption
         consumption = float(change_config('consumption.txt', 'Vlož spotřebu svého auta (litrů na 100 km): '))
      elif choice == '4':
         global fuel_type
         fuel_type = int(change_config('fuel_type.txt', 'Vyber typ paliva: ', is_fuel_type=True))
      elif choice == '5':
         break
      else:
         print("Neplatná volba, zkuste to znovu.")

api_key = read_config('api_key.txt', 'Vlož svůj Google API klíč: ')
consumption = float(read_config('consumption.txt', 'Vlož spotřebu svého auta (litrů na 100 km): '))
fuel_type = int(read_config('fuel_type.txt', 'Vyber typ paliva: ', is_fuel_type=True))

map_client = googlemaps.Client(api_key)

menu()
