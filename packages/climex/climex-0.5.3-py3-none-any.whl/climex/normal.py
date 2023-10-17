
import datetime
import json
import os

import matplotlib.pyplot as plt

import climex.klimdex as klimdex

from . config import Config
from . station import Station


missing_percentage_threshold = 0.8
missing_days_max = 11
missing_consecutive_days_max = 5


def _yearly_normal_record():
    """Creates a dictionary to store a yearly record of climate parameters"""

    record = {}
    for month in range(1, 13):
        record[f'{month:02d}'] = {
            'normal': None,
            'parameter': {
                'missing': 0,
                'count': 0, # of days with valid (non-missing) data
                'sum': 0.0,
                'mean': None,
                'min': None,
                'max': None
            },
            'missing': []
        }

    return record


def _group_consecutive_numbers(numbers):
        
    groups = [[numbers[0]]]
    for number in numbers[1:]:
        if number == groups[-1][-1] + 1:
            groups[-1].append(number)
        else:
            groups.append([number])

    test = True
    for group in groups:
        if len(group) >= missing_consecutive_days_max:
            test = False

    return test


def _normal_consecutive_test(missing):

    ordinal_missing_days = []
    for missing_day in missing:
        year, month, day = missing_day[:3]
        ordinal_missing_days.append(
            int(datetime.datetime(year, month, day).strftime('%j'))
        )
    
    return _group_consecutive_numbers(ordinal_missing_days)
    

def _pass_normal_missing_test(missing):

    if len(missing) >= missing_days_max:
        test = False
    elif len(missing) >= missing_consecutive_days_max:
        test = _normal_consecutive_test(missing)
    else:
        test = True

    return test


def _plot_prcp_monthly_anomalies(project, ):
    pass


def _plot_temp_monthly_anomalies(project, variable):
    pass



def _compute_prcp_normals(project, normal_baseline):
    """Computes monthly, yearly and project PRCP normals in a given baseline"""

    base_1, base_2 = normal_baseline

    prcp_raw_normal = {}
    prcp_monthly_normal = {}
    prcp_yearly_normal = {}
    prcp_project_monthly_normal = {}
    prcp_project_yearly_normal = {}

    for station in project.stations:

        prcp_raw = {}
        for year in range(base_1, base_2 + 1):
            prcp_raw[year] = _yearly_normal_record()

        baseline_filename = os.path.join(
            Config.instance().climex_dir, 'PROJECTS', project._name.upper(),
            'CLIMDEX', f'{station}_{base_1}_{base_2}.txt'
        )

        try:
            station_data = klimdex._read_climdex_file(baseline_filename)
        except:
            print(f'Project.compute_normal(): {baseline_filename} file not found')
            continue # to next station

        # 4.3.1. Calculation of individual monthly values
        
        for year in range(base_1, base_2 + 1):
            for month in range(1, 13):
                prcp_raw[year][f'{month:02d}']['parameter']['mean'] = station_data[0][3]
                prcp_raw[year][f'{month:02d}']['parameter']['min'] = station_data[0][3]
                prcp_raw[year][f'{month:02d}']['parameter']['max'] = station_data[0][3]

        for record in station_data[:]:
##            print(record)

            year, month, day, prcp, tmax, tmin = record

            if prcp == klimdex.null:
                prcp_raw[year][f'{month:02d}']['missing'].append(record)
                prcp_raw[year][f'{month:02d}']['parameter']['missing'] += 1
            else:
                prcp_raw[year][f'{month:02d}']['parameter']['count'] += 1
                prcp_raw[year][f'{month:02d}']['parameter']['sum'] += prcp
                prcp_raw[year][f'{month:02d}']['parameter']['mean'] += prcp

                if prcp < prcp_raw[year][f'{month:02d}']['parameter']['min']:
                    prcp_raw[year][f'{month:02d}']['parameter']['min'] = prcp
                elif prcp > prcp_raw[year][f'{month:02d}']['parameter']['max']:
                    prcp_raw[year][f'{month:02d}']['parameter']['max'] = prcp
                    

##        print(station.split('/')[-1])

##        station_ = station.split('/')[-1]

        for year in range(base_1, base_2 + 1):
            for month in range(1, 13):
                if prcp_raw[year][f'{month:02d}']['parameter']['missing'] > 11:
                    continue
                # elif > 5

                prcp_raw[year][f'{month:02d}']['normal'] = prcp_raw[year][f'{month:02d}']['parameter']['sum']

##        print(json.dumps(prcp_raw, indent=4))

        prcp_raw_normal[station] = prcp_raw        
##        break

        # 4.3.2. Calculation of monthly normals from individual monthly values

        prcp_monthly_normal_summary = {}

        for month in range(1, 13):
            prcp_monthly_normal_summary[f'{month:02d}'] = {
                'normal': {
                    'value': 0.0,
                    'sum': 0.0,
                    'count': 0,
                    'missing': 0
                },
                'missing': []
            }

        for year in range(base_1, base_2 + 1):
            for month in range(1, 13):

                if prcp_raw[year][f'{month:02d}']['normal'] is None:
