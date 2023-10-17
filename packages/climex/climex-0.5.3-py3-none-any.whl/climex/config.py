
import json
import os

import requests


class Config():
    __instance = None

    @staticmethod
    def instance():
        if Config.__instance is None:
            Config()
        return Config.__instance

    def __init__(self):
        if Config.__instance is None:
            Config.__instance = self

            if os.name == 'nt':
                self._climex_dir = os.path.join(
                    os.getenv('APPDATA'), '.climex'
                )
            #elif os.name == 'linux':
            elif os.name == 'posix':
                self._climex_dir = os.path.join(
                    os.getenv('HOME'), '.climex'
                )

            try:
                os.mkdir(self._climex_dir)
            except:
                pass

            try:
                geojson_dir = os.path.join(self._climex_dir, 'GEOJSON')
                os.mkdir(geojson_dir)
            except:
                pass

            try:
                project_dir = os.path.join(self._climex_dir, 'PROJECTS')
                os.mkdir(project_dir)
            except:
                pass


#            self._subdirs = ['CLICOM', 'CLIMDEX', 'CONAGUA', 'GEOJSON', 'INDEX', 'MAP', 'NORMAL', 'PACK', 'PLOT', 'QC', 'SHAPEFILE']

#            self._states = {}

#            for subdir in self._subdirs:
#                try:
#                    os.mkdir(os.path.join(self._climex_dir, subdir))
#                except:
#                    pass

            config_filename = os.path.join(self._climex_dir, 'config.json')

            try:
                with open(config_filename, 'rt') as config_file:
                    self._config = json.load(config_file)
            except:
                self._save_default_config()
        else:
            raise Exception('Multiple Config() instances are not allowed')


    def _save_default_config(self):
        default = {
            'url': {
                'geo': 'https://smn.conagua.gob.mx/tools/RESOURCES/estacion/EstacionesClimatologicas.kmz',
                'obs': 'https://smn.conagua.gob.mx/tools/RESOURCES/Diarios/',
                'month': 'https://smn.conagua.gob.mx/tools/RESOURCES/Mensuales/'
            },
            'subdirs': ['CLIMDEX', 'CONAGUA', 'GEOJSON', 'INDEX', 'MAP', 'MONTHLY', 'NORMAL', 'PACK', 'PLOT', 'QC', 'SHAPEFILE'],
            'states': {
                'AGUASCALIENTES': 'AGUASCALIENTES',
                'BAJA CALIFORNIA': 'BAJA CALIFORNIA',
                'BAJA CALIFORNIA SUR': 'BAJA CALIFORNIA SUR',
                'CAMPECHE': 'CAMPECHE',
                'CHIAPAS': 'CHIAPAS',
                'CHIHUAHUA': 'CHIHUAHUA',
                'COAHUILA DE ZARAGOZA': 'COAHUILA DE ZARAGOZA',
                'COAHUILA': 'COAHUILA DE ZARAGOZA',
                'COLIMA': 'COLIMA',
                'DISTRITO FEDERAL': 'DISTRITO FEDERAL',
                'DF': 'DISTRITO FEDERAL',
                'DURANGO': 'DURANGO',
                'GUANAJUATO': 'GUANAJUATO',
                'GUERRERO': 'GUERRERO',
                'HIDALGO': 'HIDALGO',
                'JALISCO': 'JALISCO',
                'MEXICO': 'MEXICO',
                'MICHOACAN DE OCAMPO': 'MICHOACAN DE OCAMPO',
                'MICHOACAN': 'MICHOACAN DE OCAMPO',
                'MORELOS': 'MORELOS',
                'NAYARIT': 'NAYARIT',
                'NUEVO LEON': 'NUEVO LEON',
                'OAXACA': 'OAXACA',
                'PUEBLA': 'PUEBLA',
                'QUERETARO': 'QUERETARO',
                'QUINTANA ROO': 'QUINTANA ROO',
                'SAN LUIS POTOSI': 'SAN LUIS POTOSI',
                'SINALOA': 'SINALOA',
                'SONORA': 'SONORA',
                'TABASCO':  'TABASCO',
                'TAMAULIPAS': 'TAMAULIPAS',
                'TLAXCALA': 'TLAXCALA',
                'VERACRUZ DE IGNACIO DE LA LLAVE': 'VERACRUZ DE IGNACIO DE LA LLAVE',
                'VERACRUZ': 'VERACRUZ DE IGNACIO DE LA LLAVE',
                'YUCATAN': 'YUCATAN',
                'ZACATECAS': 'ZACATECAS'
            },
            'abbreviations': {
                1: ['AGUASCALIENTES', 'ags'],
                2: ['BAJA CALIFORNIA', 'bc'],
                3: ['BAJA CALIFORNIA SUR', 'bcs'],
                4: ['CAMPECHE', 'camp'],
                5: ['COAHUILA DE ZARAGOZA', 'coah'],
                6: ['COLIMA', 'col'],
                7: ['CHIAPAS', 'chis'],
                8: ['CHIHUAHUA', 'chih'],
                9: ['DISTRITO FEDERAL', 'df'],
                10: ['DURANGO', 'dgo'],
                11: ['GUANAJUATO', 'gto'],
                12: ['GUERRERO', 'gro'],
                13: ['HIDALGO', 'hgo'],
                14: ['JALISCO', 'jal'],
                15: ['MEXICO', 'mex'],
                16: ['MICHOACAN', 'mich'],
                17: ['MORELOS', 'mor'],
                18: ['NAYARIT', 'nay'],
                19: ['NUEVO LEON', 'nl'],
                20: ['OAXACA', 'oax'],
                21: ['PUEBLA', 'pue'],
                22: ['QUERETARO', 'qro'],
                23: ['QUINTANA ROO', 'qroo'],
                24: ['SAN LUIS POTOSI', 'slp'],
                25: ['SINALOA', 'sin'],
                26: ['SONORA', 'son'],
                27: ['TABASCO', 'tab'],
                28: ['TAMAULIPAS', 'tams'],
                29: ['TLAXCALA', 'tlax'],
                30: ['VERACRUZ DE IGNACIO DE LA LLAVE', 'ver'],
                31: ['YUCATAN', 'yuc'],
                32: ['ZACATECAS', 'zac']
            }
        }

        self._config = default

        config_filename = os.path.join(self._climex_dir, 'config.json')

        with open(config_filename, 'wt') as config_file:
            json.dump(self._config, config_file, indent=4)


    def _get_climex_dir(self):
        return self._climex_dir


    def _get_climex_subdirs(self):
        return self._config['subdirs']


    def _get_climex_states(self):
        return self._config['states']


    def _get_climex_state_abbreviations(self):
        return self._config['abbreviations']


    def _get_climex_obs_url(self):
        return self._config['url']['obs']


    def _get_climex_geo_url(self):
        return self._config['url']['geo']


    def _get_climex_month_url(self):
        return self._config['url']['month']


    climex_dir = property(_get_climex_dir)
    climex_subdirs = property(_get_climex_subdirs)
    climex_states = property(_get_climex_states)
    climex_state_abbreviations = property(_get_climex_state_abbreviations)
    climex_obs_url = property(_get_climex_obs_url)
    climex_geo_url = property(_get_climex_geo_url)
    climex_month_url = property(_get_climex_month_url)

