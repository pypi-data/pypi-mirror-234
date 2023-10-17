
import os
import json
import sys

import matplotlib.pyplot as plt

from . klimdex import null
from . station import Station


rules = ((3, 5), (4, 10))

days_per_month = {
    1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
    7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12:31
} 

def leap_year(year):
    """Returns 1 if 'year' is a leap year and 0 if 'year' is not a leap year"""

    if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
        leap = 1
    else:
        leap = 0

    return(leap)

def qc0(station, dataset, baseline, rule=rules[0]):
    """Checks data consistency: PRCP is positive, TMAX is greater than TMIN and restores lost records"""

    base_1, base_2 = baseline

    qc_report = {'records': 0}
    for year in range(base_1, base_2 + 1):
        qc_report[year] = {
            'records': 0,
            'missing': 0,
            'lost': 0,
            'tmin>tmax': 0,
            'prcp<0.0': 0
        }

    qc_dataset = []
    for record in dataset:
        year, month, day, prcp, tmax, tmin = record

        if year < base_1 or year > base_2:
            continue

        if prcp == null or tmax == null or tmin == null:
            #qc_report[year]['missing'].append(record)
            qc_report[year]['missing'] += 1
        elif tmax != null and tmin != null and tmin > tmax:
            #qc_report[year]['tmin>tmax'].append(record)
            qc_report[year]['tmin>tmax'] += 1
            tmax = null
            tmin = null
        elif prcp != null and prcp < 0.0: 
            #qc_report[year]['prcp<0.0'].append(record)
            qc_report[year]['prcp<0.0'] += 1
            prcp = null

        qc_dataset.append([year, month, day, prcp, tmax, tmin])

        qc_report['records'] += 1
        qc_report[year]['records'] += 1

    for year in range(base_1, base_2 + 1):
        number_of_days = 365 + leap_year(year)
        qc_report[year]['lost'] = number_of_days - qc_report[year]['records']

    wrong_years = {}
    for year in range(base_1, base_2 + 1):
        if qc_report[year]['lost'] == 0:
            continue

        whole_year = []
        for month in range(1, 13):
            n = days_per_month[month]
            if month == 2:
                n += leap_year(year)
            for day in range(1, n + 1):
                whole_year.append([year, month, day])

        wrong_years[year] = {
            'whole': whole_year,
            'observed': []
        }     

    #print(json.dumps(qc_report, indent=4))
    #print()
    #print(json.dumps(wrong_years, indent=4))

    #for year in wrong_years:
    #    print(year, len(wrong_years[year]['whole']))


    for record in qc_dataset:
        year, month, day, prcp, tmax, tmin = record

        if year in wrong_years.keys():
            wrong_years[year]['observed'].append([year, month, day])

    lost_records = []
    lost_records_report = []
    for year in wrong_years:
        #print(year, len(wrong_years[year]['whole']), len(wrong_years[year]['observed']))
        for record in wrong_years[year]['whole']:
            if record not in wrong_years[year]['observed']:
                lost_records.append(record + [null, null, null])
                year, month, day = record
                lost_records_report.append(f'{year:4d}-{month:02d}-{day:02d}')

    qc_report['lost_records'] = lost_records_report        

    return qc_report, sorted(qc_dataset + lost_records)

def qc1(station, dataset, rule=rules[0]):
    """Checks rules for computation of climate normals"""
    pass

def qc2(station, dataset):
    """Detects outliers present in the dataset"""
    pass

def missing_data_plot(station, station_name, project_dir, dataset, baseline):