##                    print('--------------------')
                    prcp_monthly_normal_summary[f'{month:02d}']['normal']['missing'] += 1
                    prcp_monthly_normal_summary[f'{month:02d}']['missing'].append([year, month])
                else:
                    prcp_monthly_normal_summary[f'{month:02d}']['normal']['sum'] += prcp_raw[year][f'{month:02d}']['normal']
                    prcp_monthly_normal_summary[f'{month:02d}']['normal']['count'] += 1

        for month in range(1, 13):
            # TODO: Discuss a value (rather than 24)
            if prcp_monthly_normal_summary[f'{month:02d}']['normal']['count'] > 24:
                prcp_monthly_normal_summary[f'{month:02d}']['normal']['value'] = prcp_monthly_normal_summary[f'{month:02d}']['normal']['sum'] / prcp_monthly_normal_summary[f'{month:02d}']['normal']['count']
            else:
                prcp_monthly_normal_summary[f'{month:02d}']['normal']['value'] = None

        prcp_monthly_normal[station] = prcp_monthly_normal_summary


        # 4.3.3.A Calculation of yearly normal from monthly normals

        prcp_yearly_normal[station] = {
            'normal': {
                'value': None,
                'sum': 0.0,
                'count': 0,
                'missing': 0
            },
            'missing': []
        }
        
        for month in range(1, 13):
            if prcp_monthly_normal_summary[f'{month:02d}']['normal']['value'] is None:
                prcp_yearly_normal[station]['normal']['missing'] += 1
                prcp_yearly_normal[station]['missing'].append(f'{month:02d}')
            else:
                prcp_yearly_normal[station]['normal']['sum'] += prcp_monthly_normal_summary[f'{month:02d}']['normal']['value']
                prcp_yearly_normal[station]['normal']['count'] += 1
                
        # TODO: check minimum months required, i.e. maximum missing data
        # if
        # else:
        prcp_yearly_normal[station]['normal']['value'] = prcp_yearly_normal[station]['normal']['sum']

        individual_monthly_normal_filename = os.path.join(
            Config.instance().climex_dir, 'PROJECTS', project._name.upper(),
            'NORMAL', f'{station}_{base_1}_{base_2}_prcp_individual_monthly_normals.json'
        )

        with open(individual_monthly_normal_filename, 'wt') as individual_monthly_normal_file:
            json.dump(prcp_raw_normal, individual_monthly_normal_file, indent=4)

        monthly_normal_filename = os.path.join(
            Config.instance().climex_dir, 'PROJECTS', project._name.upper(),
            'NORMAL', f'{station}_{base_1}_{base_2}_prcp_monthly_normals.json'
        )

        with open(monthly_normal_filename, 'wt') as monthly_normal_file:
            json.dump(prcp_monthly_normal, monthly_normal_file, indent=4)

        yearly_normal_filename = os.path.join(
            Config.instance().climex_dir, 'PROJECTS', project._name.upper(),
            'NORMAL', f'{station}_{base_1}_{base_2}_prcp_yearly_normals.json'
        )

        with open(yearly_normal_filename, 'wt') as yearly_normal_file:
            json.dump(prcp_yearly_normal, yearly_normal_file, indent=4)

    # 4.3.3.B Calculation of project monthly normals from monthly normals at all stations

    prcp_project_monthly_normal = {}

    for month in range(1, 13):
        prcp_project_monthly_normal[f'{month:02d}'] = {
            'normal': {
                'value': None,
                'sum': 0.0,
                'count': 0,
                'missing': 0
            },
            'stations': [],
            'missing': []
        }

    for station, dataset in prcp_monthly_normal.items():
        for month, normal in dataset.items():
            if normal['normal']['value'] is None:
                prcp_project_monthly_normal[month]['missing'].append(station)
                prcp_project_monthly_normal[month]['normal']['missing'] += 1
            else:
                prcp_project_monthly_normal[month]['stations'].append(station)
                prcp_project_monthly_normal[month]['normal']['count'] += 1
                prcp_project_monthly_normal[month]['normal']['sum'] += normal['normal']['value']

    number_of_stations = len(project.stations)

    for month, dataset in prcp_project_monthly_normal.items():
        if dataset['normal']['count'] >= missing_percentage_threshold * number_of_stations:
            dataset['normal']['value'] = dataset['normal']['sum'] / dataset['normal']['count']
    
    # 4.3.3.C Calculation of project yearly normal from yearly normals and at stations

    prcp_project_yearly_normal = {
        'normal': {
            'value': None,
            'sum': 0.0,
            'count': 0,
            'missing': 0
        },
        'stations': [],
        'missing': []
    }
    
    for station, dataset in prcp_yearly_normal.items():
