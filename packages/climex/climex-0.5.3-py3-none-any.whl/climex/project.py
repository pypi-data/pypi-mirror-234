
import datetime
import distutils.dir_util
import glob
#import io
import json
import math
import os
import random
import sys
import warnings
import webbrowser
import zipfile

import easygui
import folium
import matplotlib.pyplot as plt
import openpyxl
import requests
import shapefile
import xlrd

import climex.base as base
import climex.geo as geo
import climex.klimdex as klimdex
import climex.normal as normal
#import plot
import climex.qc as qc
#from climdex import Index

from . config import Config
from . station import Station


class Project():
    
    def __init__(self, name, operating=True, overwrite=False):

        update = True
        right_now = datetime.datetime.now()

        self._name = name.upper()
        self._baseline = [1961, 1990]
        self._operating = bool(operating)
        self._overwrite = bool(overwrite)
        self._created = right_now.strftime('%Y-%m-%d %H:%M:%S')
        self._updated = right_now.strftime('%Y-%m-%d %H:%M:%S')
        self._source = None
        self._stations = []

        self._project_dir = os.path.join(Config.instance().climex_dir, 'PROJECTS', name.upper())

        #self._min_baseline_length = 10
        self._min_baseline_length = 5

        self._clicom_dir = os.path.join(Config.instance().climex_dir, 'PROJECTS', name.upper(), 'CLICOM')

        try:
            os.mkdir(self._project_dir)
            self._stations = []
        except FileExistsError:
            print(f'climex.Project(): Project {name.upper()} already exists')

            update = False

            try:
                project_filename = os.path.join(self._project_dir, 'project.json')

                with open(project_filename, 'rt') as project_file:
                    project_json = json.load(project_file)

                self._baseline = project_json['baseline']
                self._operating = project_json['operating']
                #self._overwrite = project_json['overwrite']
                self._created = project_json['created']
                self._updated = project_json['updated']
                self._stations = project_json['stations']
            except:
                self._stations = []

        for subdir in Config.instance().climex_subdirs:
            try:
                os.mkdir(os.path.join(self._project_dir, subdir))
            except:
                pass

        self.save(update)

    def __repr__(self):
        try:
            project_filename = os.path.join(self._project_dir, 'project.json')

            with open(project_filename, 'rt') as project_file:
                project_json = json.load(project_file)
        except:
            project_json = {
                'created': self._created,
                'updated': self._updated,
                'operating': self._operating,
                'baseline': self._baseline,
                'stations': self._stations
            }
        
        return json.dumps(project_json, indent=4)

    def _get_operating(self):
        return self._operating

    def _set_operating(self, operating):
        self._operating = bool(operating)
        self.save()

    def _get_baseline(self):
        return self._baseline

    def _set_baseline(self, baseline):
        try:
            start, end = baseline
        except:
            return

        if isinstance(start, int) and isinstance(end, int):
            if end + 1 - start < self._min_baseline_length:
                return
            if start <= end:
                self._baseline = [start, end]
                self.save()

    def _get_stations(self):
        return self._stations

    def _set_stations(self, list_of_stations):

        if isinstance(list_of_stations, list) and len(list_of_stations) == 0:
            self._stations = []
            self.save()
            return
        
        if not isinstance(list_of_stations, list):
            list_of_stations = [list_of_stations]

        updated = False
        updated_stations = self._stations
        for station in list_of_stations:
            if not Station.instance()._exists(str(station)):
                print(f'climex.Project.stations: station {station} not found on CONAGUA DB (not added to the project).')
                continue
            if self._operating:
                if not Station.instance()._operating(str(station)):
                    print(f'climex.Project.stations: station {station} is not operating (not added to the project).')
                    continue

            if str(station) not in self._stations:
                updated_stations.append(str(station))
                updated = True

        if updated:
            self._stations = sorted(updated_stations)
            self.save()

    def _get_dataset(self, station, baseline=None, edits=False):

        if str(station) not in self.stations:
            return []

        if edits:
            edits_filename = os.path.join(self._project_dir, 'edits.json')

            try:
                with open(edits_filename, 'rt') as edits_file:
                    edit_tasks = json.load(edits_file)
            except:
                edit_tasks = {}

        if baseline is None:
            base_1, base_2 = self.baseline
        else:
            try:
                base_1, base_2 = baseline
            except:
                base_1, base_2 = self.baseline

        climdex_filename = os.path.join(self._project_dir, 'CLIMDEX', f'{station}_{base_1}_{base_2}.txt')


        """
        try:
            with open(climdex_filename, 'rt') as climdex_file:
                climdex_contents = climdex_file.readlines()
        except:
            print(f'climex.Project._get_dataset(): data file for station {station} not found. Run climex.Project.qc()')
            return

        #print(climdex_filename)
        """

        if not os.path.isfile(climdex_filename):
            return
            #self.qc()

        with open(climdex_filename, 'rt') as climdex_file:
            climdex_contents = climdex_file.readlines()


        climdex_dataset = []
        for record in climdex_contents:
            fields = record.split()

            year = int(fields[0])
            month = int(fields[1])
            day = int(fields[2])
            prcp = float(fields[3])
            tmax = float(fields[4])
            tmin = float(fields[5])

            if edits:
                try:
                    pass
                except:
                    pass

            climdex_dataset.append([year, month, day, prcp, tmax, tmin])

        return climdex_dataset

    def _project_dir_exists(self):
        return os.path.isdir(self._project_dir)

    def _check_download(self):
        """Returns True if CONAGUA files are found, False otherwise"""

        check = True
        for station in self.stations:
            conagua_filename = os.path.join(self._project_dir, 'CONAGUA', f'{station}.txt')
            climdex_filename = os.path.join(self._project_dir, 'CLIMDEX', f'{station}.txt')

            if not os.path.isfile(conagua_filename):
                check = False
                break

            if not os.path.isfile(climdex_filename):
                check = False
                break

        return check

    def _check_qc(self):
        """Returns True if QC files are found, False otherwise"""

        base_1, base_2 = self.baseline

        check = True
        for station in self.stations:
            qc0_filename = os.path.join(self._project_dir, 'QC', f'{station}_{base_1}_{base_2}_qc0.json')
            climdex_filename = os.path.join(self._project_dir, 'CLIMDEX', f'{station}_{base_1}_{base_2}.txt')

            if not os.path.isfile(qc0_filename):
                check = False
                break

            if not os.path.isfile(climdex_filename):
                check = False
                break

        return check

    def _get_minimum_baseline_length(self):
        return self._min_baseline_length

    def _set_minimum_baseline_length(self, baseline_length):
        if isinstance(baseline_length, int):
            if baseline_length > 0:
                self._min_baseline_length = baseline_length

    operating = property(_get_operating, _set_operating)
    baseline = property(_get_baseline, _set_baseline)          
    stations = property(_get_stations, _set_stations)
    minimum_baseline_length = property(_get_minimum_baseline_length, _set_minimum_baseline_length)


    def bbox(self, longitude_min, latitude_min, longitude_max, latitude_max):
        """Adds stations within bounding box to current project"""

        if self._operating:
            geo_filename = os.path.join(Config.instance().climex_dir, 'GEOJSON', 'conagua_operating.geojson')
        else:
            geo_filename = os.path.join(Config.instance().climex_dir, 'GEOJSON', 'conagua_all.geojson')

        geojson = {}

        try:
            with open(geo_filename, 'rt') as geo_file:
                geojson = json.load(geo_file)
        except:
            base.geojson()

        if not geojson:
            try:
                with open(geo_filename, 'rt') as geo_file:
                    geojson = json.load(geo_file)
            except:
                return

        bbox_rectangle = [longitude_min, latitude_min, longitude_max, latitude_max]
        bbox_stations = self._stations
        for feature in geojson['features']:
            x, y = feature['geometry']['coordinates'][:2]
            if geo.point_in_rectangle(x, y, bbox_rectangle) and feature['id'] not in self._stations:
                bbox_stations.append(feature['id'])

        self._stations = sorted(bbox_stations)

        self.save()


    def state(self, state_name):
        """Adds stations from 'state_name' to current project"""

        if self._operating:
            state_filename = os.path.join(Config.instance().climex_dir, 'GEOJSON', 'conagua_operating_by_state.json')
        else:
            state_filename = os.path.join(Config.instance().climex_dir, 'GEOJSON', 'conagua_all_by_state.json')

        state_json = {}

        try:
            with open(state_filename, 'rt') as state_file:
                state_json = json.load(state_file)
        except:
            base.geojson()

        if not state_json:
            try:
                with open(state_filename, 'rt') as state_file:
                    state_json = json.load(state_file)
            except:
                return

        try:
            state_stations = self._stations
            for feature in state_json[state_name.upper()]:
                if feature['id'] not in state_stations:
                    state_stations.append(feature['id'])

            self._stations = sorted(state_stations)
            self.save()
        except KeyError:
            return


    def save(self, update=True):
        """Saves the state of current project to disk file 'project.json'"""

        right_now = datetime.datetime.now()

        if update:
            updated = right_now.strftime('%Y-%m-%d %H:%M:%S')
        else:
            updated = self._updated

        project_contents = {
            'source': self._source,
            'created': self._created,
            'updated': updated,
            'operating': self._operating,
            'baseline': self._baseline,
            'stations': self._stations
        }

        project_filename = os.path.join(self._project_dir, 'project.json')
        with open(project_filename, 'wt') as project_file:
            json.dump(project_contents, project_file, indent=4)


    def contents(self):
        """Prints all data files in current project"""

        number_of_items = 0

        current_project_contents = {}

        project_contents = glob.glob(os.path.join(self._project_dir, '*'))
        for item in project_contents:
            if os.path.basename(item) not in Config.instance()._config['subdirs']:
                continue

            current_project_contents[item] = []

            dir_contents = sorted(glob.glob(os.path.join(item, '*')))
            for subitem in dir_contents:
                number_of_items += 1
                current_project_contents[item].append(os.path.basename(subitem))

        if number_of_items == 0:
            print(f'climex.Project.contents: project {self._name} is empty')
        else:
            for item, subitems in current_project_contents.items():
                if len(subitems) > 0:
                    print(f'\n[{item}]\n')
                    for subitem in subitems:
                        print(f'   {os.path.basename(subitem)}')
            print()


    def clean(self):
        """Removes all contents from current project"""

        project_contents = glob.glob(os.path.join(self._project_dir, '*'))
        for item in project_contents:
            if os.path.basename(item) not in Config.instance()._config['subdirs']:
                continue

            dir_contents = glob.glob(os.path.join(item, '*'))
            for subitem in dir_contents:
                os.remove(subitem)

        self._stations = []
        self.save()


    def remove(self, list_of_stations):
        """Removes stations from current project"""

        if not isinstance(list_of_stations, list):
            list_of_stations = [list_of_stations]

        list_of_stations = list(map(str, list_of_stations))

        updated_stations = []
        for station in self._stations:
            if str(station) not in list_of_stations:
                updated_stations.append(str(station))

        if len(updated_stations) != len(self._stations):
            self._stations = updated_stations
            self.save()

            # TODO: Delete all files from updated_stations


    def copy(self, destination_name):
        """Copies current project to a new location"""

        destination_dir = os.path.join(
            Config.instance()._climex_dir, 'PROJECTS', destination_name.upper()
        )

        try:
            os.mkdir(destination_dir)
        except:
            print('climex.Project.copy(): target project already exists (source project not copied)')
            return

        distutils.dir_util.copy_tree(self._project_dir, destination_dir)

        print(f'climex.Project.copy(): source project copied to {destination_dir}')


    def pack(self):
        """Packs all files from current project in a ZIP file""" 

        if 'easygui' not in sys.modules.keys():
            print('climex.Project.pack(): Package "easygui" not found (pip install easygui)')
            return

        default_name = self._name.lower()
        
        zip_filename = easygui.filesavebox(
            msg='Zip CLIMEX dataset', default=default_name + '.zip',
            filetypes=['*.zip']
        )
    
        if zip_filename is None:
            return

        zip_object = zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED)

        root_length = len(self._project_dir) + 1

        for base, dirs, files in os.walk(self._project_dir):
            for file in files:
                filename = os.path.join(base, file)
                zip_object.write(filename, filename[root_length:])

        zip_object.close()


    def download(self, overwrite=True):
        """Downloads data files of all stations in current project"""

        if not self._project_dir_exists():
            return
