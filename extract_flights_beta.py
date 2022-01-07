import pandas as pd
import numpy as np
import urllib
from bs4 import BeautifulSoup
import requests
from config import *
from PIL import Image, ImageDraw
from io import BytesIO
import base64
import json
import ftplib

coords = pd.read_csv('airport-codes_csv.csv',usecols=['iata_code', 'coordinates'])

lat_top = 49.39
lat_bottom = 23.81
lon_left = -127.99
lon_right = -61

lat_space = np.linspace(lat_top, lat_bottom, 32)
lon_space = np.linspace(lon_left, lon_right, 64)

lat_top_i = 53.03
lat_bottom_i = 15.86
lon_left_i = -127.84
lon_right_i = -67

lat_space_i = np.linspace(lat_top_i, lat_bottom_i, 32)
lon_space_i = np.linspace(lon_left_i, lon_right_i, 40)

color = ['#000000','#000000','#000000']

def generate_image(base_map, array, state):
    im = Image.open(base_map)
    indiv_ims = []
    draw = ImageDraw.Draw(im)

    for i in array:
        origin = get_coords(i[2])
        dest = get_coords(i[3])
        current = (i[5], i[6])
        airline = i[1][0:2]

        if airline == 'AA':
            color[1] = '#B61F23'
            color[0] = '#0B448C'
            color[2] = '#ffffff'
        if airline == 'DL':
            color[0] = '#E41C34'
            color[1] = '#9C1C34'
            color[2] = '#113462'
        if airline == 'B6':
            color[0] = '#043474'
            color[2] = '#459EDE'
            color[1] = '#4f9b4a'
        if airline == 'WN':
            color[0] = '#FBAC1C'
            color[1] = '#2C4298'
            color[2] = '#DC1B23'

        current_x_point = np.abs(np.array([x - current[0] for x in lat_space])).argmin() + 1
        current_y_point = np.abs(np.array([x - current[1] for x in lon_space])).argmin() + 1
        #
        draw.line((current_y_point - 1,current_x_point, current_y_point + 1,current_x_point),width=1,fill=color[state])
        draw.line((current_y_point,current_x_point - 1, current_y_point,current_x_point + 1),width=1,fill=color[state])

        # draw.point((current_y_point,current_x_point))
        # draw.rectangle([current_y_point,current_x_point,current_y_point + 1,current_x_point + 1],fill=color[state])

    return im

def generate_image_ind(base_map, array):

    im_list = []

    for i in array:

        im_ind = Image.open(base_map)

        origin = get_coords(i[2])
        dest = get_coords(i[3])
        current = (i[5], i[6])
        airline = i[1][0:2]

        if airline == 'AA':
            color[1] = '#B61F23'
            color[0] = '#0B448C'
            color[2] = '#ffffff'
        if airline == 'DL':
            color[0] = '#E41C34'
            color[1] = '#9C1C34'
            color[2] = '#113462'
        if airline == 'B6':
            color[0] = '#043474'
            color[2] = '#459EDE'
            color[1] = '#4f9b4a'
        if airline == 'WN':
            color[0] = '#FBAC1C'
            color[1] = '#2C4298'
            color[2] = '#DC1B23'

        origin_x_point = np.abs(np.array([x - origin[0] for x in lat_space_i])).argmin() + 1
        origin_y_point = np.abs(np.array([x - origin[1] for x in lon_space_i])).argmin() + 1
        dest_x_point = np.abs(np.array([x - dest[0] for x in lat_space_i])).argmin() + 1
        dest_y_point = np.abs(np.array([x - dest[1] for x in lon_space_i])).argmin() + 1
        current_x_point = np.abs(np.array([x - current[0] for x in lat_space_i])).argmin() + 1
        current_y_point = np.abs(np.array([x - current[1] for x in lon_space_i])).argmin() + 1

        draw2 = ImageDraw.Draw(im_ind)

        draw2.line((origin_y_point, origin_x_point, dest_y_point, dest_x_point), width = 1, fill = color[0])

        draw2.line((current_y_point - 1,current_x_point, current_y_point + 1,current_x_point),width=1,fill='#32383b')
        draw2.line((current_y_point,current_x_point - 1, current_y_point,current_x_point + 1),width=1,fill='#32383b')

        im_list.append(im_ind)

    return im_list

def get_coords(airport):
    extracted = coords[coords['iata_code'] == airport]['coordinates'].iloc[0].split(', ')
    extracted.reverse()
    return tuple([float(x) for x in extracted])


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

zero = generate_image('base_map.png',currently_flying,0)
one = generate_image('base_map.png',currently_flying,1)
two = generate_image('base_map.png',currently_flying,2)

buffered = BytesIO()
zero.save(buffered, format="PNG")
buffered.seek(0)
zero_str = base64.b64encode(buffered.getvalue()).decode()

buffered = BytesIO()
one.save(buffered, format="PNG")
buffered.seek(0)
one_str = base64.b64encode(buffered.getvalue()).decode()

buffered = BytesIO()
two.save(buffered, format="PNG")
buffered.seek(0)
two_str = base64.b64encode(buffered.getvalue()).decode()

data_dict = {'frame_one': zero_str, 'frame_two': one_str, 'frame_three': two_str}

# individual_maps

ims = generate_image_ind('individual_map.png', currently_flying)

b64_list = []



for i in ims:
    buffered = BytesIO()
    i.save(buffered, format="PNG")
    buffered.seek(0)
    b64_list.append(base64.b64encode(buffered.getvalue()).decode())

df = pd.DataFrame(currently_flying,columns=['reg','iata_code','dep_iata','arr_iata','model','lat','lng'])
df['map'] = b64_list


json_rep = df.to_dict(orient='index')

data_dict['indiv_flights'] = json_rep
data_dict['max_entry'] = str(int(len(b64_list) - 1))


with open("current_locations.json", "w") as outfile:
    json.dump(data_dict,outfile)

ftp_server = ftplib.FTP(HOST_NAME,FTP_USER,FTP_PASS)
filename = "/public_html/resources/current_locations.json"

with open("current_locations.json", "rb") as upfile:
    ftp_server.storbinary(f"STOR {filename}", upfile)