##        print(station)
##        print(dataset['normal']['value'])

        if dataset['normal']['value'] is None:
            prcp_project_yearly_normal['normal']['missing'] += 1
            prcp_project_yearly_normal['missing'].append(station)
        else:
            prcp_project_yearly_normal['normal']['sum'] += dataset['normal']['value']
            prcp_project_yearly_normal['normal']['count'] += 1
            prcp_project_yearly_normal['stations'].append(station)

    prcp_project_yearly_normal['normal']['value'] = prcp_project_yearly_normal['normal']['sum'] / prcp_project_yearly_normal['normal']['count']

    project_monthly_normal_filename = os.path.join(
        Config.instance().climex_dir, 'PROJECTS', project._name.upper(),
        'NORMAL', f'project_{base_1}_{base_2}_prcp_monthly_normal.json'
    )

    with open(project_monthly_normal_filename, 'wt') as project_monthly_normal_file:
        json.dump(prcp_project_monthly_normal, project_monthly_normal_file, indent=4)

    project_yearly_normal_filename = os.path.join(
        Config.instance().climex_dir, 'PROJECTS', project._name.upper(),
        'NORMAL', f'project_{base_1}_{base_2}_prcp_yearly_normal.json'
    )

    with open(project_yearly_normal_filename, 'wt') as project_yearly_normal_file:
        json.dump(prcp_project_yearly_normal, project_yearly_normal_file, indent=4)


def _compute_temp_normals(project, normal_baseline, variable):
    """Computes monthly, yearly and project TEMP (TMEAN, TMAX or TMIN based on variable parameter) normals in a given baseline"""

    print('_compute_temp_normals()')

    if variable.upper() not in ['TMEAN', 'TMAX', 'TMIN']:
        # No message for now
        return
    
    base_1, base_2 = normal_baseline

    temp_raw_normal = {}
    temp_monthly_normal = {}
    temp_yearly_normal = {}
    temp_project_monthly_normal = {}
    temp_project_yearly_normal = {}

    for station in project.stations:

        temp_raw = {}
        for year in range(base_1, base_2 + 1):
            temp_raw[year] = _yearly_normal_record()

        baseline_filename = os.path.join(
            Config.instance().climex_dir, 'PROJECTS', project._name.upper(),
            'CLIMDEX', f'{station}_{base_1}_{base_2}.txt'
        )

        try:
            station_data = klimdex._read_climdex_file(baseline_filename)
        except:
            print(f'Project.compute_normal(): {baseline_filename} file not found')
            continue # to next station

        # 4.3.1. Calculation of individual monthly values
        
        for year in range(base_1, base_2 + 1):
            for month in range(1, 13):
                if variable == 'tmean':
                    pass # temp_raw[year][f'{month:02d}']['parameter']['mean'] = 0.5 * (station_data[0][4] + station_data[0][5])
                elif variable == 'tmax':
                    temp_raw[year][f'{month:02d}']['parameter']['max'] = station_data[0][4]
                elif variable == 'tmin':
                    temp_raw[year][f'{month:02d}']['parameter']['min'] = station_data[0][5]



        for record in station_data[:]:
##            print(record)

            year, month, day, temp, tmax, tmin = record

            if variable.upper() == 'TMEAN':
                if tmax == klimdex.null or tmin == klimdex.null:
                    temp_raw[year][f'{month:02d}']['missing'].append(record)
                    temp_raw[year][f'{month:02d}']['parameter']['missing'] += 1
                else:
                    temp_raw[year][f'{month:02d}']['parameter']['count'] += 1
                    temp_raw[year][f'{month:02d}']['parameter']['sum'] += 0.5 * (tmax + tmin)
            elif variable.upper() == 'TMAX':
                pass # TODO
            elif variable.upper() == 'TMIN':
                pass # TODO



##            if tmax == klimdex.null or tmin == klimdex.null:
##                temp_raw[year][f'{month:02d}']['missing'].append(record)
##                temp_raw[year][f'{month:02d}']['parameter']['missing'] += 1
##            else:
##                temp_raw[year][f'{month:02d}']['parameter']['count'] += 1
##                # discuss parameter variable = tmean, tmax, tmin: Not necessary
##                temp_raw[year][f'{month:02d}']['parameter']['sum'] += 0.5 * (tmax + tmin)
##                #temp_raw[year][f'{month:02d}']['parameter']['mean'] += 
##
##                if tmin < temp_raw[year][f'{month:02d}']['parameter']['min']:
##                    temp_raw[year][f'{month:02d}']['parameter']['min'] = tmin
##                if tmax > temp_raw[year][f'{month:02d}']['parameter']['max']:
##                    temp_raw[year][f'{month:02d}']['parameter']['max'] = tmax
                    

##        print(station.split('/')[-1])

##        station_ = station.split('/')[-1]

        for year in range(base_1, base_2 + 1):
            for month in range(1, 13):
