
#import datetime
#import glob
import json
import os

import requests

import climex.base as base

from . config import Config

class Station():
    __instance = None

    @staticmethod
    def instance():
        if Station.__instance is None:
            Station()
        return Station.__instance

    def __init__(self):
        if Station.__instance is None:
            Station.__instance = self

            station_by_id_filename = os.path.join(
                Config.instance().climex_dir, 'GEOJSON', 'conagua_all_by_id.json'
            )

            try:
                with open(station_by_id_filename, 'rt') as station_by_id_file:
                    self._station_by_id = json.load(station_by_id_file)
            except:
                base.geojson()

            try:
                with open(station_by_id_filename, 'rt') as station_by_id_file:
                    self._station_by_id = json.load(station_by_id_file)
            except:
                print('climex.Station: CONAGUA database not available')

        else:
            raise Exception('Multiple Station() instances are not allowed')

    def _station(self, station):
        try:
            return self._station_by_id[str(station)]
        except:
            return {}

    def _name(self, station):
        try:
            return self._station_by_id[str(station)]['properties']['Nombre'].title()
        except:
            return {}


    def _name_state(self, station):
        try:
            name = self._station_by_id[str(station)]['properties']['Nombre'].title()
            state = self._station_by_id[str(station)]['properties']['Estado'].title()

            return f"{name} ({state})"
        except:
            return {}


    def _operating(self, station):
        try:
            if self._station_by_id[str(station)]['properties']['Actividad'] == 'OPERANDO':
                return True
            else:
                return False
        except:
            return None
        

    def _url(self, station):
        try:
            return self._station_by_id[str(station)]['properties']['URL']
        except:
            return ''

    def _exists(self, station):
        try:
            return bool(self._station_by_id[str(station)])
        except:
            return False
