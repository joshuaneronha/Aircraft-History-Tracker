import pandas as pd
import numpy as np
import urllib
from bs4 import BeautifulSoup
import requests
from config import *

with open("flights.html", "rb") as file:
    html = BeautifulSoup(file, 'html.parser')

flights_table = pd.read_html(str(html))[0]
reg_list = list(flights_table[~flights_table['Reg'].isna()]['Reg'])

reg_list



schedule = requests.get('https://airlabs.co/api/v9/flights?api_key=' + AIRLABS_API_KEY + '&flag=US').json()['response']

currently_flying = []

for i in schedule:
    try:
        if i['reg_number'] in reg_list:
            currently_flying.append([i['reg_number'], i['flight_iata'], i['dep_iata'], i['arr_iata'],i['aircraft_icao'], i['lat'], i['lng']])
    except:
        pass

currently_flying

i