##    print(sys.modules.keys())

    if 'matplotlib.pyplot' not in sys.modules.keys():
        ## Message?
        return

    ##################### station_name no longer necessary !!!!!!!
    base_1, base_2 = baseline

    prcp_filename = os.path.join(project_dir, 'QC', f'{station}_{base_1}_{base_2}_qc_prcp.png')
    temp_filename = os.path.join(project_dir, 'QC', f'{station}_{base_1}_{base_2}_qc_temp.png')

    #prcp_filename = f'{basename}_prcp.png'
    #tmax_filename = f'{basename}_tmax.png'
    #tmin_filename = f'{basename}_tmix.png'

    #print(prcp_filename)

    prcp_point = []
    prcp_missing = []
    tmax_x = []
    tmax_y = []
    tmax_missing = []
    tmin_x = []
    tmin_y = []
    tmin_missing = []

    for i, record in enumerate(dataset):
        year, month, day, prcp, tmax, tmin = record

        if prcp == null:
            prcp_missing.append(i)
        else:
            prcp_point.append([i, prcp])

        if tmax == null:
            tmax_missing.append(i)
            tmax_x.append(i)
            tmax_y.append(None)
        else:
            #tmax_point.append([i, tmax])
            tmax_x.append(i)
            tmax_y.append(tmax)

        if tmin == null:
            tmin_missing.append(i)
            tmin_x.append(i)
            tmin_y.append(None)
        else:
            #tmin_point.append([i, tmin])
            tmin_x.append(i)
            tmin_y.append(tmin)

        #print(i, record)

    baseline_length = base_2 + 1 - base_1

    if baseline_length > 10:
        delta_year_tick = 5
    else:
        delta_year_tick = 2

    if baseline_length > 20:
        plot_aspect = (20, 50)
    elif baseline_length > 10:
        plot_aspect = (15, 35)
    else:
        #plot_aspect = (10, 25)
        plot_aspect = (1, 1)

    """
    year_tick_iters = (baseline_length // delta_year_tick) + 1
    major_x_ticks = [[0, base_1]]
    base_0 = int(base_1 / delta_year_tick) * delta_year_tick

    for i in range(1, year_tick_iters):
        year_ticks.append([None, base_0 + (i * delta_year_tick)]) 
    print(year_tick_iters, year_ticks)
    """

    fig, ax = plt.subplots()

    for prcp_x, prcp_y in prcp_point:
        plt.vlines(prcp_x, ymin=0, ymax=prcp_y, color='b', linewidth=0.5)

    for missing in prcp_missing:
        #ax.axvline(x=m, color='lightgrey', linewidth=0.5) #, zorder=0)
        plt.vlines(missing, ymin=0, ymax=100, color='darkgrey', linewidth=0.5)

    major_x_ticks = []
    major_x_labels = []
    minor_x_ticks = []
    leap = 0
    for i, year in enumerate(range(base_1, base_2 + 1)):
        if year == base_1 or (year % delta_year_tick) == 0:
            major_x_ticks.append((365 * i) + leap)
            major_x_labels.append(str(year))
        leap += leap_year(year)
        minor_x_ticks.append((365 * i) + leap)
        #print(year, leap_year(year), i, (365 * i) + leap)
    """
    print(minor_x_ticks)
    print(major_x_ticks)
    print(major_x_labels)
    """
    ax.tick_params(axis='x', labelsize=5)
    ax.tick_params(axis='y', labelsize=5)

    ax.set_xticks(minor_x_ticks, minor=True)
    ax.set_xticks(major_x_ticks, minor=False)

    ax.set_aspect(plot_aspect[0])

    ax.set_ylabel('Precipitation (mm)', fontsize=6)


    plt.xticks(major_x_ticks, major_x_labels)
    plt.yticks([0, 20, 40, 60, 80, 100])

    plt.title(
        f'{station} - {Station.instance()._name_state(station)} - PRCP ({base_1}-{base_2})', fontsize=6
    )

    #plt.show()

    fig.savefig(prcp_filename, bbox_inches='tight', dpi=300)

    plt.clf()
    plt.close()

    fig,ax = plt.subplots()
    """
    tmax_x = []
    tmax_y = []
    for x, y in tmax_point:
        tmax_x.append(x)
        tmax_y.append(y)
    """

    plt.plot(tmax_x, tmax_y, color='r', linewidth=0.25)
    plt.plot(tmin_x, tmin_y, color='b', linewidth=0.25)

    for missing in tmax_missing:
        #ax.axvline(x=m, color='lightgrey', linewidth=0.5) #, zorder=0)
        plt.vlines(missing, ymin=-10, ymax=50, color='darkgrey', linewidth=0.5)

    ax.tick_params(axis='x', labelsize=5)
    ax.tick_params(axis='y', labelsize=5)

    ax.set_xticks(minor_x_ticks, minor=True)
    ax.set_xticks(major_x_ticks, minor=False)

    ax.set_aspect(plot_aspect[1])

    ax.set_ylabel('Temperature ($^\circ$C)', fontsize=6)

    plt.xticks(major_x_ticks, major_x_labels)
    plt.yticks([-10, 0, 10, 20, 30, 40, 50])

    plt.title(
        f'{station} - {Station.instance()._name_state(station)} - TMAX,TMIN ({base_1}-{base_2})', fontsize=6
    )

    #plt.show()

    fig.savefig(temp_filename, bbox_inches='tight', dpi=300)

    plt.clf()
    plt.close()