# TODO: catch download erros and go to next station??
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'}





##        failed_a = []

        print('\nDownloading daily data...\n')
        
        for station in self._stations:

            if not overwrite:
                print('do not overwrite, not yet implemented')
                # TODO
                # get filename
                # Check it exists
                # if it exists, continue to next station
                
            url = f'{Config.instance().climex_obs_url}{station}.txt'

            print(f'Downloading  {url:70s}', end='')

##            try:
##                ornament = ' '
##                response = requests.get(url, headers=headers)
##            except:
##                ornament = '*'
##                warnings.filterwarnings('ignore')
##                response = requests.get(url, headers=headers, verify=False)
##
##                warnings.filterwarnings('always')

            try:
                response = requests.get(url, headers=headers)
                print(f'\t[{response.status_code}]')
            except requests.exceptions.RequestException as conagua_error:
                print(f'\t[{response.status_code}]')
                print(f'Project.download(): {conagua_error}')
                return

            if response.status_code != 200:
                failed_a.append(station)
                print(f'\t[{response.status_code}]')
                continue

            conagua_filename = os.path.join(self._project_dir, 'CONAGUA', f'{station}.txt')

            with open(conagua_filename, 'wt', encoding='utf-8') as conagua_file:
                conagua_file.write(response.text)

            conagua_data = response.text.split('\n')

            # Remove this when online //////////////////////////////
            #with open(conagua_filename, 'rt') as conagua_file:
            #    conagua_data = conagua_file.read().split('\n')
            # Remove this when online //////////////////////////////

            climdex_filename = os.path.join(self._project_dir, 'CLIMDEX', f'{station}.txt')

            # Convert to CLIMDEX format
            climdex_data = ''
            for record in conagua_data:

                try:
                    date, prcp, evap, tmax, tmin = record.split()
                except:
                    continue

                if prcp == 'Nulo': prcp = klimdex.null
                if evap == 'Nulo': evap = klimdex.null
                if tmax == 'Nulo': tmax = klimdex.null
                if tmin == 'Nulo': tmin = klimdex.null

                try:                    
                    prcp, evap, tmax, tmin = map(float, (prcp, evap, tmax, tmin))
                except:
                    continue

                day, month, year = date.split('/')

                climdex_record = f'{year:4s} {month:2s} {day:2s} {prcp:6.1f} {tmax:6.1f} {tmin:6.1f}\n'
                climdex_data += climdex_record

            with open(climdex_filename, 'wt') as climdex_file:
                climdex_file.write(climdex_data)

##            print(f'\t[{response.status_code}]')
##            print(f'\t{ornament}[{response.status_code}]')

