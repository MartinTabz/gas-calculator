import os
import requests
import math
from bs4 import BeautifulSoup
import googlemaps

fuel_type_names = ["Natural 95", "Natural 95+", "Natural 98", "Diesel", "Diesel+"]

def read_config(file_name, prompt_message):
   if os.path.exists(file_name):
      with open(file_name, 'r') as file:
         value = file.read().strip()
         if value:
               return value
   if(file_name == 'fuel_type.txt'):
      i = 1;
      for type in fuel_type_names:
         print(f"{i}. {type}")
         i = i + 1
   value = input(prompt_message)
   with open(file_name, 'w') as file:
      file.write(value)
   return value

api_key = read_config('api_key.txt', 'Vlož svůj Google API klíč: ')
consumption = float(read_config('consumption.txt', 'Vlož spotřebu svého auta (litrů na 100 km): '))
fuel_type = int(read_config('fuel_type.txt', 'Vyber typ paliva: '))

map_client = googlemaps.Client(api_key)

def get_distance_km(start, end):
   try:
      gmap = map_client.directions(start, end, mode="driving", avoid="tolls", departure_time="now", language="cs", units="metric")
      distance = gmap[0]['legs'][0]['distance']['value']
      distance_in_km = float(distance) / 1000
      return distance_in_km
   except ValueError:
      print("Nastala chyba! Pravděpodobně špatné město.")
      return 0

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
   km = get_distance_km(start_destination, end_destination)
   fuel_price = ((km / 100) * consumption) * price
   print("")
   print("Cena benzínu: ",price," Kč")
   print("Vzdálenost: ",km,"km")
   print("Cena: ",(math.ceil(fuel_price / 10) * 10),"Kč")
   print("")

else:
    print("Chyba při načítání stránky. Zkus to později, nebo to oprav.")