##                if temp_raw[year][f'{month:02d}']['parameter']['missing'] > 11:
##                    continue
##                elif temp_raw[year][f'{month:02d}']['parameter']['missing'] > 5:
##                    pass # TODO
                if variable.upper() == 'TMEAN':
                    try:
                        temp_raw[year][f'{month:02d}']['parameter']['mean'] = temp_raw[year][f'{month:02d}']['parameter']['sum'] / temp_raw[year][f'{month:02d}']['parameter']['count']
                    except:
                        pass

                if not _pass_normal_missing_test(temp_raw[year][f'{month:02d}']['missing']):
                    continue
                
                if variable.upper() == 'TMEAN':
                    temp_raw[year][f'{month:02d}']['normal'] = temp_raw[year][f'{month:02d}']['parameter']['sum'] / temp_raw[year][f'{month:02d}']['parameter']['count']
                elif variable.upper() == 'TMAX':
                    pass # TODO
                elif variable.upper() == 'TMIN':
                    pass # TODO
            
        print(json.dumps(temp_raw, indent=4))

        temp_raw_normal[station] = temp_raw        
##        break

        # 4.3.2. Calculation of monthly normals from individual monthly values

        temp_monthly_normal_summary = {}

        for month in range(1, 13):
            temp_monthly_normal_summary[f'{month:02d}'] = {
                'normal': {
                    'value': 0.0,
                    'sum': 0.0,
                    'count': 0,
                    'missing': 0
                },
                'missing': []
            }

        for year in range(base_1, base_2 + 1):
            for month in range(1, 13):

                if temp_raw[year][f'{month:02d}']['normal'] is None:
                    temp_monthly_normal_summary[f'{month:02d}']['normal']['missing'] += 1
                    temp_monthly_normal_summary[f'{month:02d}']['missing'].append([year, month])
                else:
                    if variable.upper() == 'TMEAN':
                        temp_monthly_normal_summary[f'{month:02d}']['normal']['sum'] += temp_raw[year][f'{month:02d}']['normal']
                        temp_monthly_normal_summary[f'{month:02d}']['normal']['count'] += 1
                    elif variable.upper() == 'TMAX':
                        pass # TODO
                    elif variable.upper() == 'TMIN':
                        pass # TODO

        for month in range(1, 13):
            if temp_monthly_normal_summary[f'{month:02d}']['normal']['count'] > ((base_2 - base_1 + 1) * missing_percentage_threshold):
                if variable.upper() == 'TMEAN':
                    temp_monthly_normal_summary[f'{month:02d}']['normal']['value'] = temp_monthly_normal_summary[f'{month:02d}']['normal']['sum'] / temp_monthly_normal_summary[f'{month:02d}']['normal']['count']
                elif variable.upper() == 'TMAX':
                    pass # TODO
                elif variable.upper() == 'TMIN':
                    pass # TODO
            else:
                temp_monthly_normal_summary[f'{month:02d}']['normal']['value'] = None

        temp_monthly_normal[station] = temp_monthly_normal_summary


        # 4.3.3.A Calculation of yearly normal from monthly normals

        temp_yearly_normal[station] = {
            'normal': {
                'value': None,
                'sum': 0.0,
                'count': 0,
                'missing': 0
            },
            'missing': []
        }
        
        for month in range(1, 13):
            if temp_monthly_normal_summary[f'{month:02d}']['normal']['value'] is None:
                temp_yearly_normal[station]['normal']['missing'] += 1
                temp_yearly_normal[station]['missing'].append(f'{month:02d}')
            else:
                # discuss parameter variable = tmean, tmax, tmin
                if variable.upper() == 'TMEAN':
                    temp_yearly_normal[station]['normal']['sum'] += temp_monthly_normal_summary[f'{month:02d}']['normal']['value']
                    temp_yearly_normal[station]['normal']['count'] += 1
                elif variable.upper() == 'TMAX':
                    pass # TODO
                elif variable.upper() == 'TMIN':
                    pass # TODO

        # TODO: check minimum months required, i.e. maximum missing data
        # if
        # else:
        temp_yearly_normal[station]['normal']['value'] = temp_yearly_normal[station]['normal']['sum'] / temp_yearly_normal[station]['normal']['count']



        individual_monthly_normal_filename = os.path.join(
            Config.instance().climex_dir, 'PROJECTS', project._name.upper(),
            'NORMAL', f'{station}_{base_1}_{base_2}_{variable.lower()}_individual_monthly_normals.json'
        )

        with open(individual_monthly_normal_filename, 'wt') as individual_monthly_normal_file:
            json.dump(temp_raw_normal, individual_monthly_normal_file, indent=4)

        monthly_normal_filename = os.path.join(
            Config.instance().climex_dir, 'PROJECTS', project._name.upper(),
            'NORMAL', f'{station}_{base_1}_{base_2}_{variable.lower()}_monthly_normals.json'
        )

        with open(monthly_normal_filename, 'wt') as monthly_normal_file:
            json.dump(temp_monthly_normal, monthly_normal_file, indent=4)

        yearly_normal_filename = os.path.join(
            Config.instance().climex_dir, 'PROJECTS', project._name.upper(),
            'NORMAL', f'{station}_{base_1}_{base_2}_{variable.lower()}_yearly_normals.json'
        )

        with open(yearly_normal_filename, 'wt') as yearly_normal_file:
            json.dump(temp_yearly_normal, yearly_normal_file, indent=4)


    # 4.3.3.B Calculation of project monthly normals from monthly normals at all stations

    temp_project_monthly_normal = {}

    for month in range(1, 13):
        temp_project_monthly_normal[f'{month:02d}'] = {
            'normal': {
                'value': None,
                'sum': 0.0,
                'count': 0,
                'missing': 0
            },
            'stations': [],
            'missing': []
        }

    for station, dataset in temp_monthly_normal.items():
        for month, normal in dataset.items():
            if normal['normal']['value'] is None:
                temp_project_monthly_normal[month]['missing'].append(station)
                temp_project_monthly_normal[month]['normal']['missing'] += 1
            else:
            # discuss parameter variable = tmean, tmax, tmin
                if variable.upper() == 'TMEAN':
                    temp_project_monthly_normal[month]['stations'].append(station)
                    temp_project_monthly_normal[month]['normal']['count'] += 1
                    temp_project_monthly_normal[month]['normal']['sum'] += normal['normal']['value']
                elif variable.upper() == 'TMAX':
                    pass # TODO
                elif variable.upper() == 'TMIN':
                    pass # TODO

    number_of_stations = len(project.stations)

    for month, dataset in temp_project_monthly_normal.items():
        if variable.upper() == 'TMEAN':
            if dataset['normal']['count'] >= missing_percentage_threshold * number_of_stations:
                dataset['normal']['value'] = dataset['normal']['sum'] / dataset['normal']['count']
        elif variable.upper() == 'TMAX':
            pass # TODO
        elif variable.upper() == 'TMIN':
            pass # TODO

    # 4.3.3.C Calculation of project yearly normal from yearly normals and at stations

    temp_project_yearly_normal = {
        'normal': {
            'value': None,
            'sum': 0.0,
            'count': 0,
            'missing': 0
        },
        'stations': [],
        'missing': []
    }
    
    for station, dataset in temp_yearly_normal.items():
