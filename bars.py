import json
import folium
import yandex_geocoder
from geopy import distance
from operator import itemgetter
import os
import sys
from sys import argv
import time
from flask import Flask
import webbrowser


def get_all_bars(filepath):
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, 'r', encoding='CP1251') as my_file:
            bars = json.load(my_file)
            return bars
    except ValueError:
        return None


def get_bars_with_distance(bars, input_location):
    nearest_bars = []
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
        nearest_bars.append(typical_bar)
    nearest_bars = sorted(nearest_bars, key=itemgetter('distance'))[:5]
    return nearest_bars


def map_mark(input_location, sorted_bars, filename):
    mark_on_map = folium.Map(
        location=input_location,
        zoom_start=17,
        tiles='Stamen Terrain')
    for bar in sorted_bars:
        folium.Marker([bar['latitude'], bar['longitude']], popup='<i>{}</i>'.format(bar['title']), tooltip=bar['title']).add_to(mark_on_map)
    mark_on_map.save(filename)


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
    sorted_bars = get_bars_with_distance(all_bars, input_location)
    html_name = 'bars_on_map.html'
    map_mark(input_location, sorted_bars, html_name)
    path_to_map_file = os.path.join(os.getcwd(), html_name)
    webbrowser.open(path_to_map_file)