##        if len(failed_a) > 0:
##            print('Retrying...')
##
##            # TODO: but apparently not necessary

        if self._source is None:
            self._source = 'CONAGUA'
            self.save()
        elif 'CONAGUA' not in self._source.upper():
            self._source += ':' + 'CONAGUA'
            print('Project.download(): project \'source\' field updated {}')
            self.save()


        print('\nDownloading monthly data...\n')

        for station in self._stations:
            
            state_index = str(int(station) // 1000)

            state_name = Config.instance().climex_state_abbreviations[state_index][-1]

            filename = f'{int(station):08d}.TXT'
            
            url = f'{Config.instance().climex_month_url}{state_name}/{filename}'

            print(f'Downloading  {url:70s}', end='')
            
            try:
                response = requests.get(url, headers=headers)
                print(f'\t[{response.status_code}]')
            except requests.exceptions.RequestException as conagua_error:
                print(f'\t[{response.status_code}]')
                print(f'Project.download(): {conagua_error}')
                return

            if response.status_code != 200:
                failed_a.append(station)
                print(f'\t[{response.status_code}]')
                continue

            print(response.text)

            conagua_filename = os.path.join(self._project_dir, 'CONAGUA', filename)

            with open(conagua_filename, 'wt', encoding='utf-8') as conagua_file:
                conagua_file.write(response.text)

##            conagua_data = response.text.split('\n')




    def describe(self):
        """Prints a brief description of the project"""

        print(f'\nProject name: {self._name}')
        print(f'Baseline: {self._baseline}')
        print(f'Number of stations: {len(self._stations)}')
        print(f'Operating: {self._operating}\n')


    def length(self):
        """Prints the length of observation periods for all stations in current project"""

        if not self._project_dir_exists():
            return

        if len(self._stations) == 0:
            return

        id_filename = os.path.join(Config.instance().climex_dir, 'GEOJSON', 'conagua_all_by_id.json')

        try:
            with open(id_filename, 'rt') as id_file:
                id_json = json.load(id_file)
        except:
            base.geojson()

        try:
            with open(id_filename, 'rt') as id_file:
                id_json = json.load(id_file)
        except:
            return

        base_1, base_2 = self._baseline

        b1 = '-'.join([str(base_1), '01', '01'])
        b2 = '-'.join([str(base_2), '12', '31'])

        b1_max = '0000-00-00'
        b2_min = '9999-99-99'
        number_of_processed_stations = 0
        number_of_wrong_stations = 0
        for station in self._stations:
            climdex_filename = os.path.join(self._project_dir, 'CLIMDEX', f'{station}.txt')

            try:
                with open(climdex_filename, 'rt') as climdex_file:
                    climdex_contents = climdex_file.readlines()
            except:
                print(f'climex.length(): data file for station {station} not found. Run climex.Project.download()')
                continue

            number_of_processed_stations += 1

            first_record_date = '-'.join(climdex_contents[0].split()[:3])
            last_record_date = '-'.join(climdex_contents[-1].split()[:3])

            if first_record_date > b1_max:
                b1_max = first_record_date

            if last_record_date < b2_min:
                b2_min = last_record_date

            if first_record_date <= b1 and last_record_date >= b2:
                test = '[OK]'
            else:
                test = '[WRONG]'
                number_of_wrong_stations += 1

            if id_json[station]['properties']['Actividad'] == 'OPERANDO':
                status = 'OPERATING'
            elif id_json[station]['properties']['Actividad'] == 'SUSPENDIDA':
                status = 'SUSPENDED'
            else:
                status = '---------'

            print(f'{station}    {status}    {first_record_date}    {last_record_date}    {test}')

        print()
        
        if number_of_processed_stations == 0:
            return

        if number_of_wrong_stations == 0:
            print(f'climex.Project.length: all stations agree with current baseline ({base_1}-{base_2})') 
        else:
            print(f'climex.Project.length: {number_of_wrong_stations} stations do not agree with current baseline ({base_1}-{base_2})')
            if b1_max >= b2_min:
                print(f'                       Common baseline not found')
            else:
                print(f'                       Maximum common baseline: {b1_max}-{b2_min}')


    def missing(self, base_1=None, base_2=None, variable='prcp'):
        """Prints missing values for all stations in current project"""

        if not self._project_dir_exists():
            return

        if len(self._stations) == 0:
            return

        if variable.upper() not in ('PRCP', 'TMAX', 'TMIN'):
            return

        if base_1 is None:
            base_1, base_2 = self.baseline
        elif base_1 is not None and base_2 is None:
            base_2 = base_1 + 1

        if not isinstance(base_1, int) or not isinstance(base_2, int):
            return

        missing_dataset = {}
        for station in self.stations:

            missing_dataset[station] = {}

            for year in range(base_1, base_2 + 1):
                missing_dataset[station][year] = {}
                missing_dataset[station][year]['year'] = 0
                for month in range(1, 13):
                    missing_dataset[station][year][month] = 0

        for station in self.stations:
            dataset = self._get_dataset(station)
            #print(dataset[0])
            for record in dataset:
                year, month, day, prcp, tmax, tmin = record
                #print(record)

                if variable == 'prcp' and prcp == klimdex.null:
                    missing_dataset[station][year]['year'] += 1
                    missing_dataset[station][year][month] += 1

        print(missing_dataset)        


    def check_baseline(self, base_1=None, base_2=None):
        """Checks data availability in a given baseline for all stations in current project"""

        if base_1 is None:
            base_1, base_2 = self.baseline
        elif base_1 is not None and base_2 is None:
            base_2 = self.baseline[1]

        print(base_1, base_2)

        # TODO: completely


    def qc(self, plot=False, download=True, verbose=True):
        """Conducts simple QC on datasets in current project"""

        if not self._project_dir_exists():
            return

        # TODO: Check plot, download, verbose are all boolean

        if download:
            if not self._check_download():
                self.download()

        if self._operating:
            id_filename = os.path.join(Config.instance().climex_dir, 'GEOJSON', 'conagua_operating_by_id.json')
        else:
            id_filename = os.path.join(Config.instance().climex_dir, 'GEOJSON', 'conagua_all_by_id.json')

        try:
            with open(id_filename, 'rt') as id_file:
                id_json = json.load(id_file)
        except:
            base.geojson()

        try:
            with open(id_filename, 'rt') as id_file:
                id_json = json.load(id_file)
        except:
            return

        edits_filename = os.path.join(self._project_dir, 'edits.json')

        try:
            with open(edits_filename, 'rt') as edits_file:
                edits = json.load(edits_file)
        except:
            edits = {}

        for station in self.stations:

            if verbose:
                print(f'Running QC on station "{station}"', end='')

            try:
                station_feature = id_json[station]
            except:
                print(': station not found [FAILED]')
                continue

            #print(station_feature)

            station_name = f"{station_feature['properties']['Nombre']}, {station_feature['properties']['Estado']}"

            climdex_filename = os.path.join(self._project_dir, 'CLIMDEX', f'{station}.txt')

#            if not os.path.isfile(climdex_filename):
#                """
#                try:
#                    raise Exception()
#                except BaseException:
#                    print('\t[FAILED]')
#                    print(f'climex.Project.qc(): data file for station {station} not found. Run climex.Project.download()')
#                    return
#                """


#                print('\t[FAILED]')
#                print(f'climex.Project.qc(): data file for station {station} not found. Run climex.Project.download()')
#                kkk
#            """


            """
            try:
                with open(climdex_filename, 'rt') as climdex_file:
                    climdex_contents = climdex_file.readlines()
            except:
                print(f'climex.Project.qc(): data file for station {station} not found. Run climex.Project.download()')
                return
                #sys.exit()
            """

            if not os.path.isfile(climdex_filename):
                if verbose:
                    print('\t[FAILED]')
                print(f'climex.Project.qc(): data file for station {station} not found. Run climex.Project.download()')
                continue
            #    self.qc()

            with open(climdex_filename, 'rt') as climdex_file:
                climdex_contents = climdex_file.readlines()

            climdex_dataset = []
            for record in climdex_contents:
                fields = record.split()

                year = int(fields[0])
                month = int(fields[1])
                day = int(fields[2])
                prcp = float(fields[3])
                tmax = float(fields[4])
                tmin = float(fields[5])

                try:
                    if station in edits['null'].keys():
                        try:
                            if  f'{year:04d}-{month:02d}-{day:02d}' in edits['null'][str(station)]['prcp']:
                                prcp = klimdex.null
                        except:
                            pass
                        try:
                            if  f'{year:04d}-{month:02d}-{day:02d}' in edits['null'][str(station)]['tmax']:
                                tmax = klimdex.null
                        except:
                            pass
                        try:
                            if  f'{year:04d}-{month:02d}-{day:02d}' in edits['null'][str(station)]['tmin']:
                                tmin = klimdex.null
                        except:
                            pass
                except:
                    pass

                try:
                    if station in edits['zero'].keys():
                        pass
                except:
                    pass

                try:
                    if station in edits['value'].keys():
                        pass
                except:
                    pass

                climdex_dataset.append([year, month, day, prcp, tmax, tmin])

            qc0_report, climdex_qc_dataset = qc.qc0(station, climdex_dataset, self.baseline)

            #
            #
            # More QCs here, if necessary !!!
            #
            #

            base_1, base_2 = self.baseline
            climdex_qc_filename = os.path.join(self._project_dir, 'CLIMDEX', f'{station}_{base_1}_{base_2}.txt')

            climdex_qc_data = ''
            for record in climdex_qc_dataset:
                year, month, day, prcp, tmax, tmin = record
                climdex_qc_record = f'{year:04d} {month:02d} {day:02d} {prcp:6.1f} {tmax:6.1f} {tmin:6.1f}\n'
                climdex_qc_data += climdex_qc_record

            with open(climdex_qc_filename, 'wt') as climdex_qc_file:
                climdex_qc_file.write(climdex_qc_data)


            qc0_report_filename = os.path.join(self._project_dir, 'QC', f'{station}_{base_1}_{base_2}_qc0.json')
            with open(qc0_report_filename, 'wt') as qc0_report_file:
                json.dump(qc0_report, qc0_report_file, indent=4)

            if plot:
                qc.missing_data_plot(station, station_name, self._project_dir, climdex_qc_dataset, self.baseline)

            if verbose:
                print('\t[OK]')

            #break

    def value(self, station, date):
        """Given station and date, returns the corresponding values of PRCP, TMAX and TMIN"""

        # TODO: completely

    def max_value(self, station):
        """Given a station, returns the maximum values of PRCP, TMAX and TMIN, together with their corresponding dates"""

        if str(station) not in self.stations:
            return

        base_1, base_2 = self.baseline

        climdex_qc_filename = os.path.join(self._project_dir, 'CLIMDEX', f'{station}_{base_1}_{base_2}.txt')

        try:
            with open(climdex_qc_filename, 'rt') as climdex_qc_file:
                climdex_qc_contents = climdex_qc_file.readlines()
        except:
            print(f'climex.Project.max_value(): QC data file for station {station} not found. Run climex.Project.qc()')
            return

        fields = climdex_qc_contents[0].split()

        year_prcp_max = int(fields[0])
        month_prcp_max = int(fields[1])
        day_prcp_max = int(fields[2])

        year_tmax_max = int(fields[0])
        month_tmax_max = int(fields[1])
        day_tmax_max = int(fields[2])

        year_tmin_max = int(fields[0])
        month_tmin_max = int(fields[1])
        day_tmin_max = int(fields[2])

        prcp_max = float(fields[3])
        tmax_max = float(fields[4])
        tmin_max = float(fields[5])

        for record in climdex_qc_contents:
            fields = record.split()

            year = int(fields[0])
            month = int(fields[1])
            day = int(fields[2])
            prcp = float(fields[3])
            tmax = float(fields[4])
            tmin = float(fields[5])

            if prcp > prcp_max:
                prcp_max = prcp

                year_prcp_max = year
                month_prcp_max = month
                day_prcp_max = day

            if tmax > tmax_max:
                tmax_max = tmax

                year_tmax_max = year
                month_tmax_max = month
                day_tmax_max = day

            if tmin > tmin_max:
                tmin_max = tmin

                year_tmin_max = year
                month_tmin_max = month
                day_tmin_max = day

        max_values = {
            'prcp': [prcp_max, f'{year_prcp_max:04d}-{month_prcp_max:02d}-{day_prcp_max:02d}'],
            'tmax': [tmax_max, f'{year_tmax_max:04d}-{month_tmax_max:02d}-{day_tmax_max:02d}'],
            'tmin': [tmin_max, f'{year_tmin_max:04d}-{month_tmin_max:02d}-{day_tmin_max:02d}']
        }

        return max_values


    def null(self, station, variable, date):
        """Given station, variable, and date, sets the value to NULL"""

        if str(station) not in self.stations:
            return

        if variable.upper() not in ('PRCP', 'TMAX', 'TMIN'):
            print(f'climex.Project.max_null(): variable name must be either "prcp", "tmax, or "tmin"')
            return

        base_1, base_2 = self.baseline

        climdex_qc_filename = os.path.join(self._project_dir, 'CLIMDEX', f'{station}_{base_1}_{base_2}.txt')

        try:
            with open(climdex_qc_filename, 'rt') as climdex_qc_file:
                climdex_qc_contents = climdex_qc_file.readlines()
        except:
            print(f'climex.Project.max_null(): QC data file for station {station} not found. Run climex.Project.qc()')
            return

        try:
            null_year, null_month, null_day = map(int, date.split('-'))
        except:
            print('Project.null(): bad date format')
            return

        climdex_qc_dataset = []
        updated = False
        current_edit = {}
        for record in climdex_qc_contents:
            fields = record.split()

            year = int(fields[0])
            month = int(fields[1])
            day = int(fields[2])
            prcp = float(fields[3])
            tmax = float(fields[4])
            tmin = float(fields[5])

            if null_year == year and null_month == month and null_day == day:
                if variable.upper() == 'PRCP':
                    climdex_qc_dataset.append([year, month, day, klimdex.null, tmax, tmin])
                    current_edit = {date: prcp}
                elif variable.upper() == 'TMAX':
                    climdex_qc_dataset.append([year, month, day, prcp, klimdex.null, tmin])
                    current_edit = {date: tmax}
                elif variable.upper() == 'TMIN':
                    climdex_qc_dataset.append([year, month, day, prcp, tmax, klimdex.null])
                    current_edit = {date: tmin}

                updated = True
            else:
                climdex_qc_dataset.append([year, month, day, prcp, tmax, tmin])
        
        if updated:
            print(current_edit)

            climdex_qc_data = ''
            for record in climdex_qc_dataset:
                year, month, day, prcp, tmax, tmin = record
                climdex_qc_record = f'{year:04d} {month:02d} {day:02d} {prcp:6.1f} {tmax:6.1f} {tmin:6.1f}\n'
                climdex_qc_data += climdex_qc_record

            with open(climdex_qc_filename, 'wt') as climdex_qc_file:
                climdex_qc_file.write(climdex_qc_data)

            edits_filename = os.path.join(self._project_dir, 'edits.json')

            try:
                with open(edits_filename, 'rt') as edits_file:
                    edits = json.load(edits_file)
            except:
                edits = {'null': {}}

            print()
            print(json.dumps(current_edit, indent=4))

            if str(station) not in edits['null'].keys():
                edits['null'][str(station)] = {}
            if variable.lower() not in edits['null'][str(station)].keys():
                edits['null'][str(station)][variable.lower()] = {}

            edits['null'][str(station)][variable.lower()][date] = current_edit[date]
            print(json.dumps(edits, indent=4))

            try:
                with open(edits_filename, 'wt') as edits_file:
                    edits = json.dump(edits, edits_file, indent=4)
            except:
                return  

            self.save()


           
            """
            try:
                edits['null'][variable.lower()][str(station)].append(date)
            except:
                edits['null'][variable.lower()][str(station)] = [date]

            try:
                with open(edits_filename, 'wt') as edits_file:
                    edits = json.dump(edits, edits_file, indent=4)
            except:
                return  

            self.save()
            """


    def restore(self):
        """Restores all edits available at edits.json file"""

        # TODO: is this necessary ?


    def sample(self, station, rand=False):
        """Prints a sample of the dataset"""

        dataset = self._get_dataset(station)

        n = len(dataset)

        if rand:
            records = random.sample(list(range(n)), 10)
        else:
            records = list(range(10))

        for record in records:
            year, month, day, prcp, tmax, tmin = dataset[record]
            climdex_record = f'{year:4d} {month:02d} {day:02d} {prcp:6.1f} {tmax:6.1f} {tmin:6.1f}'
            print(climdex_record)


    def show(self, station, plot='prcp'):
        """Shows a plot on the screen"""
        
        if plot.upper() not in ('PRCP', 'TEMP') and plot.upper() not in klimdex.climdex_list:
            return

        base_1, base_2 = self.baseline

        if plot.upper() in klimdex.climdex_list:
            index_number = klimdex.climdex_list.index(plot.upper()) + 1
            image_name = os.path.join(
                self._project_dir, 'INDEX',
                f'{str(station)}_{base_1:04d}_{base_2:04d}_{index_number:02d}_{plot.upper()}.png'
            )
            if not os.path.isfile(image_name):
                print(f'climex.Project.show(): {plot.upper()} index plot file not found')
                return
        elif plot.upper() == 'PRCP':
            image_name = os.path.join(self._project_dir, 'QC', f'{station}_{base_1}_{base_2}_qc_prcp.png')
            if not os.path.isfile(image_name):
                print(f'climex.Project.show(): {plot.upper()} plot file not found')
                return
        elif plot.upper() == 'TEMP':
            image_name = os.path.join(self._project_dir, 'QC', f'{station}_{base_1}_{base_2}_qc_temp.png')
            if not os.path.isfile(image_name):
                print(f'climex.Project.show(): {plot.upper()} plot file not found')
                return
        else:
            pass #TODO: check RNNMM

        plt.rcParams['figure.dpi'] = 300
        image = plt.imread(image_name)

        fig, ax = plt.subplots()
        im = ax.imshow(image)

        ax.axis('off')
        plt.show()


    def compute_normal(self):
        """Computes climate normals according to WMO publication xxxxxxxx"""

        #for station in self.stations:
        #     1. Get qc dataset ~ nested list with the data
        #     2. Call klimdex.normal_batch(station, dataset, baseline)


    def compute_index(self, index_list=None, plot=False):
        """Computes climate change indices according to https://www.climdex.org/learn/indices/"""

        if not self._check_qc():
            self.qc()

        index = klimdex.Index(self, index_list, plot)
        index.index_batch()


        """
        if index_list is None:
            index_list = klimdex.indexes

        if not isinstance(index_list, list):
            list_index = [index_list]

        if self._operating:
            id_filename = os.path.join(Config.instance().climex_dir, 'GEOJSON', 'conagua_operating_by_id.json')
        else:
            id_filename = os.path.join(Config.instance().climex_dir, 'GEOJSON', 'conagua_all_by_id.json')

        try:
            with open(id_filename, 'rt') as id_file:
                id_json = json.load(id_file)
        except:
            base.geojson()

        try:
            with open(id_filename, 'rt') as id_file:
                id_json = json.load(id_file)
        except:
            return

        base_1, base_2 = self.baseline

        for station in self.stations:

            try:
                station_feature = id_json[station]
            except:
                print(f'climex.compute_index(): station {station} not found')
                continue

            #print(station_feature)

            station_name = f"{station_feature['properties']['Nombre']}, {station_feature['properties']['Estado']}"

            climdex_filename = os.path.join(self._project_dir, 'CLIMDEX', f'{station}_{base_1}_{base_2}.txt')

            try:
                with open(climdex_filename, 'rt') as climdex_file:
                    climdex_contents = climdex_file.readlines()
            except:
                print(f'climex.Project.qc(): data file for station {station} not found. Run climex.Project.download() and/or climex.Project.qc()')
                return

            climdex_dataset = []
            for record in climdex_contents:
                fields = record.split()

                year = int(fields[0])
                month = int(fields[1])
                day = int(fields[2])
                prcp = float(fields[3])
                tmax = float(fields[4])
                tmin = float(fields[5])

                climdex_dataset.append([year, month, day, prcp, tmax, tmin])

            #print(climdex_filename)

            #for index in index_list:
            #    print(f'Computing {} index on station "{station}"', end='')
            climdex.index_batch(index_list, station, climdex_dataset, self.baseline, self._project_dir)

        
        #for station in self.stations:
        #     1. Get qc dataset ~ nested list with the data
        #         If not found, message to run QC
        #     2. Call climdex.index_batch(index_list, station, dataset, self.baseline)
        pass
        """


    def geojson(self, verbose=True):
        """Creates several GeoJSON datasets from current project"""

        if self._operating:
            id_filename = os.path.join(Config.instance().climex_dir, 'GEOJSON', 'conagua_operating_by_id.json')
        else:
            id_filename = os.path.join(Config.instance().climex_dir, 'GEOJSON', 'conagua_all_by_id.json')

        id_json = {}

        try:
            with open(id_filename, 'rt') as id_file:
                id_json = json.load(id_file)
        except:
            base.geojson()

        if not id_json:
            try:
                with open(id_filename, 'rt') as id_file:
                    id_json = json.load(id_file)
            except:
                return

        """
        if attributes:

            base_1, base_2 = self.baseline

            attributes = {}

            index_dir_contents = glob.glob(os.path.join(self._project_dir, 'INDEX', '*'))

            for index_filename in index_dir_contents:
                print(index_filename)
                with open(index_filename, 'rt') as index_file:
                    index_data = json.load(index_file)

                if index_data['station'] not in attributes.keys():
                    attributes[index_data['station']] = {}

                if index_data['index'] not in attributes[index_data['station']].keys():
                    attributes[index_data['station']][index_data['index']] = {}

                for key, value in index_data.items():
                    if key in ('station', 'index', 'baseline'):
                        continue

                    attributes[index_data['station']][index_data['index']][key] = value['value']
        """


        features = []
        for station in self.stations:
            try:
                station_feature = id_json[station]
            except:
                continue

            """
            if attributes:
                try:                    
                    station_index_data = attributes[station]
                    #print(station_index_data)
                    
                    for index_name, index_data in station_index_data.items():
                        #print(index_name)
                        #print(index_data)
                        for year, value in index_data.items():
                            attribute_name = f'{index_name}_{year}'
                            #print(attribute_name, value)
                            station_feature['properties'][attribute_name] = value 
                        
                except:
                    pass
            """

            features.append(station_feature)

            #break

        project_geojson = {'type': 'FeatureCollection', 'features': features}

        project_geojson_filename = os.path.join(self._project_dir, 'GEOJSON', f'{self._name}.geojson')

        try:
            with open(project_geojson_filename, 'wt') as project_geojson_file:
                json.dump(project_geojson, project_geojson_file, indent=4)
        except:
            print(f'climex.Project.geojson(): GeoJSON file cannot be created')
            return


        #print(json.dumps(attributes, indent=4))

        attributes = {}
        for index in klimdex.climdex_list:
            attributes[index] = {}

        index_dir_contents = glob.glob(os.path.join(self._project_dir, 'INDEX', '*'))

        for index_filename in index_dir_contents:

            try:
                with open(index_filename, 'rt', encoding='utf-8') as index_file:
                    index_data = json.load(index_file)

                index = index_data['index']
                station = index_data['station']
                baseline = index_data['baseline']
            except:
                continue

            #print(index_filename)

            del index_data['index']
            del index_data['station']
            del index_data['name']
            del index_data['baseline']
            del index_data['description']
            del index_data['units']

            if station not in attributes[index]:
                attributes[index][station] = {}

            for key, value in index_data.items():
                attributes[index][station][key] = value['value']

            #print(index_data.keys())

        #print(attributes)

        for index, data in attributes.items():
            if len(data) == 0:
                continue

            index_number = klimdex.climdex_list.index(index.upper()) + 1

            index_geojson_filename = os.path.join(self._project_dir, 'GEOJSON', f'{self._name}_{index_number:02d}_{index}.geojson')
            
            index_geojson = {'type': 'FeatureCollection', 'features': []}

            #print(geojson_index_filename)

            for feature in project_geojson['features']:
                index_geojson['features'].append(feature)

            for feature in index_geojson['features']:
                #print(feature['id'])

                for key, value in attributes[index][feature['id']].items():
                    feature['properties'][key] = value
            try:
                with open(index_geojson_filename, 'wt') as index_geojson_file:
                    json.dump(index_geojson, index_geojson_file, indent=4)
            except:
                print(f'climex.Project.geojson(): file {self._name}_{index}.geojson cannot be created')

            #break

        project_geojson_dir = os.path.join(self._project_dir, 'GEOJSON')

        if verbose:
            print(f'climex.Project.geojson(): GeoJSON files available at {project_geojson_dir}')

        return # json.dumps(project_geojson)


    def shapefile(self, attributes=False):
        """Creates several Shapefile datasets from current project"""

        if 'shapefile' not in sys.modules.keys():
            print('climex.Project.osm(): Package "shapefile" not found (pip install pyshp)')
            return
        
        shp_filename = os.path.join(self._project_dir, 'SHAPEFILE', f'{self._name}.shp')

        shp_writer = shapefile.Writer(shp_filename, shapefile.POINT)

        shp_writer.field('EID', 'C', 10)
        shp_writer.field('Nombre', 'C', 20)
        shp_writer.field('Municipio', 'C', 20)
        shp_writer.field('Estado', 'C', 20)
        shp_writer.field('Organismo', 'C', 20)
        shp_writer.field('Cuenca', 'C', 20)
        shp_writer.field('Elevation', 'N', 20, 16)
        shp_writer.field('URL', 'C', 60)

        stations_by_id = {}
        for station in self._stations:

            station_data = Station.instance()._station(str(station))

            if not station_data:
                continue

            stations_by_id[str(station)] = station_data['geometry']['coordinates']

            longitude, latitude, elevation = station_data['geometry']['coordinates']

            record = (
                str(station),
                station_data['properties']['Nombre'],
                station_data['properties']['Municipio'],
                station_data['properties']['Estado'],
                station_data['properties']['Organismo'],
                station_data['properties']['Cuenca'],
                elevation,
                station_data['properties']['URL']
            )

            shp_writer.point(longitude, latitude)
            shp_writer.record(*record)

        shp_writer.close()

        prj_filename = os.path.join(self._project_dir, 'SHAPEFILE', f'{self._name}.prj')

        prj_wkt = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.01745329251994328,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]]'

        try:
            with open(prj_filename, 'wt') as prj_file:
                prj_file.write(prj_wkt)
        except:
            pass

        index_dir_contents = glob.glob(os.path.join(self._project_dir, 'INDEX', '*.json'))
        attributes = {}
        for index_filename in index_dir_contents:
            index_fields = os.path.basename(index_filename).split('.')[0].split('_')

            if index_fields[0] not in self.stations or len(index_fields) != 5:
                continue

            try:
                with open(index_filename, 'rt') as index_file:
                    index_data = json.load(index_file)
            except:
                pass

            #print(index_data['index'])
            current_index = index_data['index']
            if current_index not in attributes.keys():
                attributes[current_index] = {}

            current_station = index_data['station']
            if current_station not in attributes[current_index].keys():
                attributes[current_index][current_station] = {}

            base_1, base_2 = index_data['baseline']

            del index_data['station']
            del index_data['name']
            del index_data['index']
            del index_data['description']
            del index_data['baseline']
            del index_data['units']
            
