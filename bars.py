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


def sorted_5_close_bars(bars, bar_input):
    sorted_bars = []
    for bar in bars:
        longitude = bar['geoData']['coordinates'][0]
        latitude = bar['geoData']['coordinates'][1]
        bar_coordinate = (latitude, longitude)
        typing_bar = {
        'title': bar['Name'],
        'longitude' : longitude,
        'latitude' : latitude,
        'distance' : distance.distance(bar_coordinate, bar_input)
        }
        sorted_bars.append(typing_bar)
    sorted_bars = sorted(sorted_bars, key=itemgetter('distance'))[:5]
    return sorted_bars


def marker_on_map(bar_input, sorted_bars):
    mark_on_map = folium.Map(
        location=bar_input,
        zoom_start=17,
        tiles='Stamen Terrain')
    for bar in sorted_bars:
        folium.Marker([bar['latitude'], bar['longitude']], popup='<i>{}</i>'.format(bar['title']), tooltip=bar['title']).add_to(mark_on_map)
    mark_on_map.save('bars_on_map.html')


if __name__ == '__main__':
    if not len(sys.argv) > 1:
        exit('Укажите путь к файлу со списком баров, формата json')
    path_to_json = sys.argv[1]
    if get_all_bars(path_to_json) is None:
        exit('Неверно указан путь к файлу с базой')
    bar_input = False
    while bar_input == False:
        try:
            bar_input = yandex_geocoder.Client.coordinates(input('Укажите Ваше Местоположение\n'))
        except yandex_geocoder.exceptions.YandexGeocoderAddressNotFound:
            print('Не существующий адрес')
            bar_input = False
    bar_input = [bar_input[1], bar_input[0]]
    sorted_bars = sorted_5_close_bars(get_all_bars(path_to_json), bar_input)
    marker_on_map(bar_input, sorted_bars)