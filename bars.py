import json
import folium
from yandex_geocoder import Client
from geopy import distance
from operator import itemgetter
import os
import sys
from sys import argv


def get_all_bars(filepath):
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, 'r', encoding='CP1251') as my_file:
            bars_list = json.load(my_file)
            return bars_list
    except ValueError:
        return None


def create_bar_list(bars_list, bar_input):
	sorted_bars = []
	for i in range(len(bars_list)):
		longitude = bars_list[i]['geoData']['coordinates'][0]
		latitude = bars_list[i]['geoData']['coordinates'][1]
		bar_coordinate = (latitude, longitude)
		typing_bar = {
		'title': bars_list[i]['Name'],
		'longitude' : longitude,
		'latitude' : latitude,
		'distance' : distance.distance(bar_coordinate, bar_input)
		}
		sorted_bars.append(typing_bar)
	sorted_bars = sorted(sorted_bars, key=itemgetter('distance'))[0:5]
	return sorted_bars


def marker_on_map(bar_input, sorted_bars):
	m = folium.Map(
		location=bar_input,
		zoom_start=17,
		tiles='Stamen Terrain')
	for bar in range(len(sorted_bars)):
		folium.Marker([sorted_bars[bar]['latitude'], sorted_bars[bar]['longitude']], popup='<i>{}</i>'.format(sorted_bars[bar]['title']), tooltip=sorted_bars[bar]['title']).add_to(m)
	m.save('bars_on_map.html')


if __name__ == '__main__':
    if not len(sys.argv) > 1:
        exit("Укажите путь к файлу со списком баров, формата json")
    if get_all_bars(sys.argv[1]) is None:
    	exit('Неверно указан путь к файлу с базой')
    bar_input = False
    while bar_input == False:
	    try:
	        bar_input = Client.coordinates(input('Укажите Ваше Местоположение\n'))
	    except BaseException:
    		print('Не существующий адрес')
    		bar_input = False
    bar_input = [bar_input[1], bar_input[0]]
    sorted_bars = create_bar_list(get_all_bars(sys.argv[1]), bar_input)
    marker_on_map(bar_input, sorted_bars)