#            print(index_data['1961']['value'], type(index_data['1961']['value']))

            for year, data in index_data.items():
                if math.isnan(data['value']):
                    attributes[current_index][current_station][year] = None
                else:
                    attributes[current_index][current_station][year] = data['value']

                

            #break


        base_1, base_2 = self.baseline

        for index in attributes.keys():

            shp_filename = os.path.join(self._project_dir, 'SHAPEFILE', f'{self._name}_{index}_{base_1}_{base_2}.shp')
            #print(shp_filename)

            shp_writer = shapefile.Writer(shp_filename, shapefile.POINT)

            shp_writer.field('EID', 'C', 10)
            shp_writer.field('Elevation', 'N', 10, 3)
            #for year, value in attributes[index][station].items():
            for year in range(base_1, base_2 + 1):
                #print(f'{index}_{year}')
                shp_writer.field(f'{index}_{year}', 'N', 10, 2)

            for station in attributes[index].keys():
                #print(index, station)

                longitude, latitude, elevation = stations_by_id[str(station)]

                #print(attributes[index][station])
                record = [station, elevation]
                #shp_writer.field('EID', 'C', 10)
                #shp_writer.field('Elevation', 'N', 10, 3)
                for year, value in attributes[index][station].items():
                    #print(f'{index}_{year}')
                    #shp_writer.field(f'{index}_{year}', 'N', 10, 2)
                    record.append(value)

                shp_writer.point(longitude, latitude)
                #print(record)
                shp_writer.record(*record)

                #break

            shp_writer.close()

            prj_filename = os.path.join(self._project_dir, 'SHAPEFILE', f'{self._name}_{index}_{base_1}_{base_2}.prj')

            prj_wkt = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.01745329251994328,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]]'

            try:
                with open(prj_filename, 'wt') as prj_file:
                    prj_file.write(prj_wkt)
            except:
                pass

            #break

        project_shp_dir = os.path.join(self._project_dir, 'SHAPEFILE')

        print(f'climex.Project.shapefile(): Shapefiles available at {project_shp_dir}')


    def osm(self, browser=True, climate_index=None, missing=False):
        """Shows stations in current project on OSM base map using default web browser"""

        if browser and 'folium' not in sys.modules.keys():
            print('climex.Project.osm(): Package "folium" not found (pip install folium)')
            return

        if climate_index is None:
            geojson_filename = os.path.join(self._project_dir, 'GEOJSON', f'{self._name}.geojson')
            html_filename = os.path.join(self._project_dir, 'MAP', f'{self._name}.html')
        else:
            try:
                index_number = klimdex.climdex_list.index(climate_index.upper()) + 1
            except:
                print(f'climex.Project.osm(): wrong index name "{climate_index.upper()}"')
                return
                
            geojson_filename = os.path.join(
                self._project_dir, 'GEOJSON', f'{self._name}_{index_number:02d}_{climate_index.upper()}.geojson'
            )
            html_filename = os.path.join(
                self._project_dir, 'MAP', f'{self._name}_{index_number:02d}_{climate_index.upper()}.html'
            )

        base_1, base_2 = self.baseline
        
        if not os.path.isfile(geojson_filename):
            self.geojson(verbose=False)
        
        try:
            with open(geojson_filename, 'rt', encoding='utf-8') as geojson_file:
                geojson_data = json.load(geojson_file)
        except:
            print(f'climex.Project.osm(): index {climate_index.upper()} not yet computed')
            return

        html_layer = folium.FeatureGroup(name='OSM')

        for entity in geojson_data['features']:
        
            pretty_popup = base.html_popup(entity)

            marker_colour = 'blue'

            if missing and climate_index is not None:
                """discuss colour here (green=no missing, orange=5 missing, red= more than 5  missind"""

                number_of_missing_data = 0
                for value in entity['properties'].values():
                    try:
                        if math.isnan(value):
                            number_of_missing_data += 1
                    except:
                        continue
                
                if number_of_missing_data == 0:
                    marker_colour = 'blue'
                elif number_of_missing_data < 5:
                    marker_colour = 'green'
                elif number_of_missing_data < 10:
                    marker_colour = 'orange'
                elif number_of_missing_data == base_2 - base_1 + 1:
                    marker_colour = 'black'
                else:
                    marker_colour = 'red'
                    
            html_layer.add_child(
                folium.CircleMarker(
                    location = entity['geometry']['coordinates'][:2][::-1],
                    popup = folium.Popup(pretty_popup, max_width=500),
                    radius = 6,
                    color = marker_colour,
                    fill = True,
                    fill_color = marker_colour,
                    fill_opacity = 0.3
                )
            )
        
        html_map = folium.Map()
        html_map.add_child(html_layer)
        html_map.fit_bounds(html_layer.get_bounds())

        if browser:
            html_map.save(html_filename)
            
            webbrowser.open(
                os.path.abspath(html_filename)
            )
        else:
            return html_map


    def prcp_plot(self, station, years):
        """Creates a PRCP plot of the period given by parameter \"years\""""

        if isinstance(years, int):
            span_1 = years
            span_2 = years + 1
        elif isinstance(years, list):
            if len(years) == 1 and isinstance(years[0], int):
                span_1 = years[0]
                span_2 = years[0]
            elif len(years) == 2 and isinstance(years[0], int) and isinstance(years[1], int):
                span_1, span_2 = years
            else:
                return
        else:
            return

        #if not isinstance(span_1, int) or not isinstance(span_2, int):
        #    print('climex.Project.prcp_plot(): Please, use integers to define the span')
        #    return

        base_1, base_2 = self.baseline

        if span_1 < base_1 or span_1 > base_2 or span_2 < base_1 or span_2 > base_2:
            print(f'climex.Project.prcp_plot(): Please, provide a span within baseline limits {self.baseline}')
            return

        if str(station) not in self.stations:
            print(f'climex.Project.prcp_plot(): wrong station name ({station})')
            return

        dataset = self._get_dataset(station)

        span = tuple(range(span_1, span_2 + 1))

        x_data = []
        y_data = []
        minor_ticks = []
        major_ticks = []
        major_labels = []
        
        number_of_record = 0
        for record in dataset:
            year, month, day, prcp, tmax, tmin = record

            if year not in span:
                continue



    def temp_plot(self, years=None):
        """Creates a TEMP plot of the period given by parameter \"years\""""
        pass

    def temp_percentile_plot(self):
        pass
        #plot.temp_percentile_plot(self)

    def in_out_plot(self):
        pass
        #plot.in_out_plot(self)

    def temp_extreme_plot(self):
        pass
        #plot.temp_extreme_plot(self)

    def clicom_folder(self):
        """Allows setting the folder the contains the CLICOM files"""

        if 'easygui' not in sys.modules.keys():
            print('climex.Project.clicom_folder(): Package "easygui" not found (pip install easygui)')
            return

        folder = easygui.diropenbox()
    
        if folder is not None:
            self._clicom_dir = folder

    def _read_clicom(self, filename, fileformat):

        if fileformat.upper() == 'XLS':
            clicom_workbook = xlrd.open_workbook(filename)

            dataset = {
                'status': True,
                'station': None,
                'data': {}
            }

            for sheet in clicom_workbook.sheets():
                if 'CLICOM' in sheet.name.upper():
                    #print(sheet.name)
                    header = sheet.row_values(0, start_colx=0, end_colx=None)
                    #print(header)

                    # Find indices of key fields: STATION-ID, ELEMENT-CODE, YEAR-MONTH
                    # TODO

                    number_of_rows = sheet.nrows

                    for row_number in range(1, number_of_rows):
                        row = sheet.row_values(row_number, start_colx=0, end_colx=None)

                        station_id = row[1].lstrip('0')

                        if dataset['station'] is None:
                            dataset['station'] = station_id
                        elif dataset['station'] != station_id:
                            dataset['status'] = False
                            

                        element_code = row[2]

                        if element_code == '002': # tmax
                            year_month = row[4]
                            for column in range(5, len(row), 2):
                                day = (column // 2) - 1
                                value = float(row[column])
                                flag = row[column + 1].strip()

                                date = f'{year_month:s}-{day:02d}'
                                #print(date, value, flag)
                                try:
                                    dataset['data'][date]['tmax'] = [value, flag]
                                except:
                                    dataset['data'][date] = {'prcp': [], 'tmax': [], 'tmin': []}
                                    dataset['data'][date]['tmax'] = [value, flag]

                        elif element_code == '003': # tmin
                            year_month = row[4]
                            for column in range(5, len(row), 2):
                                day = (column // 2) - 1
                                value = float(row[column])
                                flag = row[column + 1].strip()

                                date = f'{year_month:s}-{day:02d}'
                                #print(date, value, flag)
                                try:
                                    dataset['data'][date]['tmin'] = [value, flag]
                                except:
                                    dataset['data'][date] = {'prcp': [], 'tmax': [], 'tmin': []}
                                    dataset['data'][date]['tmin'] = [value, flag]

                        elif element_code == '005': # prcp
                            year_month = row[4]
                            for column in range(5, len(row), 2):
                                day = (column // 2) - 1
                                value = float(row[column])
                                flag = row[column + 1].strip()

                                date = f'{year_month:s}-{day:02d}'
                                #print(date, value, flag)
                                try:
                                    dataset['data'][date]['prcp'] = [value, flag]
                                except:
                                    dataset['data'][date] = {'prcp': [], 'tmax': [], 'tmin': []}
                                    dataset['data'][date]['prcp'] = [value, flag]

        elif fileformat.upper() == 'XLSX':
            # TODO: process XLSX formaat
            pass



        return dataset


    def clicom(self, fileformat='xls'):
        """Converts CLICOM data files to Climdex format"""

        if fileformat.upper() not in ('XLSX', 'XLS', 'CSV'):
            return

        if fileformat.upper() == 'XLSX':
            clicom_dir_contents = glob.glob(os.path.join(self._clicom_dir, '*.xlsx'))
        elif fileformat.upper() == 'XLS':
            clicom_dir_contents = glob.glob(os.path.join(self._clicom_dir, '*.xls'))
        elif fileformat.upper() == 'CSV':
            clicom_dir_contents = glob.glob(os.path.join(self._clicom_dir, '*.csv'))

        if len(clicom_dir_contents) == 0:
            print(self._clicom_dir)
            print(f'climex.Project.clicom(): {fileformat.upper()} data files not found')
            return

        if fileformat.upper() == 'XLSX':
            if 'openpyxl' not in sys.modules.keys():
                print('climex.Project.clicom(): Package "openpyxl" not found (pip install openpyxl)')
                return
        elif fileformat.upper() == 'XLS':
            if 'xlrd' not in sys.modules.keys():
                print('climex.Project.clicom(): Package "xlrd" not found (pip install xlrd)')
                return

        for clicom_filename in clicom_dir_contents:
            clicom_data = self._read_clicom(clicom_filename, fileformat.upper())

            if not clicom_data['status']:
                continue

            period = []
            for date in clicom_data['data'].keys():
                year = int(date.split('-')[0])
                if year not in period:
                    period.append(year)

            base_1 = min(period)
            base_2 = max(period)

            if (base_2 - base_1 + 1) < self.minimum_baseline_length:
                print(f'climex.Project.clicom(): CLICOM baseline shorter than current baseline length for station {clicom_data["station"]}')
                continue

            self.baseline = [base_1, base_2]
            self.stations = clicom_data['station']

            period_dates = []
            for year in range(base_1, base_2 + 1):
                days_per_month = base.days_per_month.copy()
                days_per_month[2] += base.leap_year(year)

                for month in sorted(days_per_month.keys()):
                    for day in range(1, days_per_month[month] + 1):
                        period_dates.append(f'{year:4d}-{month:02d}-{day:02d}')

            climdex_filename = os.path.join(Config.instance().climex_dir, 'PROJECTS', self._name.upper(), 'CLIMDEX', f"{clicom_data['station']}.txt")

            #print(climdex_filename)

            with open(climdex_filename, 'wt') as climdex_file:
                for date in sorted(clicom_data['data'].keys()):
                    observation = clicom_data['data'][date]
                    climdex_date = date.replace('-', ' ')
                    #print(date, bool(date in period_dates))
                    year, month, day = climdex_date.split()

                    prcp_value = observation['prcp'][0]
                    tmax_value = observation['tmax'][0]
                    tmin_value = observation['tmin'][0]
                    #print(observation)

                    if prcp_value <= -99.0:
                        prcp_value = klimdex.null

                    if tmax_value <= -99.0:
                        tmax_value = klimdex.null

                    if tmin_value <= -99.0:
                        tmin_value = klimdex.null


                    if date not in period_dates:
                        continue

                    climdex_record = f'{climdex_date} {prcp_value:6.1f} {tmax_value:6.1f} {tmin_value:6.1f}\n'
                    climdex_file.write(climdex_record)



            print(f"climex.Project.clicom(): datafile created for station {clicom_data['station']}")
            #break


    def bounds(self, elevation=False):
        """Prints the bounding box of the stations in current project in order lon_min, lat_min, lon_max, lat_max"""
        
        geojson_filename = os.path.join(self._project_dir, 'GEOJSON', f'{self._name}.geojson')

        if not os.path.isfile(geojson_filename):
            self.geojson(verbose=False)
        
        try:
            with open(geojson_filename, 'rt', encoding='utf-8') as geojson_file:
                geojson_data = json.load(geojson_file)
        except:
            return

        longitude_max, latitude_max, height_max = geojson_data['features'][0]['geometry']['coordinates']
        longitude_min, latitude_min, height_min = geojson_data['features'][0]['geometry']['coordinates']
        
        for station in geojson_data['features']:
            longitude, latitude, height = station['geometry']['coordinates']

            if longitude > longitude_max:
                longitude_max = longitude
            elif longitude < longitude_min:
                longitude_min = longitude
            
            if latitude > latitude_max:
                latitude_max = latitude
            elif latitude < latitude_min:
                latitude_min = latitude

            if height > height_max:
                height_max = height
            elif height < height_min:
                height_min = height


        bounding_box = [longitude_min, latitude_min, longitude_max, latitude_max]

        if elevation:
            bounding_box.insert(2, height_min)
            bounding_box.append(height_max)

        return bounding_box


    def _export_to_csv(self, output_filename, station_by_id, index_data, attribute_data={}, separator=','):
        """Exports data to CSV format with a record per station/year"""
        
        csv_header = ['station', 'year', 'longitude', 'latitude', 'elevation']
        if len(index_data) > 0:
            for index in index_data['indices']:
                csv_header.append(index)
        if len(attribute_data) > 0:
            for attribute in attribute_data['attributes']:
                csv_header.append(attribute)

        csv_dataset = [csv_header]
        for station, records in index_data['data'].items():
            longitude, latitude, elevation = station_by_id[station]['geometry']['coordinates']
            for year, record in records.items():
                csv_record = [station, year, longitude, latitude, elevation]

                if len(index_data) > 0:
                    for index in index_data['indices']:
                        index_value = index_data['data'][station][year][index]
                        if math.isnan(index_value):
                            csv_record.append('NA')
                        else:
                            csv_record.append(index_value)
                if len(attribute_data) > 0:
                    for attribute in attribute_data['attributes']:
                        try:
                            csv_record.append(attribute_data['data'][station][year][attribute])
                        except:
                            csv_record.append('NA')
                csv_dataset.append(csv_record)

##                        print(station, year, longitude, latitude, elevation, index_data['data'][station][year][index])

        with open(output_filename, 'wt') as output_file:
            for record in csv_dataset:
                output_file.write(
                    str(record).replace('\'', '').replace('[', '').replace(']', '').replace(',', separator) + '\n'
                )

    
    def _export_to_json(self):
        pass

    
    def _export_to_geojson(self):
        pass


    def _export_to_shapefile(self):
        pass

    
    def export(self, data_format='csv', separator=',', filename=None):
        """Exports all computed indices and attributes to CSV, JSON, GEOJSON or SHAPEFILE format"""

        if data_format.upper() not in ['CSV', 'JSON', 'GEOJSON', 'SHP', 'SHAPEFILE']:
            return

        station_by_id_filename = os.path.join(
            Config.instance().climex_dir, 'GEOJSON', 'conagua_all_by_id.json'
        )

        try:
            with open(station_by_id_filename, 'rt') as station_by_id_file:
                station_by_id = json.load(station_by_id_file)
        except:
            base.geojson()

        try:
            with open(station_by_id_filename, 'rt') as station_by_id_file:
                station_by_id = json.load(station_by_id_file)
        except:
            print('Project.export(): CONAGUA database not available')
            return

        if filename is None:

            if 'easygui' not in sys.modules.keys():
                print('climex.Project.export(): Package "easygui" not found (pip install easygui)')
                return

            if data_format.upper() == 'CSV':
                file_extensions = ['*.csv']
                default_extension = '*.csv'
            elif data_format.upper() == 'JSON':
                file_extensions = ['*.json']
                default_extension = '*.json'
            elif data_format.upper() == 'GEOJSON':
                file_extensions = ['*.geojson']
                default_extension = '*.geojson'
            elif data_format.upper() == 'SHAPEFILE' or data_format.upper() == 'SHP':
                file_extensions = ['*.shp']
                default_extension = '*.shp'
            else:
                return
                
            filename = easygui.filesavebox(
                msg='Save CLIMEX dataset as', default=default_extension,
                filetypes=file_extensions
            )
        
        if filename is None:
            return
        
        index_data = {'indices': [], 'data': {}}
        
        index_dir_contents = sorted(
            glob.glob(os.path.join(self._project_dir, 'INDEX', '*.json'))
        )

        for json_filename in index_dir_contents:
            with open(json_filename, 'rt') as json_file:

                json_data = json.load(json_file)

            if json_data['index'] not in index_data['indices']:
                index_data['indices'].append(json_data['index'])

            if json_data['station'] not in index_data['data'].keys():
                index_data['data'][json_data['station']] = {}

            year_1, year_2 = json_data['baseline']

            for year in range(year_1, year_2 + 1):
                if str(year) not in index_data['data'][json_data['station']].keys():
                    index_data['data'][json_data['station']][str(year)] = {}
                index_data['data'][json_data['station']][str(year)][json_data['index']] = json_data[str(year)]['value']

##            break

##        print(json.dumps(index_data, indent=4))

##        # TODO: Retrieve external attributes of stations, i.e. aspect, slope, lan cover, etc.

        attributes_filename = os.path.join(
            Config.instance().climex_dir, 'PROJECTS', self._name, 'GEOJSON', 'attributes.json'
        )

        try:
            with open(attributes_filename, 'rt') as attributes_file:
                attributes_data = json.load(attributes_file)
        except:
            attributes_data = {}

##        print(attributes_filename)
##        print(json.dumps(attributes_data, indent=4))


        if data_format.upper() == 'CSV':
            self._export_to_csv(
                filename, station_by_id, index_data, attributes_data, separator
            )            

        
    def missing_index(self):
        """Shows a text output representing missing data in computed indices"""
        
        index_dir_contents = sorted(
            glob.glob(os.path.join(self._project_dir, 'INDEX', '*.json'))
        )

        missing_data = {}
        for json_filename in index_dir_contents:
##            print(json_filename)
            with open(json_filename, 'rt') as json_file:
                json_data = json.load(json_file)


            if json_data['index'] not in missing_data.keys():
                missing_data[json_data['index']] = {}

            missing_data[json_data['index']][json_data['station']] = {
                'baseline': json_data['baseline'],
                'data': []
            }

            base_1, base_2 = json_data['baseline']

            for year in range(base_1, base_2 + 1):
                missing_data[json_data['index']][json_data['station']]['data'].append(json_data[str(year)]['value'])

##            break

        output_text = ''
        for index_id, index_data in missing_data.items():
            output_text += index_id
            output_text += '\n\n'
##
##            print(index_data)

            record = ''            
            for station_id, station_data in index_data.items():
                record += station_id
                record += ' ' + str(station_data['baseline'])

                for value in station_data['data']:
##                    print(value, type(value), math.isnan(value))
                    if math.isnan(value):
                        record += ' -'
                    else:
                        record += ' +'
                record += '\n'
                
            output_text += record

##        print(output_text)
        for record in output_text.split('\n'):
            print(record)

##        print(json.dumps(missing_data, indent=4))
        
        
    def _get_computed_indices(self):
        """Returns a list of index names if some climate indices have been computed and an empty list otehrwise"""
        
        index_contents = glob.glob(os.path.join(self._project_dir, 'INDEX', '*.json'))

        indices = []
        for item in index_contents:
            current_index = os.path.splitext(item)[0].split('_')[-1]

            if current_index in klimdex.climdex_list and current_index not in indices:
                indices.append(current_index)

        return indices


    def check_download(self):
        """Checks if all stations in current project have been downloaded or not"""

        missing_download_files = {}
        for station in self.stations:
            conagua_filename = os.path.join(self._project_dir, 'CONAGUA', f'{station}.txt')
            climdex_filename = os.path.join(self._project_dir, 'CLIMDEX', f'{station}.txt')

            conagua_filename_exists = os.path.isfile(conagua_filename)
            climdex_filename_exists = os.path.isfile(climdex_filename)

            station_report = {}

            if not conagua_filename_exists:
                station_report['CONAGUA'] = 'missing'
            if not climdex_filename_exists:
                station_report['CLIMDEX'] = 'missing'

            if len(station_report) > 0:
                missing_download_files[str(station)] = station_report

        return missing_download_files


    def download_stations(self, stations):
        """Downloads files from a number of specific stations"""

        if not self._project_dir_exists():
            return
        
        if not isinstance(stations, list):
            stations = [stations]

        self.stations = stations

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'}

        for station in stations:

            url = f'{Config.instance().climex_obs_url}{station}.txt'

            print(f'Downloading  {url:62s}', end='')

            try:
                response = requests.get(url, headers=headers)
                print(f'\t[{response.status_code}]')
            except requests.exceptions.Timeout:
                print(f'\t[{response.status_code}]')
                print(f'Project.download(): {conagua_error}')
                continue
            except requests.exceptions.RequestException as conagua_error:
                print(f'\t[{response.status_code}]')
                print(f'Project.download(): {conagua_error}')
                continue

##            if response.status_code != 200:
##                failed_a.append(station)
##                print(f'\t[{response.status_code}]')
##                continue

            conagua_filename = os.path.join(self._project_dir, 'CONAGUA', f'{station}.txt')

            with open(conagua_filename, 'wt', encoding='utf-8') as conagua_file:
                conagua_file.write(response.text)

            conagua_data = response.text.split('\n')

            # Remove this when online //////////////////////////////
            #with open(conagua_filename, 'rt') as conagua_file:
            #    conagua_data = conagua_file.read().split('\n')
            # Remove this when online //////////////////////////////

            climdex_filename = os.path.join(self._project_dir, 'CLIMDEX', f'{station}.txt')

            # Convert to CLIMDEX format
            climdex_data = ''
            for record in conagua_data:

                try:
                    date, prcp, evap, tmax, tmin = record.split()
                except:
                    continue

                if prcp == 'Nulo': prcp = klimdex.null
                if evap == 'Nulo': evap = klimdex.null
                if tmax == 'Nulo': tmax = klimdex.null
                if tmin == 'Nulo': tmin = klimdex.null

                try:                    
                    prcp, evap, tmax, tmin = map(float, (prcp, evap, tmax, tmin))
                except:
                    continue

                day, month, year = date.split('/')

                climdex_record = f'{year:4s} {month:2s} {day:2s} {prcp:6.1f} {tmax:6.1f} {tmin:6.1f}\n'
                climdex_data += climdex_record

            with open(climdex_filename, 'wt') as climdex_file:
                climdex_file.write(climdex_data)

##            print(f'\t[{response.status_code}]')
##            print(f'\t{ornament}[{response.status_code}]')


    def get_attribute_from_raster(self, stations=None, grid_filename=None, attribute_name=None, target_epsg=4236, years=None, legend=None):
        """Adds a new attribute to \'stations\' from a raster map in ARC/INFO ASCII GRID format"""

        if stations is None:
            stations = self.stations

        if not isinstance(stations, list):
            stations = [stations]

        year_1, year_2 = self.baseline
            
        if years is None:
            years = list(range(year_1, year_2 + 1))
        elif isinstance(years, range):
            years = list(years)
        elif not isinstance(years, list):
            years = [years]

        if grid_filename is None:

            if 'easygui' not in sys.modules.keys():
                print('climex.Project.get_attribute_from_raster(): Package "easygui" not found (pip install easygui)')
                return

            grid_filename = easygui.fileopenbox(
                default='*.asc', filetypes=['*.asc']
            )

            if grid_filename is None:
                return

        if attribute_name is None:

            if 'easygui' not in sys.modules.keys():
                print('climex.Project.get_attribute_from_raster(): Package "easygui" not found (pip install easygui)')
                return

            attribute_name = easygui.enterbox(msg='Enter attribute name:')

            if attribute_name is None:
                return
            
        
        origin_epsg = 4326

        common_epsg = True
        if origin_epsg != target_epsg:
            # TODO: Create Projection objects
            common_epsg = False

        grid = geo.read_ascii_grid(grid_filename)

        longitude_min = grid['xllcorner']
        latitude_min = grid['yllcorner']

        # TODO: xllcenter, yllcenter

        longitude_max = longitude_min + grid['ncols'] * grid['cellsize']
        latitude_max = latitude_min + grid['nrows'] * grid['cellsize']


        attributes = {}

        attributes_filename = os.path.join(
            Config.instance().climex_dir, 'PROJECTS', \
            self._name.upper(), 'GEOJSON', 'attributes.json'
        )

        try:
            with open(attributes_filename, 'rt') as attributes_file:
                attributes = json.load(attributes_file)
##                attribute_items = json.load(attributes_file).items()
##
##                attributes = {
##                    str(key): value for key, value in attribute_items
##                }
        except:
            attributes = {
                'attributes': [],
                'data': {}
            }

            for station in stations:
                station = str(station)

                attributes['data'][station] = {}

                for year in range(year_1, year_2 + 1):
                    attributes['data'][station][str(year)] = {}

##        print(attributes)

        if attribute_name in attributes['attributes']:
            print(f'climex.Project.get_attribute_from_raster(): attribute "{attribute_name}" already exists. Please, change attribute name')
            return
        
        attributes['attributes'].append(attribute_name)

        # TODO: prepare reading the legend dictionary
        
        for station in stations:
            station = str(station)

            if not common_epsg:
                # Project coordinates
                pass

            station_data = Station.instance()._station(station)

            if not station_data:
                continue

            longitude, latitude, elevation = station_data['geometry']['coordinates']

            # TODO: Check station is within bounding box

            delta_longitude = longitude - longitude_min
            delta_latitude = latitude - latitude_min

            grid_row = int(delta_latitude / grid['cellsize'])
            grid_column = int(delta_longitude / grid['cellsize'])

##            print(grid['data'][grid_row][grid_column])

            grid_value = grid['data'][grid_row][grid_column]    
##
##            if station not in attributes.keys():
##                attributes[station] = {}
##            attributes[station][attribute_name] = grid_value
##

            if station not in attributes['data'].keys():
                attributes['data'][station] = {}
                for year in range(year_1, year_2 + 1):
                    attributes['data'][station][str(year)] = {}
            
            for year in range(year_1, year_2 + 1):
                if year in years:                    
                    try:
                        attributes['data'][station][str(year)][attribute_name] = grid_value
                        # TODO: apply legend value
                    except:
                        pass

        with open(attributes_filename, 'wt') as attributes_file:
            attributes_file.write(
                json.dumps(attributes, indent=4)
            )
            
##        print(attributes)


    def get_attribute_from_shapefile(self, stations=None, shapefilename=None, field_name=None, target_epsg=4236, years=None, legend=None):
        """Adds a new attribute to \'stations\' from a vector dataset in Shapefile format"""

        if stations is None:
            stations = self.stations

        year_1, year_2 = self.baseline
            
        if not isinstance(stations, list):
            stations = [stations]

        if years is None:
            years = list(range(year_1, year_2 + 1))
        elif isinstance(years, range):
            years = list(years)
        elif not isinstance(years, list):
            years = [years]
        
        if shapefilename is None:
            
            if 'easygui' not in sys.modules.keys():
                print('climex.Project.get_attribute_from_shapefile(): Package "easygui" not found (pip install easygui)')
                return
            
            shapefilename = easygui.fileopenbox(
                default='*.shp', filetypes=['*.shp']
            )

            if shapefilename is None:
                return

        shape = geo.read_shapefile(shapefilename)

        if shape['type'] != 'POLYGON':
                print('climex.Project.get_attribute_from_shapefile(): Shapefile must contain polygon entities')
                return

        if field_name is None:

            if 'easygui' not in sys.modules.keys():
                print('climex.Project.get_attribute_from_shapefile(): Package "easygui" not found (pip install easygui)')
                return

            field_name = easygui.choicebox(msg='Select field name:', choices=(shape['fields']))

            if field_name is None:
                return

        try:
            field_name_index = shape['fields'].index(field_name)
        except:
            print(f'climex.Project.get_attribute_from_shapefile(): field name "{field_name}" not found in attribute table')
            return

        origin_epsg = 4326

        # TODO: get shapefile CRS
        
        common_epsg = True
        if origin_epsg != target_epsg:
            # TODO: Create Projection objects
            common_epsg = False

        attributes = {}

        attributes_filename = os.path.join(
            Config.instance().climex_dir, 'PROJECTS', \
            self._name.upper(), 'GEOJSON', 'attributes.json'
        )

        try:
            with open(attributes_filename, 'rt') as attributes_file:
                attributes = json.load(attributes_file)
        except:
            attributes = {
                'attributes': [],
                'data': {}
            }

            for station in stations:
                station = str(station)

                attributes['data'][station] = {}

                for year in range(year_1, year_2 + 1):
                    attributes['data'][station][str(year)] = {}

        if field_name in attributes['attributes']:
            print(f'climex.Project.get_attribute_from_raster(): attribute "{field_name}" already exists. Please, change attribute name')
            return
        
        attributes['attributes'].append(field_name)

        # TODO: prepare reading the legend dictionary
                
        for station in stations:
            station = str(station)

            if not common_epsg:
                # TODO: Project coordinates
                pass

            station_data = Station.instance()._station(station)

            if not station_data:
                continue
            
            longitude, latitude, elevation = station_data['geometry']['coordinates']

            # TODO: Check station is within bounding box

            tentative_polygons = []
            for shift, polygon in enumerate(shape['geometries']):
                station_inside_polygon = geo.point_in_multipart_polygon(
                    longitude, latitude, polygon
                )

                if station_inside_polygon:
                    tentative_polygons.append(shift)

            if len(tentative_polygons) == 0:
                continue
            elif len(tentative_polygons) > 1:
                print('climex.Project.get_attribute_from_shapefile(): Multiple polygons to get attribute, check the Shapefile')
                continue

            shape_value = shape['attributes'][tentative_polygons[0]][field_name_index]

            if station not in attributes['data'].keys():
                attributes['data'][station] = {}
                for year in range(year_1, year_2 + 1):
                    attributes['data'][station][str(year)] = {}
            
            for year in range(year_1, year_2 + 1):
                if year in years:
                    try:
                        attributes['data'][station][str(year)][field_name] = shape_value
                        # TODO: apply legend value
                    except:
                        pass

        with open(attributes_filename, 'wt') as attributes_file:
            attributes_file.write(
                json.dumps(attributes, indent=4)
            )


##    def ingest(self, ingest_folder=None):
    def feed(self, feed_folder=None):
        """Incorporates observation files from data sources other than CONAGUA"""

        # TODO
    
    def compute_normal(self, normal_baseline=[1961, 1990]):
        # import climex; test = climex.Project('test_normal')
        
        base_1, base_2 = normal_baseline
        
        for station in self.stations:
            baseline_filename = os.path.join(
                Config.instance().climex_dir, 'PROJECTS', self._name.upper(),
                'CLIMDEX', f'{station}_{base_1}_{base_2}.txt'
            )

            if not os.path.isfile(baseline_filename):
                project_baseline = self.baseline
                self.baseline = normal_baseline
                self.qc(verbose=False)
                self.baseline = project_baseline

        #normal._compute_prcp_normals(self, normal_baseline)
        normal._compute_temp_normals(self, normal_baseline, 'tmean')
        #normal._compute_temp_normals(self, normal_baseline, 'tmax')
        #normal._compute_temp_normals(self, normal_baseline, 'tmin')


    def anomaly(self, anomalous_years=None, normal_baseline=[1961, 1990]):

        if anomalous_years is None:
            base_1, base_2 = self.baseline
            anomalous_years = range(base_1, base_2 + 1)
        elif not isinstance(anomaly_years, list):
            anomalous_years = [anomaly_years]

        for year in anomalous_years:
            if not isinstance(year, int):
                # MSG: not an integer
                return

        normal._prcp_monthly_anomaly(self, anomalous_years, normal_baseline)
        normal._temp_monthly_anomaly(self, anomalous_years, normal_baseline, 'tmean')


    def heatwave(self, threshold=30, length=3, plot=False):

        try:
            threshold = float(threshold)
        except:
            return

        base_1, base_2 = self.baseline
        
        for station in self.stations:

            heatwave_data = {
                'summary': {}, 'heatwave': [], 'date': [], 'heat': []
            }

            baseline_filename = os.path.join(
                Config.instance().climex_dir, 'PROJECTS', self._name.upper(),
                'CLIMDEX', f'{station}_{base_1}_{base_2}.txt'
            )

            #print(baseline_filename)

            # Read data
            
            with open(baseline_filename, 'rt') as baseline_file:
                dataset = baseline_file.readlines()

            # Create binary series (1 if Tmax > threshold, 0 otherwise)
            
            for record in dataset:
                year, month, day, prpc, tmax, tmin = record.split()

                heatwave_data['date'].append(f'{year}-{month}-{day}')

                if float(tmax) > threshold:
                    heatwave_data['heat'].append(1)
                elif float(tmax) == klimdex.null:
                    heatwave_data['heat'].append(0)
                else:
                    heatwave_data['heat'].append(0)

                if year not in heatwave_data['summary'].keys():
                    heatwave_data['summary'][year] = {
                        'count': None, 'sum': None, 'average': None, 'max': None, 'lengths': []
                    }

            # Compute spells

            if heatwave_data['heat'][0] == 1:
                heatwave_data['heatwave'].append({
                    'index': 0,
                    'date': heatwave_data['date'][0],
                    'length': 1
                })

            for count in range(1, len(heatwave_data['heat'])):

                if heatwave_data['heat'][count] != 1:
                    continue

                if heatwave_data['heat'][count] != heatwave_data['heat'][count - 1]:
                    heatwave_data['heatwave'].append({
                        'index': count,
                        'date': heatwave_data['date'][count],
                        'length': 1
                    })
                else:
                    heatwave_data['heatwave'][-1]['length'] += 1

            # Compute summary

            for wave in heatwave_data['heatwave']:

                year = wave['date'].split('-')[0]

                if wave['length'] > length:

                    heatwave_data['summary'][year]['lengths'].append(wave['length'])

                    
##                    heatwave_data['summary'][year]['average'] += wave['length']
##                    
##                    if heatwave_data['summary'][year]['max'] is None:
##                        heatwave_data['summary'][year]['max'] = wave['length']

                
##                print(wave)
##                break

            for year, summary in heatwave_data['summary'].items():

                if len(summary['lengths']) == 0:
                    continue

                summary['count'] = len(summary['lengths'])
                summary['sum'] = sum(summary['lengths'])
                summary['average'] = sum(summary['lengths']) / summary['count']
                summary['max'] = max(summary['lengths'])


            heatwave_filename = os.path.join(
                Config.instance().climex_dir, 'PROJECTS', self._name.upper(),
                'NORMAL', f'{station}_heatwave_{base_1}_{base_2}.json'
            )

            with open(heatwave_filename, 'wt') as heatwave_file:
                json.dump(heatwave_data, heatwave_file, indent=4)
                

    def get_csv_header(self, csv_filename=None, separator=','):
        """Prints the fields in the first row of a CSV file"""
        
        if csv_filename is None:
            
            if 'easygui' not in sys.modules.keys():
                print('climex.Project.get_csv_header(): Package "easygui" not found (pip install easygui)')
                return
            
            csv_filename = easygui.fileopenbox(
                default='*.csv', filetypes=['*.csv']
            )

            if csv_filename is None:
                return

        with open(csv_filename, 'rt') as csvfile:
            first_row = csvfile.readlines()[0]

        header = [token.strip('"') for token in first_row.strip().split(separator)]

        header_string = '{\n'
        for i, item in enumerate(header):
            if item == '':
                item = '\'\' [empty string]'
            
            header_string += f'    {i}: {item}\n'
        header_string += '}'

        print(header_string)


    def get_csv_ids(self, id_field, csv_filename=None, header=True, separator=','):
        """Prints the fields in the first row of a CSV file"""

        # TODO: check id_field is integer
        
        if csv_filename is None:
            
            if 'easygui' not in sys.modules.keys():
                print('climex.Project.get_csv_header(): Package "easygui" not found (pip install easygui)')
                return
            
            csv_filename = easygui.fileopenbox(
                default='*.csv', filetypes=['*.csv']
            )

            if csv_filename is None:
                return

        with open(csv_filename, 'rt') as csv_file:
            csv_rows = csv_file.readlines()

        if header:
            starting_row = 1
        else:
            starting_row = 0

        csv_ids = []
        for row in csv_rows[starting_row:]:
            csv_ids.append(row.split(separator)[id_field].strip('"'))

        return csv_ids


    def get_csv_sample(self, csv_filename=None, separator=','):
        """Prints the fields in the first row of a CSV file"""
        
        if csv_filename is None:
            
            if 'easygui' not in sys.modules.keys():
                print('climex.Project.get_csv_sample(): Package "easygui" not found (pip install easygui)')
                return
            
            csv_filename = easygui.fileopenbox(
                default='*.csv', filetypes=['*.csv']
            )

            if csv_filename is None:
                return

        with open(csv_filename, 'rt') as csv_file:
            csv_rows = csv_file.readlines()

        for row in csv_rows[:5]:
            print(row)

        print(f'\nTotal {len(csv_rows)} rows')

    
    def get_attribute_from_csv(self, id_field, attribute_fields, csv_filename=None, header=True, year_field=None, separator=','):
        """Adds a new attribute to \'stations\' from a CSV file"""

        if not isinstance(attribute_fields, list):
            attribute_fields = [attribute_fields]

        # TODO: Check attribute_fields items are all integers
        # TODO: Check attribute fields are sorted
        
        base_1, base_2 = self.baseline
        
        if csv_filename is None:
            
            if 'easygui' not in sys.modules.keys():
                print('climex.Project.get_csv_header(): Package "easygui" not found (pip install easygui)')
                return
            
            csv_filename = easygui.fileopenbox(
                default='*.csv', filetypes=['*.csv']
            )

            if csv_filename is None:
                return

        with open(csv_filename, 'rt') as csv_file:
            csv_rows = csv_file.readlines()

        if header:
            starting_row = 1
            field_names = []
            for i, item in enumerate(csv_rows[0].strip().split(separator)):
                if i in attribute_fields:
                    field_names.append(item.strip('"'))
        else:
            starting_row = 0
            field_names = attribute_fields

        attributes = {}
        for row in csv_rows[starting_row:]:
            station_id = row.split(separator)[id_field].strip('"')

            if station_id in self.stations:
                attributes[station_id] = {}
                
                row_attributes = []
                for i, item in enumerate(row.strip().split(separator)):
                    if i in attribute_fields:
                        row_attributes.append(base.parse_item(item))

                for year in range(base_1, base_2 + 1):
                    if year_field is None:
                        pass
                    else:
                        pass # TODO
                    

            
##            csv_ids.append(row.split(separator)[id_field].strip('"'))

        print(field_names)
        
        return attributes
    
############# merge(): merges current project with other projects: TODO, very interesting