##        print(station)
##        print(dataset['normal']['value'])

        if dataset['normal']['value'] is None:
            temp_project_yearly_normal['normal']['missing'] += 1
            temp_project_yearly_normal['missing'].append(station)
        else:
            # discuss parameter variable = tmean, tmax, tmin
            if variable.upper() == 'TMEAN':
                temp_project_yearly_normal['normal']['sum'] += dataset['normal']['value']
                temp_project_yearly_normal['normal']['count'] += 1
                temp_project_yearly_normal['stations'].append(station)
            elif variable.upper() == 'TMAX':
                pass # TODO
            elif variable.upper() == 'TMIN':
                pass # TODO


    if variable.upper() == 'TMEAN':

        if temp_project_yearly_normal['normal']['count'] >= missing_percentage_threshold * number_of_stations:
            temp_project_yearly_normal['normal']['value'] = temp_project_yearly_normal['normal']['sum'] / temp_project_yearly_normal['normal']['count']
    elif variable.upper() == 'TMAX':
        pass # TODO
    elif variable.upper() == 'TMIN':
        pass # TODO
    
    project_monthly_normal_filename = os.path.join(
        Config.instance().climex_dir, 'PROJECTS', project._name.upper(),
        'NORMAL', f'project_{base_1}_{base_2}_{variable.lower()}_monthly_normal.json'
    )

    with open(project_monthly_normal_filename, 'wt') as project_monthly_normal_file:
        json.dump(temp_project_monthly_normal, project_monthly_normal_file, indent=4)

    project_yearly_normal_filename = os.path.join(
        Config.instance().climex_dir, 'PROJECTS', project._name.upper(),
        'NORMAL', f'project_{base_1}_{base_2}_{variable.lower()}_yearly_normal.json'
    )

    with open(project_yearly_normal_filename, 'wt') as project_yearly_normal_file:
        json.dump(temp_project_yearly_normal, project_yearly_normal_file, indent=4)


