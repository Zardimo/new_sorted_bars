import json
import folium
import yandex_geocoder
from geopy import distance
from operator import itemgetter
import os
import sys
from sys import argv
import time


def get_all_bars(filepath):
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, 'r', encoding='CP1251') as my_file:
            bars = json.load(my_file)
            return bars
    except ValueError:
        return None


def sorting_5_ing_close_bars(bars, input_location):
    sorted_bars = []
    for bar in bars:
        longitude = bar['geoData']['coordinates'][0]
        latitude = bar['geoData']['coordinates'][1]
        bar_coordinate = (latitude, longitude)
        typical_bar = {
        'title': bar['Name'],
        'longitude' : longitude,
        'latitude' : latitude,
        'distance' : distance.distance(bar_coordinate, input_location)
        }
        sorted_bars.append(typical_bar)
    sorted_bars = sorted(sorted_bars, key=itemgetter('distance'))[:5]
    return sorted_bars


def map_mark(input_location, sorted_bars):
    mark_on_map = folium.Map(
        location=input_location,
        zoom_start=17,
        tiles='Stamen Terrain')
    for bar in sorted_bars:
        folium.Marker([bar['latitude'], bar['longitude']], popup='<i>{}</i>'.format(bar['title']), tooltip=bar['title']).add_to(mark_on_map)
    mark_on_map.save('bars_on_map.html')


if __name__ == '__main__':
    if not len(sys.argv) > 1:
        exit('Укажите путь к файлу со списком баров, формата json')
    path_to_json_file = sys.argv[1]
    all_bars = get_all_bars(path_to_json_file)
    if not all_bars:
        exit('Неверно указан путь к файлу с базой')
    input_location = False
    while not input_location:
        try:
            input_location = yandex_geocoder.Client.coordinates(input('Укажите Ваше Местоположение\n'))
        except yandex_geocoder.exceptions.YandexGeocoderAddressNotFound:
            print('Не существующий адрес')
            input_location = False
    input_location = [input_location[1], input_location[0]]
    sorted_bars = sorting_5_ing_close_bars(all_bars, input_location)
    map_mark(input_location, sorted_bars)