def _prcp_monthly_anomaly(project, anomalous_years, normal_baseline):
    """Computes PRCP anomalies with respect to a baseline normal"""

    project_monthly_normals = {}

    for station in project.stations:

        base_1, base_2 = normal_baseline

        monthly_normal_filename = os.path.join(
            Config.instance().climex_dir, 'PROJECTS', project._name.upper(),
            'NORMAL', f'{station}_{base_1}_{base_2}_prcp_monthly_normals.json'
        )

        try:
            with open(monthly_normal_filename, 'rt') as monthly_normal_file:
                baseline_monthly_normals = json.load(monthly_normal_file)
        except:
            print(f'Project.compute_anomaly(): {monthly_normal_filename} file not found')
            continue # to next station


        base_1, base_2 = project.baseline

        project_data_filename = os.path.join(
            Config.instance().climex_dir, 'PROJECTS', project._name.upper(),
            'CLIMDEX', f'{station}_{base_1}_{base_2}.txt'
        )
        
        try:
            station_data = klimdex._read_climdex_file(project_data_filename)
        except:
            print(f'Project.compute_normal(): {project_data_filename} file not found')
            continue # to next station

        station_monthly_normals = {}
        for year in range(base_1, base_2 + 1):
            station_monthly_normals[year] = _yearly_normal_record()

        for year in range(base_1, base_2 + 1):
            for month in range(1, 13):
                station_monthly_normals[year][f'{month:02d}']['parameter']['mean'] = station_data[0][3]
                station_monthly_normals[year][f'{month:02d}']['parameter']['min'] = station_data[0][3]
                station_monthly_normals[year][f'{month:02d}']['parameter']['max'] = station_data[0][3]

        for record in station_data:

            year, month, day, prcp, tmax, tmin = record

            if prcp == klimdex.null:
                station_monthly_normals[year][f'{month:02d}']['missing'].append(record)
                station_monthly_normals[year][f'{month:02d}']['parameter']['missing'] += 1
            else:
                station_monthly_normals[year][f'{month:02d}']['parameter']['count'] += 1
                station_monthly_normals[year][f'{month:02d}']['parameter']['sum'] += prcp
                station_monthly_normals[year][f'{month:02d}']['parameter']['mean'] += prcp

##                if prcp < station_monthly_normals[year][f'{month:02d}']['parameter']['min']:
##                    station_monthly_normals[year][f'{month:02d}']['parameter']['min'] = prcp
##                elif prcp > station_monthly_normals[year][f'{month:02d}']['parameter']['max']:
##                    station_monthly_normals[year][f'{month:02d}']['parameter']['max'] = prcp

        for year, dataset in station_monthly_normals.items():
            for month, normal in dataset.items():

##                if variable.upper() == 'TMEAN':
                    if _pass_normal_missing_test(normal['missing']):
##                    if _pass_normal_missing_test(normal['parameter']['missing']):
                    #if normal['parameter']['missing'] < 5:
                        normal['normal'] = normal['parameter']['sum']

        project_monthly_normals[station] = station_monthly_normals

##        print(json.dumps(station_monthly_normals, indent=4))
##        break

    # TODO: write files with project_monthly_normals
    
##    print(json.dumps(project_monthly_normals, indent=4))
##    print(json.dumps(baseline_monthly_normals, indent=4))

##    project_monthly_anomalies = {}
##    year_data = []
##    anomaly_data = []


    #############################################
##    _plot_prcp_monthly_anomalies()
    base_3, base_4 = normal_baseline

    station_monthly_anomaly_filename = os.path.join(
        Config.instance().climex_dir, 'PROJECTS', project._name.upper(),
        'NORMAL', f'{station}_{base_1}_{base_2}_monthly_anomaly_baseline_{base_3}_{base_4}.png'
    )
    
    for station, dataset in project_monthly_normals.items():

        station_monthly_anomaly_filename = os.path.join(
            Config.instance().climex_dir, 'PROJECTS', project._name.upper(),
            'NORMAL', f'{station}_{base_1}_{base_2}_prcp_monthly_anomaly_baseline_{base_3}_{base_4}.png'
        )

        project_monthly_anomalies = {}
        year_data = []
        anomaly_data = []

        project_monthly_anomalies[station] = {}
        for year, year_dataset in dataset.items():
            for month, month_dataset in year_dataset.items():
##                print(year, month, month_dataset['normal'], baseline_monthly_normals[station][month]['normal']['value'])
##                print(month_dataset['normal'])
##                print(baseline_monthly_normals[station][month]['normal']['value'])
                if month_dataset['normal'] is None:
                    continue
                monthly_anomaly = month_dataset['normal'] - baseline_monthly_normals[station][month]['normal']['value']
##                print(monthly_anomaly)
                
                year_data.append(year)
                anomaly_data.append(monthly_anomaly)

        
        fig, ax = plt.subplots()
    ##    plt.figure()





        x_ticks = []
        x_labels = []
        x_minor_ticks = []
        
        for i, anomaly_value in enumerate(anomaly_data):
##            print(anomaly_value)

            if year_data[i] != year_data[i - 1]:
                x_ticks.append(i)
                x_minor_ticks.append(i + 6)
                x_labels.append(year_data[i])

            if anomaly_value is None:
                continue
            
            if anomaly_value >= 0:
##                colour = 'b'
                colour = 'tab:blue'
            else:
##                colour = 'silver'
                colour = 'tab:gray'

            plt.vlines(
                x=i, ymin=0.0, ymax=anomaly_value, color=colour, linewidth=2
    ##            label = 'axvline - % of full height'
            )

            if i == 10*12:
                break

        # Parameters:
        # 10 years, aspect=0.1, linewidth=2, size_ticks=8, size_ylabel, size_title
        #  5 years, aspect=0.05, linewidth=4

        x_ticks.append(x_ticks[-1] + 12)
##        x_labels.append(year_data[-1] + 1)
        
        ax.set_aspect(0.1)

        ax.set_ylabel('Anomaly (mm)', fontsize=6)
 
        #ax.set_xticks(x_ticks, minor=False)
        ax.set_xticks(x_ticks, minor=True)

        #plt.grid(axis='x', color='thistle', linewidth = 0.25)
        for x_coordinate in x_ticks:
            plt.axvline(x=x_coordinate, color='thistle', linewidth=0.25, zorder=0)

        #plt.xticks(x_ticks, [], fontsize=5) #, x_labels, fontsize=5)
        plt.xticks(x_minor_ticks, x_labels, fontsize=5)

        plt.tick_params(axis='x', which='major', bottom=False, top=False)
        plt.yticks([-200, -100, 0, 100, 200], fontsize=5)

        plt.ylim([-210, 210])

        plt.title(
            f'{station} - {Station.instance()._name_state(station)} - PRCP Monthly anomalies (Baseline {base_3}-{base_4})',
            fontdict = {'fontsize': 7}
        )
        
##        plt.show()

        fig.savefig(station_monthly_anomaly_filename, bbox_inches='tight', dpi=300)
        
        plt.clf()
        plt.close()

        print()
        print(x_ticks)
        print(x_labels)

        print(station_monthly_anomaly_filename)
        

def _temp_monthly_anomaly(project, anomalous_years, normal_baseline, variable):        
    """Computes TEMP (TMEAN, TMAX, TMIN) anomalies with respect to a baseline normal"""

    print('_compute_temp_anomaly()')
    
    project_monthly_normals = {}

    if variable.upper() not in ['TMEAN', 'TMAX', 'TMIN']:
        return

    for station in project.stations:

        base_1, base_2 = normal_baseline

        monthly_normal_filename = os.path.join(
            Config.instance().climex_dir, 'PROJECTS', project._name.upper(),
            'NORMAL', f'{station}_{base_1}_{base_2}_{variable.lower()}_monthly_normals.json'
        )

        try:
            with open(monthly_normal_filename, 'rt') as monthly_normal_file:
                baseline_monthly_normals = json.load(monthly_normal_file)
        except:
            print(f'Project.compute_anomaly(): {monthly_normal_filename} file not found')
            continue # to next station
        
        base_1, base_2 = project.baseline

        project_data_filename = os.path.join(
            Config.instance().climex_dir, 'PROJECTS', project._name.upper(),
            'CLIMDEX', f'{station}_{base_1}_{base_2}.txt'
        )
        
        try:
            station_data = klimdex._read_climdex_file(project_data_filename)
        except:
            print(f'Project.compute_anomaly(): {project_data_filename} file not found')
            continue # to next station
        
        station_monthly_normals = {}
        for year in range(base_1, base_2 + 1):
            station_monthly_normals[year] = _yearly_normal_record()

##        for year in range(base_1, base_2 + 1):
##            for month in range(1, 13):
##                station_monthly_normals[year][f'{month:02d}']['parameter']['mean'] = 0.5 * (station_data[0][4] + station_data[0][5])
##                station_monthly_normals[year][f'{month:02d}']['parameter']['min'] = station_data[0][4]
##                station_monthly_normals[year][f'{month:02d}']['parameter']['max'] = station_data[0][5]

        for record in station_data:

            year, month, day, prcp, tmax, tmin = record

            if variable.upper() == 'TMEAN':
                if tmax == klimdex.null or tmin == klimdex.null:
                    station_monthly_normals[year][f'{month:02d}']['missing'].append(record)
                    station_monthly_normals[year][f'{month:02d}']['parameter']['missing'] += 1
                else:
                    station_monthly_normals[year][f'{month:02d}']['parameter']['count'] += 1
                    station_monthly_normals[year][f'{month:02d}']['parameter']['sum'] += 0.5 * (tmax + tmin)
                    station_monthly_normals[year][f'{month:02d}']['parameter']['mean'] = station_monthly_normals[year][f'{month:02d}']['parameter']['sum'] / station_monthly_normals[year][f'{month:02d}']['parameter']['count']

####                if prcp < station_monthly_normals[year][f'{month:02d}']['parameter']['min']:
####                    station_monthly_normals[year][f'{month:02d}']['parameter']['min'] = prcp
####                elif prcp > station_monthly_normals[year][f'{month:02d}']['parameter']['max']:
####                    station_monthly_normals[year][f'{month:02d}']['parameter']['max'] = prcp
            elif variable.upper() == 'TMAX':
                pass # TODO
            elif variable.upper() == 'TMIN':
                pass # TODO

        for year, dataset in station_monthly_normals.items():
            for month, normal in dataset.items():
                if variable.upper() == 'TMEAN':
                    if _pass_normal_missing_test(normal['missing']):
                        normal['normal'] = normal['parameter']['mean']
                elif variable.upper() == 'TMAX':
                    pass # TODO
                elif variable.upper() == 'TMIN':
                    pass # TODO

        project_monthly_normals[station] = station_monthly_normals

##        print(json.dumps(station_monthly_normals, indent=4))
##        break

    # TODO: write file with project_monthly_normals
    


##    if plot:
##        pass
##    
##    print(json.dumps(project_monthly_normals, indent=4))
##    print(json.dumps(baseline_monthly_normals, indent=4))
##
####    project_monthly_anomalies = {}
####    year_data = []
####    anomaly_data = []








##
##
##    #############################################
####    _plot_temp_monthly_anomalies()
    base_3, base_4 = normal_baseline

    station_monthly_anomaly_filename = os.path.join(
        Config.instance().climex_dir, 'PROJECTS', project._name.upper(),
        'NORMAL', f'{station}_{base_1}_{base_2}_{variable.lower()}_monthly_anomaly_baseline_{base_3}_{base_4}.png'
    )
    
    for station, dataset in project_monthly_normals.items():

        station_monthly_anomaly_filename = os.path.join(
            Config.instance().climex_dir, 'PROJECTS', project._name.upper(),
            'NORMAL', f'{station}_{base_1}_{base_2}_{variable.lower()}_monthly_anomaly_baseline_{base_3}_{base_4}.png'
        )

        project_monthly_anomalies = {}
        year_data = []
        anomaly_data = []

        project_monthly_anomalies[station] = {}
        for year, year_dataset in dataset.items():
            for month, month_dataset in year_dataset.items():
##                print(year, month, month_dataset['normal'], baseline_monthly_normals[station][month]['normal']['value'])
##                print(month_dataset['normal'])
##                print(baseline_monthly_normals[station][month]['normal']['value'])
                if month_dataset['normal'] is None or baseline_monthly_normals[station][month]['normal']['value'] is None:
                    continue
                monthly_anomaly = month_dataset['normal'] - baseline_monthly_normals[station][month]['normal']['value']
##                print(monthly_anomaly)
                
                year_data.append(year)
                anomaly_data.append(monthly_anomaly)

        
        fig, ax = plt.subplots()
    ##    plt.figure()





        x_ticks = []
        x_labels = []
        x_minor_ticks = []
        
        for i, anomaly_value in enumerate(anomaly_data):
##            print(anomaly_value)

            if year_data[i] != year_data[i - 1]:
                x_ticks.append(i)
                x_minor_ticks.append(i + 6)
                x_labels.append(year_data[i])

            if anomaly_value is None:
                continue
            
            if anomaly_value >= 0:
                colour = 'tab:red'
            else:
                colour = 'tab:blue'

            plt.vlines(
                x=i, ymin=0.0, ymax=anomaly_value, color=colour, linewidth=2
    ##            label = 'axvline - % of full height'
            )

            if i == 10*12:
                break

        # Parameters:
        # 10 years, aspect=5, linewidth=2, size_ticks=8, size_ylabel, size_title
        #  5 years, aspect=0.05, linewidth=4

        x_ticks.append(x_ticks[-1] + 12)
##        x_labels.append(year_data[-1] + 1)
        
        ax.set_aspect(5)

        ax.set_ylabel('Anomaly ($^\circ$C)', fontsize=6)
 
        #ax.set_xticks(x_ticks, minor=False)
        ax.set_xticks(x_ticks, minor=True)

        #plt.grid(axis='x', color='thistle', linewidth = 0.25)
        for x_coordinate in x_ticks:
            plt.axvline(x=x_coordinate, color='thistle', linewidth=0.25, zorder=0)

        #plt.xticks(x_ticks, [], fontsize=5) #, x_labels, fontsize=5)
        plt.xticks(x_minor_ticks, x_labels, fontsize=5)

        plt.tick_params(axis='x', which='major', bottom=False, top=False)
        plt.yticks([-3, -2, -1, 0, 1, 2, 3], fontsize=5)

        plt.ylim([-3.5, 3.5])

        plt.title(
            f'{station} - {Station.instance()._name_state(station)} - {variable.upper()} Monthly anomalies (Baseline {base_3}-{base_4})',
            fontdict = {'fontsize': 7}
        )
        
##        plt.show()

        fig.savefig(station_monthly_anomaly_filename, bbox_inches='tight', dpi=300)
        
        plt.clf()
        plt.close()
##
##        print()
##        print(x_ticks)
##        print(x_labels)
##
##        print(station_monthly_anomaly_filename)
##    

