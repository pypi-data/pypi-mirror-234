
import datetime
import json
import math
import os

import matplotlib.pyplot as plt

#import scipy.stats as stats

import climex.stats as stats

from . config import Config
from . base import days_per_month, leap_year
from . station import Station



null = -99.9

missing_index_yearly_threshold = 50    # If missing days > threshold index, then value is nan
missing_index_monthly_threshold = 5

climdex_list = [
    'FD',    'SU',    'ID',      'TR',      'GSL',
    'TXX',   'TNX',   'TXN',     'TNN',     'TN10P',
    'TX10P', 'TN90P', 'TX90P',   'WSDI',    'CSDI',
    'DTR',   'ETR',   'RX1DAY',  'RX5DAY',  'SDII',
    'R10MM', 'R20MM', 'RNNMM',   'CDD',     'CWD',
    'R95P',  'R99P',  'R95PTOT', 'R99PTOT', 'PRCPTOT'
]


def _read_climdex_file(climdex_filename):

    climdex_data = []

    # TODO: error check
    
    with open(climdex_filename, 'rt') as climdex_file:
        climdex_records = climdex_file.readlines()

    for record in climdex_records:
        fields = record.split()

        year, month, day = map(int, fields[:3])
        prcp, tmax, tmin = map(float, fields[3:])

        climdex_data.append(
            [year, month, day, prcp, tmax, tmin]
        )

    return climdex_data


def info(index=None):
    """Prints information about climate indices"""

    if index is None:
        return climdex_list
    
    if index.upper() not in climdex_list:
        print(f'climex.info(): index "{index.upper()}" not found. Type climex.climdex_list for a complete list of indexes')
        return

    if index.upper() == 'FD':
        help_string = u'\nFD: Number of frost days\n\n'
        help_string += u'Annual count of days when TN (daily minimum temperature) < 0 \u00b0C. Let TNij be \n'
        help_string += u'daily minimum temperature on day i in year j. Count the number of days where \nTNij < 0\u00b0C.\n'
        print(help_string)
    elif index.upper() == 'SU':
        help_string = u'\nSU: Number of summer days\n\n'
        help_string += u'Annual count of days when TX (daily maximum temperature) > 25 \u00b0C. Let TXij be \n'
        help_string += u'daily minimum temperature on day i in year j. Count the number of days where \nTXij > 25\u00b0C.\n'
        print(help_string)
    elif index.upper() == 'ID':
        help_string = u'\nID: Number of icing days\n\n'
        help_string += u'Annual count of days when TX (daily maximum temperature) < 0 \u00b0C. Let TXij be\n'
        help_string += u'daily maximum temperature on day i in year j. Count the number of days where \nTXij < 0 \u00b0C.\n'
        print(help_string)
    elif index.upper() == 'TR':
        help_string = u'\nTR: Number of tropical nights\n\n'
        help_string += u'    Annual count of days when TN (daily minimum temperature) > 20 \u00b0C. Let TNij be \n'
        help_string += u'    daily minimum temperature on day i in year j. Count the number of days where \n'
        help_string += u'    TNij > 20\u00b0C.\n'
        print(help_string)
    elif index.upper() == 'GSL':
        help_string = u'\nGSL: Growing season length\n\n'
        help_string += u'Annual* count between the first span of at least 6 days with daily mean\n'
        help_string += u'temperature TG > 5 \u00b0C and the first span after July 1st (Jan 1st in SH)\n'
        help_string += u'of 6 days with TG < 5 \u00b0C.\n\n'
        help_string += u'Let TGij be daily mean temperature on day i in year j. Count the number of days\n'
        help_string += u'between the first occurrence of at least 6 consecutive days with TGij > 5 \u00b0C\n'
        help_string += u'and the first occurrence after 1st July (Jan 1st in SH) of at least 6\n'
        help_string += u'consecutive days with TGij < 5 \u00b0C.\n\n'
        help_string += u'* Annual means Jan 1st to Dec 31st in the Northern Hemisphere (NH); July 1st\n'
        help_string += u'to June 30th in the Southern Hemisphere (SH).\n'
        print(help_string)
    elif index.upper() == 'TXX':
        help_string = u'\nTXx: Maximum value of daily maximum temperature\n\n'
        help_string += u'Let TXx be the daily maximum temperatures in month k, period j. The maximum\n'
        help_string += u'daily maximum temperature each month is then TXxkj = max(TXxkj).\n'
        print(help_string)
    elif index.upper() == 'TNX':
        help_string = u'\nTNx: Maximum value of daily minimum temperature\n\n'
        help_string += u'    Let TNx be the daily minimum temperatures in month k, period j. The maximum\n'
        help_string += u'    daily minimum temperature each month is then TNxkj = max(TNxkj).\n'
        print(help_string)
    elif index.upper() == 'TXN':
        help_string = u'\nTXn: Minimum value of daily maximum temperature\n\n'
        help_string += u'    Let TXn be the daily maximum temperatures in month k, period j. The minimum\n'
        help_string += u'    daily maximum temperature each month is then TXnkj = min(TXnkj).\n'
        print(help_string)
    elif index.upper() == 'TNN':
        help_string = u'\nTNn: Minimum value of daily minimum temperature\n\n'
        help_string += u'    Let TNn be the daily minimum temperatures in month k, period j. The minimum\n'
        help_string += u'    daily minimum temperature each month is then TNnkj=min(TNnkj).\n'
        print(help_string)
    elif index.upper() == 'TN10P':
        help_string = u'\nTN10p: Percentage of days when TN < 10th percentile\n\n'
        help_string += u'Let TN_ij be the daily minimum temperature on day i in period j and let TN_in10 be\n'
        help_string += u'the calendar day 10th percentile centred on a 5-day window for the base period 1961-1990.\n'
        help_string += u'The percentage of time for the base period is determined where: TN_ij < TN_in10. To avoid possible\n'
        help_string += u'inhomogeneity across the in-base and out-base periods, the calculation for the base period (1961-1990)\n'
        help_string += u'requires the use of a bootstrap procedure. Details are described in https://doi.org/10.1175/JCLI3366.1.\n'
        print(help_string)
        print(f'climex.info(): index "{index.upper()}" not yet fully implemented') # -------------------------------------------- 
    elif index.upper() == 'TX10P':
        help_string = u'\nTX10p: Percentage of days when TX < 10th percentile\n\n'
        help_string += u'Let TXij be the daily maximum temperature on day i in period j and let TXin10 be the calendar day 10th\n'
        help_string += u'percentile centred on a 5-day window for the base period 1961-1990. The percentage of time for the\n'
        help_string += u'base period is determined where TXij < TXin10. To avoid possible inhomogeneity across the in-base and\n'
        help_string += u'out-base periods, the calculation for the base period (1961-1990) requires the use of a bootstrap\n'
        help_string += u'procedure. Details are described in https://doi.org/10.1175/JCLI3366.1.\n'
        print(help_string)
        print(f'climex.info(): index "{index.upper()}" not yet fully implemented') # --------------------------------------------
    elif index.upper() == 'TN90P':
        help_string = u'TN90p: Percentage of days when TN > 90th percentile\n\n'
        help_string += u'Let TNij be the daily minimum temperature on day i in period j and let TNin90 be the calendar day 90th\n'
        help_string += u'percentile centred on a 5-day window for the base period 1961-1990. The percentage of time for the\n'
        help_string += u'base period is determined where TNij > TNin90. To avoid possible inhomogeneity across the in-base and\n'
        help_string += u'out-base periods, the calculation for the base period (1961-1990) requires the use of a bootstrap\n'
        help_string += u'processure. Details are described in https://doi.org/10.1175/JCLI3366.1.\n'
        print(help_string)
        print(f'climex.info(): index "{index.upper()}" not yet fully implemented') # --------------------------------------------
    elif index.upper() == 'TX90P':
        help_string = u'\nTX90p: Percentage of days when TX > 90th percentile\n\n'
        help_string += u'Let TXij be the daily maximum temperature on day i in period j and let TXin90 be\n'
        help_string += u'the calendar day 90th percentile centred on a 5-day window for the base period 1961-1990.\n'
        help_string += u'The percentage of time for the base period is determined where TXij > TXin90. To avoid possible\n'
        help_string += u'inhomogeneity across the in-base and out-base periods, the calculation for the base period (1961-1990)\n'
        help_string += u'requires the use of a bootstrap procedure. Details are described in https://doi.org/10.1175/JCLI3366.1.\n'
        print(help_string)
        print(f'climex.info(): index "{index.upper()}" not yet fully implemented') # --------------------------------------------
    elif index.upper() == 'WSDI':
        help_string = u'\nWSDI: Warm spell duration index: annual count of days with at least 6 consecutive days when TX > 90th percentile\n\n'
        help_string += u'Let TXij be the daily maximum temperature on day i in period j and let TXin90 be the calendar day 90th percentile\n'
        help_string += u'centred on a 5-day window for the base period 1961-1990. Then the number of days per period is summed where,\n'
        help_string += u'in intervals of at least 6 consecutive days, TXij > TXin90.\n'
        print(help_string)
        print(f'climex.info(): index "{index.upper()}" not yet implemented') # --------------------------------------------
    elif index.upper() == 'CSDI':
        help_string = u'\nCSDI: Cold spell duration index: annual count of days with at least 6 consecutive days when TN < 10th percentile\n\n'
        help_string += u'Let TNij be the daily maximum temperature on day i in period j and let TNin10 be the calendar day 10th percentile\n'
        help_string += u'centred on a 5-day window for the base period 1961-1990. Then the number of days per period is summed where,\n'
        help_string += u'in intervals of at least 6 consecutive days, TNij < TNin10.\n'
        print(help_string)
        print(f'climex.info(): index "{index.upper()}" not yet implemented') # --------------------------------------------
    elif index.upper() == 'DTR':
        help_string = u'\nDTR: Daily temperature range\n\n'
        help_string += u'Let TXij and TNij be the daily maximum and minimum temperature respectively on day i\n'
        help_string += u'in period j. If I represents the number of days in j, then:\n\n'
        help_string += u'    DTRj = \sum_{i=1}^I (TXij - TNij) / I\n'
        print(help_string)
    elif index.upper() == 'ETR':
        help_string = u'\nETR: Extreme temperature range\n\n'
        help_string += u'Let TXx be the daily maximum temperature in month k and TNn the daily minimum temperature\n'
        help_string += u'in month k. The extreme temperature range each month is then:\n\n'
        help_string += u'   ETR_k =  TXx_k - TNn_k\n'
        print(help_string)
    elif index.upper() == 'RX1DAY':
        help_string = u'\nRx1day: Maximum 1-day precipitation\n\n'
        help_string += u'Let RRij be the daily precipitation amount on day i in period j. The maximum 1-day\n'
        help_string += u'value for period j are Rx1dayj = max (RRij).\n'
        print(help_string)
    elif index.upper() == 'RX5DAY':
        help_string = u'\nRx5day: Maximum consecutive 5-day precipitation\n\n'
        help_string += u'Let RRkj be the precipitation amount for the 5-day interval ending k, period j. Then\n'
        help_string += u'maximum 5-day values for period j are Rx5dayj = max (RRkj).\n'
        print(help_string)
    elif index.upper() == 'SDII':
        help_string = u'\nSDII: Simple precipitation intensity index\n\n'
        help_string += u'Let RRwj be the daily precipitation amount on wet days, with (RR ≥ 1mm) in period j. \n'
        help_string += u'If W represents number of wet days in j, then:\n\n'
        help_string += u'    SDII_j = \\frac{\sum_{w=1}^{W}RR_{wj}}{W}\n'
        print(help_string)
    elif index.upper() == 'R10MM':
        help_string = u'\nR10mm: Annual count of days when PRCP ≥ 10mm\n\n'
        help_string += u'Let RRij be the daily precipitation amount on day i in period j. Count the number of days\n'
        help_string += u'where RRij ≥ 10mm.\n'
        print(help_string)
    elif index.upper() == 'R20MM':
        help_string = u'\nR20mm: Annual count of days when PRCP ≥ 20mm\n\n'
        help_string += u'Let RRij be the daily precipitation amount on day i in period j. Count the number of days\n'
        help_string += u'where RRij ≥ 20mm.\n'
        print(help_string)
    elif index.upper() == 'RNNMM':
        help_string = u'\nRnnmm: Annual count of days when PRCP ≥ nn mm, where nn is a user-defined threshold\n\n'
        help_string += u'Let RRij be the daily precipitation amount on day i in period j. Count the number of days\n'
        help_string += u'where RRij ≥ nnmm.\n'
        print(help_string)
    elif index.upper() == 'CDD':
        help_string = u'\nCDD: Maximum length of dry spell: maximum number of consecutive days with RR < 1mm\n\n'
        help_string += u'Let RRij be the daily precipitation amount on day i in period j. Count the \n'
        help_string += u'largest number of consecutive days where RRij < 1mm.\n'
        print(help_string)
    elif index.upper() == 'CWD':
        help_string = u'\nCWD: Maximum length of wet spell: maximum number of consecutive days with RR ≥ 1mm\n\n'
        help_string += u'Let RRij be the daily precipitation amount on day i in period j. Count the \n'
        help_string += u'largest number of consecutive days where RRij ≥ 1mm.\n'
        print(help_string)
    elif index.upper() == 'R95P':
        help_string = u'\nR95p: Annual total PRCP when RR > 95th percentile\n\n'
        help_string += u'Let RR_wj be the daily precipitation amount on a wet day w (RR ≥ 1.0mm) in period i\n'
        help_string += u'and let RR_wn95 be the 95th percentile of precipitation on wet days in the 1961-1990\n'
        help_string += u'period. If W represents the number of wet days in the period, then:\n\n'
        help_string += u'    R95p = \sum_{w=1}^{W}RR_{wj}\n'
        help_string += u'\nwhere RR_wj > RR_wn95.\n'
        print(help_string)
    elif index.upper() == 'R99P':
        help_string = u'\nR99p: Annual total PRCP when RR > 99th percentile\n\n'
        help_string += u'Let RR_wj be the daily precipitation amount on a wet day w (RR ≥ 1.0mm) in period i\n'
        help_string += u'and let RR_wn99 be the 95th percentile of precipitation on wet days in the 1961-1990\n'
        help_string += u'period. If W represents the number of wet days in the period, then:\n\n'
        help_string += u'    R99p = \sum_{w=1}^{W}RR_{wj}\n'
        help_string += u'\nwhere RR_wj > RR_wn99.\n'
        print(help_string)
    elif index.upper() == 'R95PTOT':
        help_string = u'\nR95pTOT: Contribution to total precipitation from very wet days\n\n'
        help_string += u'    R95pTOT = 100 × R95p / RPTOT\n'
        print(help_string)
    elif index.upper() == 'R99PTOT':
        help_string = u'\nR99pTOT: Contribution to total precipitation from extremely wet days\n\n'
        help_string += u'    R99pTOT = 100 × R99p / RPTOT\n'
        print(help_string)
    elif index.upper() == 'PRCPTOT':
        help_string = u'\nPRCPTOT: Annual total precipitation on wet days\n\n'
        help_string += u'Let RRij be the daily precipitation in period j. If i represents the number\n'
        help_string += u'of days in j, then:\n\n    PRCPTOT_j = \sum_{i=1}^I RR_{ij}'
        print(help_string)


class Index():

    def __init__(self, project, index_list, plot):

        if index_list is None:
            index_list = climdex_list
        elif not isinstance(index_list, list):
            index_list = [index_list]

        self._project = project
        self._index_list = index_list
        self._plot = plot
        self._prcp_threshold = None

        #print(type(project))

    def _plot_annual_index(self, result):
        """Plots an annual climate index and some statistical parameters in a PNG file"""

        #print(f"_plot_annual_index {result['station']} {result['index']}")
        #print(result)

        base_1, base_2 = result['baseline']

        baseline_length = base_2 + 1 - base_1

        if baseline_length > 20:
            plot_aspect = 0.15
        elif baseline_length > 10:
            plot_aspect = 15
        else:
            plot_aspect = 10

        index_x = []
        index_y = []
        for key, value in result.items():
            if key in ('station', 'name', 'index', 'description', 'baseline', 'units'):
                continue

            if math.isnan(value['value']):
                continue

            index_x.append(int(key))
            index_y.append(float(value['value']))

        #print(index_x)
        #print(index_y)

        regression = stats.annual_regression_line(index_x, index_y)
        #regression = stats.linregress(index_x, index_y)

        if regression is None:
            return

        #print('regression')
        #print(regression)

        fig, ax = plt.subplots()

        # Version with home made function stats.regression
        try:
            ax.plot(
                [index_x[0] + 0.25, index_x[-1] - 0.25],
                [regression['a'] * (index_x[0] + 0.25) + regression['b'], regression['a'] * (index_x[-1] - 0.25) + regression['b']],
                color='blue',
                linewidth=0.8,
                zorder=0
            )
        except:
            pass
        
        """
        # Version with scipy.stats
        ax.plot(
            [index_x[0] + 0.25, index_x[-1] - 0.25],
            [regression.slope * (index_x[0] + 0.25) + regression.intercept, regression.slope * (index_x[-1] - 0.25) + regression.intercept],
            color='blue',
            linewidth=0.8,
            zorder=0
        )
        """
        ax.plot(index_x, index_y, color='silver', linewidth=0.8, zorder=1)
        ax.scatter(index_x, index_y, color='black', marker='s', s=3, zorder=2)

        ax.tick_params(axis='x', labelsize=9)
        ax.tick_params(axis='y', labelsize=9)

        #ax.set_aspect(plot_aspect)

        ax.set_ylabel(result['units'], fontsize=9)

        plt.title(
            f"{result['station']} - {result['name']} - ({base_1}-{base_2})\n {result['description']} ",
            fontsize=10
        )

        #plt.show()

        #print(f"00_{result['index']}")

        try:
            index_number = (climdex_list.index(result['index'])) + 1
        except:
            #print(f"01_{result['index']}")
            #print(result['index'][0], result['index'][-2:])
            if result['index'][0].upper() == 'R' and result['index'][-2:].upper() == 'MM':
                #print(f"02_{result['index']}")
                index_number = (climdex_list.index('RNNMM')) + 1
                """
                try:
                    #prcp_threshold = float(index[1:-2])
                    index_number = (climdex_list.index('RNNMM')) + 1
                except:
                    return
                """
        #print(f"{index_number}_{result['index']}")

        plot_filename = os.path.join(
            self._project._project_dir, 'INDEX',
            f"{str(result['station'])}_{base_1:04d}_{base_2:04d}_{index_number:02d}_{result['index']}.png"
        )


        try:
            if not math.isnan(regression['p-value']):
                x_label = f"\nLinear trend slope = {regression['a']:.3f}      Slope error = {regression['error']:.3f}      p-value = {regression['p-value']:.3f}"
            else:
                x_label = f"\nLinear trend slope = {regression['a']:.3f}      Slope error = {regression['error']:.3f}"

            ax.set_xlabel(x_label, fontsize=8)
        except:
            pass
        
        fig.savefig(plot_filename, bbox_inches='tight', dpi=300)

        plt.clf()
        plt.close()

    def _get_spells(self, days):
        """Given a list of days (in day-of-year format) returns spells, i.e. groups of consecutive days"""

        all_spells = []
        current_spell = []

        for i in range(1, len(days)):
            difference = days[i] - days[i - 1]

            if difference == 1:
                in_spell = True
            else:
                in_spell = False

            if in_spell:
                if len(current_spell) == 0:
                    current_spell.append(days[i - 1])
                current_spell.append(days[i])
            else:
                if len(current_spell) > 0:
                    all_spells.append(current_spell)
                current_spell = []

        if len(current_spell) > 0:
            all_spells.append(current_spell)
            current_spell = []

        return all_spells

    def _prcp_percentiles(self, station):

        #print('Index._prcp_percentiles()')
        percentile_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_1961_1990_00_PRCP_percentiles.json')
        #print(percentile_filename)

        prcp_percentiles = {}
        """
        try:
            with open(percentile_filename, 'rt') as percentile_file:
                prcp_percentiles = json.load(percentile_file)
            #print('percentile file exists')
        except:
            #print('NO_%_FILENAME')
            dataset = self._project._get_dataset(station, baseline=[1961, 1990])
            #print('Percentiles')
            #print(dataset[0])
            #print(dataset[-1])
            stats.prcp_percentiles(station, dataset, self._project.baseline, percentile_filename)
        """

        if not os.path.isfile(percentile_filename):
            dataset = self._project._get_dataset(station, baseline=[1961, 1990])
            if dataset is None:
                old_baseline = self._project.baseline
                self._project.baseline = [1961, 1990]
                # if not exist CONAGUA file download()
                self._project.download()
                self._project.qc()
                self._project.baseline = old_baseline
                dataset = self._project._get_dataset(station, baseline=[1961, 1990])

            #stats.prcp_percentiles(station, dataset, self._project.baseline, percentile_filename)
            stats.prcp_percentiles(station, dataset, [1961, 1990], percentile_filename)




        #return


        """
        if len(prcp_percentiles) == 0:
            try:
                with open(percentile_filename, 'wt') as percentile_file:
                    prcp_percentiles = json.dump(percentile_file)
            except:
                pass

        return prcp_percentiles
        """

    def _temp_percentiles(self, station):

        tmax_by_day_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_1961_1990_00_TMAX_day.json')
        tmin_by_day_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_1961_1990_00_TMIN_day.json')

        dataset = self._project._get_dataset(station, baseline=[1961, 1990])

        if dataset is None:
            return

        tmax_dataset_by_day = {}
        tmin_dataset_by_day = {}
        for month, days in days_per_month.items():
            for day in range(1, days + 1):
                tmax_dataset_by_day[f'{month:02d}-{day:02d}'] = []
                tmin_dataset_by_day[f'{month:02d}-{day:02d}'] = []
            if month == 2:
                tmax_dataset_by_day[f'{month:02d}-29'] = []
                tmin_dataset_by_day[f'{month:02d}-29'] = []


        print(f'Computing TEMP percentiles on station "{station}"', end='')

        for record in dataset:
            year, month, day, prcp, tmax, tmin = record

            day_of_year = f'{month:02d}-{day:02d}'

            if tmax != null:
                tmax_dataset_by_day[day_of_year].append(tmax)

            if tmin != null:
                tmin_dataset_by_day[day_of_year].append(tmin)

        with open(tmax_by_day_filename, 'wt') as tmax_by_day_file:
            json.dump(tmax_dataset_by_day, tmax_by_day_file, indent=4)

        with open(tmin_by_day_filename, 'wt') as tmin_by_day_file:
            json.dump(tmin_dataset_by_day, tmin_by_day_file, indent=4)


        tmax_by_window_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_1961_1990_00_TMAX_window.json')
        tmin_by_window_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_1961_1990_00_TMIN_window.json')

        tmax_dataset_by_window = {}
        tmin_dataset_by_window = {}
        for month, days in days_per_month.items():
            for day in range(1, days + 1):
                tmax_dataset_by_window[f'{month:02d}-{day:02d}'] = []
                tmin_dataset_by_window[f'{month:02d}-{day:02d}'] = []
            if month == 2:
                tmax_dataset_by_window[f'{month:02d}-29'] = []
                tmin_dataset_by_window[f'{month:02d}-29'] = []

        calendar_days = sorted(tmax_dataset_by_window.keys())
        number_of_calendar_days = len(calendar_days)

        for i, day in enumerate(calendar_days):
            for j in [-2, -1, 0, 1, 2]:
                k = i + j
                if k >= 0 and k < number_of_calendar_days:
                    #print(k, calendar_days[k])
                    tmax_dataset_by_window[day] += tmax_dataset_by_day[calendar_days[k]]
                    tmin_dataset_by_window[day] += tmin_dataset_by_day[calendar_days[k]]

        with open(tmax_by_window_filename, 'wt') as tmax_by_window_file:
            json.dump(tmax_dataset_by_window, tmax_by_window_file, indent=4)

        with open(tmin_by_window_filename, 'wt') as tmin_by_window_file:
            json.dump(tmin_dataset_by_window, tmin_by_window_file, indent=4)


        tmax_percentile_by_window_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_1961_1990_00_TMAX_window_percentile.json')
        tmin_percentile_by_window_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_1961_1990_00_TMIN_window_percentile.json')

        tmax_percentile_by_window = {}
        tmin_percentile_by_window = {}
        for month, days in days_per_month.items():
            for day in range(1, days + 1):
                tmax_percentile_by_window[f'{month:02d}-{day:02d}'] = {'10': math.nan, '90': math.nan}
                tmin_percentile_by_window[f'{month:02d}-{day:02d}'] = {'10': math.nan, '90': math.nan}
            if month == 2:
                tmax_percentile_by_window[f'{month:02d}-29'] = {'10': math.nan, '90': math.nan}
                tmin_percentile_by_window[f'{month:02d}-29'] = {'10': math.nan, '90': math.nan}


        for day, data in tmax_dataset_by_window.items():
            tmax_percentile_by_window[day]['10'] = stats.percentile(data, 10)
            tmax_percentile_by_window[day]['90'] = stats.percentile(data, 90)

        with open(tmax_percentile_by_window_filename, 'wt') as tmax_percentile_by_window_file:
            json.dump(tmax_percentile_by_window, tmax_percentile_by_window_file, indent=4)

        for day, data in tmin_dataset_by_window.items():
            tmin_percentile_by_window[day]['10'] = stats.percentile(data, 10)
            tmin_percentile_by_window[day]['90'] = stats.percentile(data, 90)

        with open(tmin_percentile_by_window_filename, 'wt') as tmin_percentile_by_window_file:
            json.dump(tmin_percentile_by_window, tmin_percentile_by_window_file, indent=4)

        print('\t[OK]')

    def index_batch(self):
        """Batch computation of climate indexes for current project"""

        """
        prcp_percentiles = False
        for index in self._index_list:
            if index.upper() in ('R95P', 'R99P', 'R95PTOT', 'R99PTOT'):
                prcp_percentiles = True
                # Check climdex reference files 1961-1990 exists, if it doesn't, then call qc()               
                for station in self._project.stations:
                    climdex_ref_filename = os.path.join(self._project._project_dir, 'QC', f'{str(station)}_1961_1990.txt')
                    try:
                        #print(climdex_ref_filename)
                        with open(climdex_ref_filename, 'rt') as climdex_ref_file:
                            pass
                    except:
                        old_baseline = self._project.baseline
                        self._project.baseline = [1961, 1990]
                        self._project.qc()
                        self._project.baseline = old_baseline
                        break
                else: # https://stackoverflow.com/questions/653509/breaking-out-of-nested-loops
                    continue
            break



        if prcp_percentiles:
            for station in self._project.stations:

                self._prcp_percentiles(station)
                # Compute percentiles
                #print('compute percentiles')
                #dataset = self._project._get_dataset(station)
                #print(dataset[0])

        """



        for station in self._project.stations:
            climdex_ref_filename = os.path.join(self._project._project_dir, 'CLIMDEX', f'{str(station)}_1961_1990.txt')
            #print(climdex_ref_filename)

            try:
                #print(climdex_ref_filename)
                with open(climdex_ref_filename, 'rt') as climdex_ref_file:
                    pass
            except:
                #print('NO_FILENAME')
                old_baseline = self._project.baseline
                self._project.baseline = [1961, 1990]
                self._project.qc()
                self._project.baseline = old_baseline

        for station in self._project.stations:
            #self._prcp_percentiles(station)
            pass ####################################################################################################

        for station in self._project.stations:
            #self._temp_percentiles(station)
             pass

        #return


        #prcp_threshold = None

        for station in self._project.stations:

            dataset = self._project._get_dataset(station)

            if dataset is None:
                continue

            for index in self._index_list:
                index_ok = True
                if index.upper() not in climdex_list:
                    if index[0].upper() == 'R' and index[-2:].upper() == 'MM':
                        try:
                            self._prcp_threshold = float(index[1:-2])
                            index = 'rnnmm'
                        except:
                            index_ok = False
                    else:
                        index_ok = False

                if not index_ok:
                    print(f'climex.Index.index_batch(): index "{index.upper()}" not found. Type climex.climdex_list for a complete list of indexes')
                    continue

                if index.upper() == 'FD':
                    self._index_01_fd(station, dataset)
                elif index.upper() == 'SU':
                    self._index_02_su(station, dataset)
                elif index.upper() == 'ID':
                    self._index_03_id(station, dataset)
                elif index.upper() == 'TR':
                    self._index_04_tr(station, dataset)
                elif index.upper() == 'GSL':
                    self._index_05_gsl(station, dataset)
                elif index.upper() == 'TXX':
                    self._index_06_txx(station, dataset)
                elif index.upper() == 'TNX':
                    self._index_07_tnx(station, dataset)
                elif index.upper() == 'TXN':
                    self._index_08_txn(station, dataset)
                elif index.upper() == 'TNN':
                    self._index_09_tnn(station, dataset)
                elif index.upper() == 'TN10P':
                    self._index_10_tn10p(station, dataset)
                elif index.upper() == 'TX10P':
                    self._index_11_tx10p(station, dataset)
                elif index.upper() == 'TN90P':
                    self._index_12_tn90p(station, dataset)
                elif index.upper() == 'TX90P':
                    self._index_13_tx90p(station, dataset)
                elif index.upper() == 'WSDI':
                    self._index_14_wsdi(station, dataset)
                elif index.upper() == 'CSDI':
                    self._index_15_csdi(station, dataset)
                elif index.upper() == 'DTR':
                    self._index_16_dtr(station, dataset)
                elif index.upper() == 'ETR':
                    self._index_17_etr(station, dataset)
                elif index.upper() == 'RX1DAY':
                    self._index_18_rx1day(station, dataset)
                elif index.upper() == 'RX5DAY':
                    self._index_19_rx5day(station, dataset)
                elif index.upper() == 'SDII':
                    self._index_20_sdii(station, dataset)
                elif index.upper() == 'R10MM':
                    self._index_21_r10mm(station, dataset)
                elif index.upper() == 'R20MM':
                    self._index_22_r20mm(station, dataset)
                elif index.upper() == 'RNNMM':
                    self._index_23_rnnmm(station, dataset) #, prcp_threshold)
                elif index.upper() == 'CDD':
                    self._index_24_cdd(station, dataset)
                elif index.upper() == 'CWD':
                    self._index_25_cwd(station, dataset)
                elif index.upper() == 'R95P':
                    self._index_26_r95p(station, dataset)
                elif index.upper() == 'R99P':
                    self._index_27_r99p(station, dataset)
                elif index.upper() == 'R95PTOT':
                    self._index_28_r95ptot(station, dataset)
                elif index.upper() == 'R99PTOT':
                    self._index_29_r99ptot(station, dataset)
                elif index.upper() == 'PRCPTOT':
                    self._index_30_prcptot(station, dataset)

            #break


    def _index_01_fd(self, station, dataset):

        print(f'Computing index "FD" on station "{station}"', end='')

        base_1, base_2 = self._project.baseline

        result = {
            'station': station,
            'name': Station.instance()._name_state(station),
            'index': 'FD',
            'description': 'FD: Number of frost days',
            'baseline': self._project.baseline,
            'units': 'Number of days (count)'
        }

        for year in range(base_1, base_2 + 1):
            result[f'{year:04d}'] = {
                'value': 0, 'count': 0, 'missing': 0,
                '01': 0, '02': 0, '03': 0, '04': 0,
                '05': 0, '06': 0, '07': 0, '08': 0,
                '09': 0, '10': 0, '11': 0, '12': 0
            }

        for record in dataset:
            fields = record

            year = fields[0]
            month = fields[1]
            day = fields[2]

            tmin = float(fields[5])

            if tmin == null:
                result[f'{year:04d}']['missing'] += 1
            elif tmin < 0.0:
                result[f'{year:04d}']['count'] += 1
                result[f'{year:04d}'][f'{month:02d}'] += 1

        for year in range(base_1, base_2 + 1):
            if result[f'{year:04d}']['missing'] < missing_index_yearly_threshold:
                result[f'{year:04d}']['value'] = result[f'{year:04d}']['count']
            else:
                result[f'{year:04d}']['value'] = math.nan

        index_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_{base_1:04d}_{base_2:04d}_01_FD.json')

        with open(index_filename, 'wt') as index_file:
            json.dump(result, index_file, indent=4)
           
        if self._plot:
            self._plot_annual_index(result)

        print('\t\t[OK]')


    def _index_02_su(self, station, dataset):

        print(f'Computing index "SU" on station "{station}"', end='')

        base_1, base_2 = self._project.baseline
        
        result = {
            'station': station,
            'name': Station.instance()._name_state(station),
            'index': 'SU',
            'description': 'SU: Number of summer days',
            'baseline': self._project.baseline,
            'units': 'Number of days (count)'
        }

        for year in range(base_1, base_2 + 1):
            result[f'{year:04d}'] = {
                'value': 0, 'count': 0, 'missing': 0,
                '01': 0, '02': 0, '03': 0, '04': 0,
                '05': 0, '06': 0, '07': 0, '08': 0,
                '09': 0, '10': 0, '11': 0, '12': 0
            }

        for record in dataset:
            fields = record

            year = fields[0]
            month = fields[1]
            day = fields[2]

            tmax = float(fields[4])

            if tmax == null:
                result[f'{year:04d}']['missing'] += 1
            elif tmax > 25.0:
                result[f'{year:04d}']['count'] += 1
                result[f'{year:04d}'][f'{month:02d}'] += 1

        for year in range(base_1, base_2 + 1):
            if result[f'{year:04d}']['missing'] < missing_index_yearly_threshold:
                result[f'{year:04d}']['value'] = result[f'{year:04d}']['count']
            else:
                result[f'{year:04d}']['value'] = math.nan

        index_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_{base_1:04d}_{base_2:04d}_02_SU.json')
        #print(index_filename)
        with open(index_filename, 'wt') as index_file:
            json.dump(result, index_file, indent=4)
           
        if self._plot:
            self._plot_annual_index(result)

        print('\t\t[OK]')

        #print(result)


    def _index_03_id(self, station, dataset):

        print(f'Computing index "ID" on station "{station}"', end='')

        base_1, base_2 = self._project.baseline
        
        result = {
            'station': station,
            'name': Station.instance()._name_state(station),
            'index': 'ID',
            'description': 'ID: Number of icing days',
            'baseline': self._project.baseline,
            'units': 'Number of days (count)'
        }

        for year in range(base_1, base_2 + 1):
            result[f'{year:04d}'] = {
                'value': 0, 'count': 0, 'missing': 0,
                '01': 0, '02': 0, '03': 0, '04': 0,
                '05': 0, '06': 0, '07': 0, '08': 0,
                '09': 0, '10': 0, '11': 0, '12': 0
            }

        for record in dataset:
            fields = record

            year = fields[0]
            month = fields[1]
            day = fields[2]

            tmax = float(fields[4])

            if tmax == null:
                result[f'{year:04d}']['missing'] += 1
            elif tmax < 0.0:
                result[f'{year:04d}']['count'] += 1
                result[f'{year:04d}'][f'{month:02d}'] += 1

        for year in range(base_1, base_2 + 1):
            if result[f'{year:04d}']['missing'] < missing_index_yearly_threshold:
                result[f'{year:04d}']['value'] = result[f'{year:04d}']['count']
            else:
                result[f'{year:04d}']['value'] = math.nan

        index_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_{base_1:04d}_{base_2:04d}_03_ID.json')

        with open(index_filename, 'wt') as index_file:
            json.dump(result, index_file, indent=4)
           
        if self._plot:
            self._plot_annual_index(result)

        print('\t\t[OK]')


    def _index_04_tr(self, station, dataset):

        print(f'Computing index "TR" on station "{station}"', end='')

        base_1, base_2 = self._project.baseline

        result = {
            'station': station,
            'name': Station.instance()._name_state(station),
            'index': 'TR',
            'description': 'TR: Number of icing days',
            'baseline': self._project.baseline,
            'units': 'Number of nights (count)'
        }

        for year in range(base_1, base_2 + 1):
            result[f'{year:04d}'] = {
                'value': 0, 'missing': 0,                # count ########################################################
                '01': 0, '02': 0, '03': 0, '04': 0,
                '05': 0, '06': 0, '07': 0, '08': 0,
                '09': 0, '10': 0, '11': 0, '12': 0
            }

        for record in dataset:
            fields = record

            year = fields[0]
            month = fields[1]
            day = fields[2]

            tmin = float(fields[5])

            if tmin == null:
                result[f'{year:04d}']['missing'] += 1
            elif tmin > 20.0:
                result[f'{year:04d}']['value'] += 1
                result[f'{year:04d}'][f'{month:02d}'] += 1

        index_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_{base_1:04d}_{base_2:04d}_04_TR.json')

        with open(index_filename, 'wt') as index_file:
            json.dump(result, index_file, indent=4)

        if self._plot:
            self._plot_annual_index(result)

        print('\t\t[OK]')


    def _index_05_gsl(self, station, dataset, span=6):

        if span not in (5, 6):
            print('climex.Index.compute_index(): span size must be 5 or 6 in GSL index')
            return

        print(f'Computing index "GSL" on station "{station}"', end='')

        base_1, base_2 = self._project.baseline

        result = {
            'station': station,
            'name': Station.instance()._name_state(station),
            'index': 'GSL',
            'description': 'GSL: Growing season length',
            'baseline': self._project.baseline,
            'units': 'Growing season length (days)'
        }

        for year in range(base_1, base_2 + 1):
            result[f'{year:04d}'] = {
                'value': 0, 'count': 0, 'missing': 0,
                'span_start': None, 'span_end': None,
                'span_start_dataset': [], 'span_end_dataset': []
            }

        dataset_by_year = {}
        for record in dataset:
            fields = record
            year = fields[0]

            try:
                dataset_by_year[year].append(record)
            except:
                dataset_by_year[year] = [record]

        for year in range(base_1, base_2 + 1):

            for i in range(len(dataset_by_year[year])):

                segment = dataset_by_year[year][i:i + span]
                fields = segment[0]

                year = fields[0]
                month = fields[1]
                day = fields[2]

                if month >= 7:
                    break

                tmax = float(fields[4])
                tmin = float(fields[5])

                if tmax == null or tmin == null:
                    result[f'{year:04d}']['missing'] += 1
                    continue

                try:
                    year, month, day = segment[0][:3]

                    tmax_1, tmin_1 = segment[0][4:]
                    if tmax_1 == null or tmin_1 == null:
                        continue

                    tmax_2, tmin_2 = segment[1][4:]
                    if tmax_2 == null or tmin_2 == null:
                        continue

                    tmax_3, tmin_3 = segment[2][4:]
                    if tmax_3 == null or tmin_3 == null:
                        continue

                    tmax_4, tmin_4 = segment[3][4:]
                    if tmax_4 == null or tmin_4 == null:
                        continue

                    tmax_5, tmin_5 = segment[4][4:]
                    if tmax_5 == null or tmin_5 == null:
                        continue

                    if span == 6:
                        tmax_6, tmin_6 = segment[5][4:]
                        if tmax_6 == null or tmin_6 == null:
                            continue

                    tavg_span = 0.0
                    tavg_span += (tmax_1 + tmin_1) / 2
                    tavg_span += (tmax_2 + tmin_2) / 2
                    tavg_span += (tmax_3 + tmin_3) / 2
                    tavg_span += (tmax_4 + tmin_4) / 2
                    tavg_span += (tmax_5 + tmin_5) / 2

                    if span == 6:
                        tavg_span += (tmax_6 + tmin_6) / 2

                    tavg_span /= span

                    if tavg_span > 5.0:
                        result[f'{year:04d}']['span_start'] = f"{year:04d}-{month:02d}-{day:02d}"
                        result[f'{year:04d}']['span_start_dataset'] = segment
                        break
                except:
                    continue

            for i in range(len(dataset_by_year[year])):

                segment = dataset_by_year[year][i:i + span]
                fields = segment[0]

                year = fields[0]
                month = fields[1]
                day = fields[2]

                if month < 7:
                    continue
                
                tmax = float(fields[4])
                tmin = float(fields[5])

                if tmax == null or tmin == null:
                    result[f'{year:04d}']['missing'] += 1
                    continue

                try:
                    year, month, day = segment[0][:3]

                    tmax_1, tmin_1 = segment[0][4:]
                    if tmax_1 == null or tmin_1 == null:
                        continue

                    tmax_2, tmin_2 = segment[1][4:]
                    if tmax_2 == null or tmin_2 == null:
                        continue

                    tmax_3, tmin_3 = segment[2][4:]
                    if tmax_3 == null or tmin_3 == null:
                        continue

                    tmax_4, tmin_4 = segment[3][4:]
                    if tmax_4 == null or tmin_4 == null:
                        continue

                    tmax_5, tmin_5 = segment[4][4:]
                    if tmax_5 == null or tmin_5 == null:
                        continue

                    if span == 6:
                        tmax_6, tmin_6 = segment[5][4:]
                        if tmax_6 == null or tmin_6 == null:
                            continue

                    tavg_span = 0.0
                    tavg_span += (tmax_1 + tmin_1) / 2
                    tavg_span += (tmax_2 + tmin_2) / 2
                    tavg_span += (tmax_3 + tmin_3) / 2
                    tavg_span += (tmax_4 + tmin_4) / 2
                    tavg_span += (tmax_5 + tmin_5) / 2

                    if span == 6:
                        tavg_span += (tmax_6 + tmin_6) / 2

                    tavg_span /= span

                    if tavg_span < 5.0:
                        result[f'{year:04d}']['span_end'] = f"{year:04d}-{month:02d}-{day:02d}"
                        result[f'{year:04d}']['span_end_dataset'] = segment
                        break
                except:
                    continue


            if result[f'{year:04d}']['span_start'] is None or result[f'{year:04d}']['span_end'] is None:
                result[f'{year:04d}']['count'] = math.nan
                result[f'{year:04d}']['value'] = math.nan
                continue
            else:
                start = datetime.datetime.strptime(result[f'{year:04d}']['span_start'], '%Y-%m-%d').timetuple().tm_yday
                end = datetime.datetime.strptime(result[f'{year:04d}']['span_end'], '%Y-%m-%d').timetuple().tm_yday
                result[f'{year:04d}']['count'] = end - start

            if result[f'{year:04d}']['missing'] > missing_index_yearly_threshold:
                result[f'{year:04d}']['value'] = math.nan
            else:
                result[f'{year:04d}']['value'] = result[f'{year:04d}']['count']

        index_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_{base_1:04d}_{base_2:04d}_05_GSL.json')

        with open(index_filename, 'wt') as index_file:
            json.dump(result, index_file, indent=4)

        if self._plot:
            self._plot_annual_index(result)

        print('\t[OK]')


    def _index_06_txx(self, station, dataset):

        print(f'Computing index "TXx" on station "{station}"', end='')

        base_1, base_2 = self._project.baseline
        
        result = {
            'station': station,
            'name': Station.instance()._name_state(station),
            'index': 'TXX',
            'description': 'TXx: Maximum value of daily maximum temperature',
            'baseline': self._project.baseline,
            'units': 'Temperature (\u00b0C)'
        }
        for year in range(base_1, base_2 + 1):
            result[f'{year:04d}'] = {
                'value': null, 'missing': 0,                # count ########################################################
                '01': null, '02': null, '03': null, '04': null,
                '05': null, '06': null, '07': null, '08': null,
                '09': null, '10': null, '11': null, '12': null
            }

        for record in dataset:
            fields = record

            year = fields[0]
            month = fields[1]
            day = fields[2]

            tmax = float(fields[4])

            if tmax == null:
                result[f'{year:04d}']['missing'] += 1
            else:
                if tmax > result[f'{year:04d}']['value']:
                    result[f'{year:04d}']['value'] = tmax
                if tmax > result[f'{year:04d}'][f'{month:02d}']:
                    result[f'{year:04d}'][f'{month:02d}'] = tmax

        index_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_{base_1:04d}_{base_2:04d}_06_TXX.json')

        with open(index_filename, 'wt') as index_file:
            json.dump(result, index_file, indent=4)

        if self._plot:
            self._plot_annual_index(result)

        print('\t[OK]')


    def _index_07_tnx(self, station, dataset):

        print(f'Computing index "TNx" on station "{station}"', end='')

        base_1, base_2 = self._project.baseline
        
        result = {
            'station': station,
            'name': Station.instance()._name_state(station),
            'index': 'TNX',
            'description': 'TNx: Maximum value of daily minimum temperature',
            'baseline': self._project.baseline,
            'units': 'Temperature (\u00b0C)'
        }
        for year in range(base_1, base_2 + 1):
            result[f'{year:04d}'] = {
                'value': null, 'missing': 0,                # count ########################################################
                '01': null, '02': null, '03': null, '04': null,
                '05': null, '06': null, '07': null, '08': null,
                '09': null, '10': null, '11': null, '12': null
            }

        for record in dataset:
            fields = record

            year = fields[0]
            month = fields[1]
            day = fields[2]

            tmin = float(fields[5])

            if tmin == -99.9:
                result[f'{year:04d}']['missing'] += 1
            else:
                if tmin > result[f'{year:04d}']['value']:
                    result[f'{year:04d}']['value'] = tmin
                if tmin > result[f'{year:04d}'][f'{month:02d}']:
                    result[f'{year:04d}'][f'{month:02d}'] = tmin

        index_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_{base_1:04d}_{base_2:04d}_07_TNX.json')

        with open(index_filename, 'wt') as index_file:
            json.dump(result, index_file, indent=4)

        if self._plot:
            self._plot_annual_index(result)

        print('\t[OK]')


    def _index_08_txn(self, station, dataset):

        print(f'Computing index "TXn" on station "{station}"', end='')

        base_1, base_2 = self._project.baseline
        
        result = {
            'station': station,
            'name': Station.instance()._name_state(station),
            'index': 'TXN',
            'description': 'TXn: Minimum value of daily maximum temperature',
            'baseline': self._project.baseline,
            'units': 'Temperature (\u00b0C)'
        }
        for year in range(base_1, base_2 + 1):
            result[f'{year:04d}'] = {
                'value': -null, 'missing': 0,                # count ########################################################
                '01': -null, '02': -null, '03': -null, '04': -null,
                '05': -null, '06': -null, '07': -null, '08': -null,
                '09': -null, '10': -null, '11': -null, '12': -null
            }

        for record in dataset:
            fields = record

            year = fields[0]
            month = fields[1]
            day = fields[2]

            tmax = float(fields[4])

            if tmax == -99.9:
                result[f'{year:04d}']['missing'] += 1
            else:
                if tmax < result[f'{year:04d}']['value']:
                    result[f'{year:04d}']['value'] = tmax
                if tmax < result[f'{year:04d}'][f'{month:02d}']:
                    result[f'{year:04d}'][f'{month:02d}'] = tmax

        index_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_{base_1:04d}_{base_2:04d}_08_TXN.json')

        with open(index_filename, 'wt') as index_file:
            json.dump(result, index_file, indent=4)

        if self._plot:
            self._plot_annual_index(result)

        print('\t[OK]')


    def _index_09_tnn(self, station, dataset):

        print(f'Computing index "TNn" on station "{station}"', end='')

        base_1, base_2 = self._project.baseline
        
        result = {
            'station': station,
            'name': Station.instance()._name_state(station),
            'index': 'TNN',
            'description': 'TNn: Minimum value of daily minimum temperature',
            'baseline': self._project.baseline,
            'units': 'Temperature (\u00b0C)'
        }
        for year in range(base_1, base_2 + 1):
            result[f'{year:04d}'] = {
                'value': -null, 'missing': 0,                # count ########################################################
                '01': -null, '02': -null, '03': -null, '04': -null,
                '05': -null, '06': -null, '07': -null, '08': -null,
                '09': -null, '10': -null, '11': -null, '12': -null
            }

        for record in dataset:
            fields = record

            year = fields[0]
            month = fields[1]
            day = fields[2]

            tmin = float(fields[5])

            if tmin == -99.9:
                result[f'{year:04d}']['missing'] += 1
            else:
                if tmin < result[f'{year:04d}']['value']:
                    result[f'{year:04d}']['value'] = tmin
                if tmin < result[f'{year:04d}'][f'{month:02d}']:
                    result[f'{year:04d}'][f'{month:02d}'] = tmin

        index_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_{base_1:04d}_{base_2:04d}_09_TNN.json')

        with open(index_filename, 'wt') as index_file:
            json.dump(result, index_file, indent=4)

        if self._plot:
            self._plot_annual_index(result)

        print('\t[OK]')


    def _index_10_tn10p(self, station, dataset):

        print(f'Computing index "TN10p" on station "{station}"', end='')

        tmin_percentile_by_window_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_1961_1990_00_TMIN_window_percentile.json')

        if not os.path.isfile(tmin_percentile_by_window_filename):
            print(f'climex.Index.compute_index(): index TN10p cannot be computed (percentile file not found)')
            return

        with open(tmin_percentile_by_window_filename, 'rt') as tmin_percentile_by_window_file:
            tmin_percentile_by_window = json.load(tmin_percentile_by_window_file)

        base_1, base_2 = self._project.baseline
        
        result = {
            'station': station,
            'name': Station.instance()._name_state(station),
            'index': 'TN10P',
            'description': 'TN10p: Percentage of days when TN < 10th percentile',
            'baseline': self._project.baseline,
            'units': u'Percentage of days (%)'
        }

        for year in range(base_1, base_2 + 1):
            result[f'{year:04d}'] = {
                'value': math.nan, 'count': 0, 'missing': 0,
                '01': {'value': math.nan, 'count': 0, 'missing': 0},
                '02': {'value': math.nan, 'count': 0, 'missing': 0},
                '03': {'value': math.nan, 'count': 0, 'missing': 0},
                '04': {'value': math.nan, 'count': 0, 'missing': 0},
                '05': {'value': math.nan, 'count': 0, 'missing': 0},
                '06': {'value': math.nan, 'count': 0, 'missing': 0},
                '07': {'value': math.nan, 'count': 0, 'missing': 0},
                '08': {'value': math.nan, 'count': 0, 'missing': 0},
                '09': {'value': math.nan, 'count': 0, 'missing': 0},
                '10': {'value': math.nan, 'count': 0, 'missing': 0},
                '11': {'value': math.nan, 'count': 0, 'missing': 0},
                '12': {'value': math.nan, 'count': 0, 'missing': 0}
            }

        for record in dataset:
            fields = record

            year = fields[0]
            month = fields[1]
            day = fields[2]

            tmin = fields[5]

            if tmin == null:
                result[f'{year:04d}']['missing'] += 1
                result[f'{year:04d}'][f'{month:02d}']['missing'] += 1
            else:
                day_of_year = f'{month:02d}-{day:02d}'
                percentile_10 = tmin_percentile_by_window[day_of_year]['10']
                if tmin < percentile_10:
                    result[f'{year:04d}']['count'] += 1
                    result[f'{year:04d}'][f'{month:02d}']['count'] += 1

        for year in range(base_1, base_2 + 1):
            leap_day = leap_year(year)
            if result[f'{year:04d}']['missing'] < missing_index_yearly_threshold:
                result[f'{year:04d}']['value'] = 100 * result[f'{year:04d}']['count'] / (365 + leap_day)

            for month in range(1, 13):
                number_of_days = days_per_month[month]
                if month == 2:
                    number_of_days += leap_year(year)
                    
                if result[f'{year:04d}'][f'{month:02d}']['missing'] < missing_index_monthly_threshold:
                    result[f'{year:04d}'][f'{month:02d}']['value'] = 100 * result[f'{year:04d}'][f'{month:02d}']['count'] / (number_of_days + leap_day)

        index_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_{base_1:04d}_{base_2:04d}_10_TN10P.json')

        with open(index_filename, 'wt') as index_file:
            json.dump(result, index_file, indent=4)

        if self._plot:
            self._plot_annual_index(result)

        print('\t[OK]')


    def _index_11_tx10p(self, station, dataset):

        print(f'Computing index "TX10p" on station "{station}"', end='')

        tmax_percentile_by_window_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_1961_1990_00_TMAX_window_percentile.json')

        if not os.path.isfile(tmax_percentile_by_window_filename):
            print(f'climex.Index.compute_index(): index TX10p cannot be computed (percentile file not found)')
            return

        with open(tmax_percentile_by_window_filename, 'rt') as tmax_percentile_by_window_file:
            tmax_percentile_by_window = json.load(tmax_percentile_by_window_file)

        base_1, base_2 = self._project.baseline
        
        result = {
            'station': station,
            'name': Station.instance()._name_state(station),
            'index': 'TX10P',
            'description': 'TX10p: Percentage of days when TX < 10th percentile',
            'baseline': self._project.baseline,
            'units': u'Percentage of days (%)'
        }

        for year in range(base_1, base_2 + 1):
            result[f'{year:04d}'] = {
                'value': math.nan, 'count': 0, 'missing': 0,
                '01': {'value': math.nan, 'count': 0, 'missing': 0},
                '02': {'value': math.nan, 'count': 0, 'missing': 0},
                '03': {'value': math.nan, 'count': 0, 'missing': 0},
                '04': {'value': math.nan, 'count': 0, 'missing': 0},
                '05': {'value': math.nan, 'count': 0, 'missing': 0},
                '06': {'value': math.nan, 'count': 0, 'missing': 0},
                '07': {'value': math.nan, 'count': 0, 'missing': 0},
                '08': {'value': math.nan, 'count': 0, 'missing': 0},
                '09': {'value': math.nan, 'count': 0, 'missing': 0},
                '10': {'value': math.nan, 'count': 0, 'missing': 0},
                '11': {'value': math.nan, 'count': 0, 'missing': 0},
                '12': {'value': math.nan, 'count': 0, 'missing': 0}
            }

        for record in dataset:
            fields = record

            year = fields[0]
            month = fields[1]
            day = fields[2]

            tmax = fields[4]

            if tmax == null:
                result[f'{year:04d}']['missing'] += 1
                result[f'{year:04d}'][f'{month:02d}']['missing'] += 1
            else:
                day_of_year = f'{month:02d}-{day:02d}'
                percentile_10 = tmax_percentile_by_window[day_of_year]['10']
                if tmax < percentile_10:
                    result[f'{year:04d}']['count'] += 1
                    result[f'{year:04d}'][f'{month:02d}']['count'] += 1

        for year in range(base_1, base_2 + 1):
            leap_day = leap_year(year)
            if result[f'{year:04d}']['missing'] < missing_index_yearly_threshold:
                result[f'{year:04d}']['value'] = 100 * result[f'{year:04d}']['count'] / (365 + leap_day)

            for month in range(1, 13):
                number_of_days = days_per_month[month]
                if month == 2:
                    number_of_days += leap_year(year)
                    
                if result[f'{year:04d}'][f'{month:02d}']['missing'] < missing_index_monthly_threshold:
                    result[f'{year:04d}'][f'{month:02d}']['value'] = 100 * result[f'{year:04d}'][f'{month:02d}']['count'] / (number_of_days + leap_day)

        index_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_{base_1:04d}_{base_2:04d}_11_TX10P.json')

        with open(index_filename, 'wt') as index_file:
            json.dump(result, index_file, indent=4)

        if self._plot:
            self._plot_annual_index(result)

        print('\t[OK]')


    def _index_12_tn90p(self, station, dataset):

        print(f'Computing index "TN90p" on station "{station}"', end='')

        tmin_percentile_by_window_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_1961_1990_00_TMIN_window_percentile.json')

        if not os.path.isfile(tmin_percentile_by_window_filename):
            print(f'climex.Index.compute_index(): index TN90p cannot be computed (percentile file not found)')
            return

        with open(tmin_percentile_by_window_filename, 'rt') as tmin_percentile_by_window_file:
            tmin_percentile_by_window = json.load(tmin_percentile_by_window_file)

        base_1, base_2 = self._project.baseline
        
        result = {
            'station': station,
            'name': Station.instance()._name_state(station),
            'index': 'TN90P',
            'description': 'TN90p: Percentage of days when TN > 90th percentile',
            'baseline': self._project.baseline,
            'units': u'Percentage of days (%)'
        }

        for year in range(base_1, base_2 + 1):
            result[f'{year:04d}'] = {
                'value': math.nan, 'count': 0, 'missing': 0,
                '01': {'value': math.nan, 'count': 0, 'missing': 0},
                '02': {'value': math.nan, 'count': 0, 'missing': 0},
                '03': {'value': math.nan, 'count': 0, 'missing': 0},
                '04': {'value': math.nan, 'count': 0, 'missing': 0},
                '05': {'value': math.nan, 'count': 0, 'missing': 0},
                '06': {'value': math.nan, 'count': 0, 'missing': 0},
                '07': {'value': math.nan, 'count': 0, 'missing': 0},
                '08': {'value': math.nan, 'count': 0, 'missing': 0},
                '09': {'value': math.nan, 'count': 0, 'missing': 0},
                '10': {'value': math.nan, 'count': 0, 'missing': 0},
                '11': {'value': math.nan, 'count': 0, 'missing': 0},
                '12': {'value': math.nan, 'count': 0, 'missing': 0}
            }

        for record in dataset:
            fields = record

            year = fields[0]
            month = fields[1]
            day = fields[2]

            tmin = fields[5]

            if tmin == null:
                result[f'{year:04d}']['missing'] += 1
                result[f'{year:04d}'][f'{month:02d}']['missing'] += 1
            else:
                day_of_year = f'{month:02d}-{day:02d}'
                percentile_90 = tmin_percentile_by_window[day_of_year]['90']
                if tmin > percentile_90:
                    result[f'{year:04d}']['count'] += 1
                    result[f'{year:04d}'][f'{month:02d}']['count'] += 1

        for year in range(base_1, base_2 + 1):
            leap_day = leap_year(year)
            if result[f'{year:04d}']['missing'] < missing_index_yearly_threshold:
                result[f'{year:04d}']['value'] = 100 * result[f'{year:04d}']['count'] / (365 + leap_day)

            for month in range(1, 13):
                number_of_days = days_per_month[month]
                if month == 2:
                    number_of_days += leap_year(year)
                    
                if result[f'{year:04d}'][f'{month:02d}']['missing'] < missing_index_monthly_threshold:
                    result[f'{year:04d}'][f'{month:02d}']['value'] = 100 * result[f'{year:04d}'][f'{month:02d}']['count'] / (number_of_days + leap_day)

        index_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_{base_1:04d}_{base_2:04d}_12_TN90P.json')

        with open(index_filename, 'wt') as index_file:
            json.dump(result, index_file, indent=4)

        if self._plot:
            self._plot_annual_index(result)

        print('\t[OK]')


    def _index_13_tx90p(self, station, dataset):

        print(f'Computing index "TX90p" on station "{station}"', end='')

        tmax_percentile_by_window_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_1961_1990_00_TMAX_window_percentile.json')

        if not os.path.isfile(tmax_percentile_by_window_filename):
            print(f'climex.Index.compute_index(): index TX90p cannot be computed (percentile file not found)')
            return

        with open(tmax_percentile_by_window_filename, 'rt') as tmax_percentile_by_window_file:
            tmax_percentile_by_window = json.load(tmax_percentile_by_window_file)

        base_1, base_2 = self._project.baseline
        
        result = {
            'station': station,
            'name': Station.instance()._name_state(station),
            'index': 'TX90P',
            'description': 'TX90p: Percentage of days when TX > 90th percentile',
            'baseline': self._project.baseline,
            'units': u'Percentage of days (%)'
        }

        for year in range(base_1, base_2 + 1):
            result[f'{year:04d}'] = {
                'value': math.nan, 'count': 0, 'missing': 0,
                '01': {'value': math.nan, 'count': 0, 'missing': 0},
                '02': {'value': math.nan, 'count': 0, 'missing': 0},
                '03': {'value': math.nan, 'count': 0, 'missing': 0},
                '04': {'value': math.nan, 'count': 0, 'missing': 0},
                '05': {'value': math.nan, 'count': 0, 'missing': 0},
                '06': {'value': math.nan, 'count': 0, 'missing': 0},
                '07': {'value': math.nan, 'count': 0, 'missing': 0},
                '08': {'value': math.nan, 'count': 0, 'missing': 0},
                '09': {'value': math.nan, 'count': 0, 'missing': 0},
                '10': {'value': math.nan, 'count': 0, 'missing': 0},
                '11': {'value': math.nan, 'count': 0, 'missing': 0},
                '12': {'value': math.nan, 'count': 0, 'missing': 0}
            }

        for record in dataset:
            fields = record

            year = fields[0]
            month = fields[1]
            day = fields[2]

            tmax = fields[4]

            if tmax == null:
                result[f'{year:04d}']['missing'] += 1
                result[f'{year:04d}'][f'{month:02d}']['missing'] += 1
            else:
                day_of_year = f'{month:02d}-{day:02d}'
                percentile_90 = tmax_percentile_by_window[day_of_year]['90']
                if tmax > percentile_90:
                    result[f'{year:04d}']['count'] += 1
                    result[f'{year:04d}'][f'{month:02d}']['count'] += 1

        for year in range(base_1, base_2 + 1):
            leap_day = leap_year(year)
            if result[f'{year:04d}']['missing'] < missing_index_yearly_threshold:
                result[f'{year:04d}']['value'] = 100 * result[f'{year:04d}']['count'] / (365 + leap_day)

            for month in range(1, 13):
                number_of_days = days_per_month[month]
                if month == 2:
                    number_of_days += leap_year(year)
                    
                if result[f'{year:04d}'][f'{month:02d}']['missing'] < missing_index_monthly_threshold:
                    result[f'{year:04d}'][f'{month:02d}']['value'] = 100 * result[f'{year:04d}'][f'{month:02d}']['count'] / (number_of_days + leap_day)

        index_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_{base_1:04d}_{base_2:04d}_13_TX90P.json')

        with open(index_filename, 'wt') as index_file:
            json.dump(result, index_file, indent=4)

        if self._plot:
            self._plot_annual_index(result)

        print('\t[OK]')


    def _index_14_wsdi(self, station, dataset, span=6):

        if span not in (2, 5, 6):
            return

        tmax_percentile_by_window_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_1961_1990_00_TMAX_window_percentile.json')

        if not os.path.isfile(tmax_percentile_by_window_filename):
            print(f'climex.Index.compute_index(): index WSDI cannot be computed (percentile file not found)')
            return

        with open(tmax_percentile_by_window_filename, 'rt') as tmax_percentile_by_window_file:
            tmax_percentile_by_window = json.load(tmax_percentile_by_window_file)

        print(f'Computing index "WSDI" on station "{station}"', end='')

        base_1, base_2 = self._project.baseline
        
        result = {
            'station': station,
            'name': Station.instance()._name_state(station),
            'index': 'WSDI',
            'description': 'WSDI: Warm spell duration index', #: annual count of days with at least 6 consecutive days when TX > 90th percentile',
            'baseline': self._project.baseline,
            'units': 'Warm spell duration index (days)'
        }

        tmax_days = {}

        for year in range(base_1, base_2 + 1):
            result[f'{year:04d}'] = {
                'value': math.nan, 'count': 0, 'missing': 0,
                'spells': []
            }

            tmax_days[f'{year:04d}'] = {'tmax': [], 'day_of_year': []}

        for record in dataset:
            fields = record

            year = fields[0]
            month = fields[1]
            day = fields[2]

            tmax = fields[4]

            if tmax == null:
                result[f'{year:04d}']['missing'] += 1
                #result[f'{year:04d}'][f'{month:02d}']['missing'] += 1
            else:
                day_of_year = f'{month:02d}-{day:02d}'
                percentile_90 = tmax_percentile_by_window[day_of_year]['90']
                if tmax > percentile_90:
                    tmax_days[f'{year:04d}']['tmax'].append(tmax)
                    tmax_days[f'{year:04d}']['day_of_year'].append(datetime.datetime(year, month, day).timetuple().tm_yday)

        #print(tmax_days)

        for year in range(base_1, base_2 + 1):
            #print(tmax_days[f'{year:04d}'])
            spells = self._get_spells(tmax_days[f'{year:04d}']['day_of_year'])
            #print(spells)
            for spell in spells:
                if len(spell) >= span:
                    result[f'{year:04d}']['count'] += len(spell)
                    result[f'{year:04d}']['spells'].append(spell)

        for year in range(base_1, base_2 + 1):
            if result[f'{year:04d}']['missing'] < missing_index_yearly_threshold:
                result[f'{year:04d}']['value'] = result[f'{year:04d}']['count']

        index_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_{base_1:04d}_{base_2:04d}_14_WSDI.json')

        with open(index_filename, 'wt') as index_file:
            json.dump(result, index_file, indent=4)

        if self._plot:
            self._plot_annual_index(result)

        print('\t[OK]')


    def _index_15_csdi(self, station, dataset, span=6):

        if span not in (2, 5, 6):
            return

        tmin_percentile_by_window_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_1961_1990_00_TMIN_window_percentile.json')

        if not os.path.isfile(tmin_percentile_by_window_filename):
            print(f'climex.Index.compute_index(): index CSDI cannot be computed (percentile file not found)')
            return

        with open(tmin_percentile_by_window_filename, 'rt') as tmin_percentile_by_window_file:
            tmin_percentile_by_window = json.load(tmin_percentile_by_window_file)

        print(f'Computing index "CSDI" on station "{station}"', end='')

        base_1, base_2 = self._project.baseline
        
        result = {
            'station': station,
            'name': Station.instance()._name_state(station),
            'index': 'CSDI',
            'description': 'CSDI: Cold spell duration index', #: annual count of days with at least 6 consecutive days when TX > 90th percentile',
            'baseline': self._project.baseline,
            'units': 'Cold spell duration index (days)'
        }

        tmin_days = {}

        for year in range(base_1, base_2 + 1):
            result[f'{year:04d}'] = {
                'value': math.nan, 'count': 0, 'missing': 0,
                'spells': []
            }

            tmin_days[f'{year:04d}'] = {'tmin': [], 'day_of_year': []}

        for record in dataset:
            fields = record

            year = fields[0]
            month = fields[1]
            day = fields[2]

            tmin = fields[5]

            if tmin == null:
                result[f'{year:04d}']['missing'] += 1
                #result[f'{year:04d}'][f'{month:02d}']['missing'] += 1
            else:
                day_of_year = f'{month:02d}-{day:02d}'
                percentile_10 = tmin_percentile_by_window[day_of_year]['10']
                if tmin < percentile_10:
                    tmin_days[f'{year:04d}']['tmin'].append(tmin)
                    tmin_days[f'{year:04d}']['day_of_year'].append(datetime.datetime(year, month, day).timetuple().tm_yday)

        #print(tmax_days)

        for year in range(base_1, base_2 + 1):
            #print(tmax_days[f'{year:04d}'])
            spells = self._get_spells(tmin_days[f'{year:04d}']['day_of_year'])
            #print(spells)
            for spell in spells:
                if len(spell) >= span:
                    result[f'{year:04d}']['count'] += len(spell)
                    result[f'{year:04d}']['spells'].append(spell)

        for year in range(base_1, base_2 + 1):
            if result[f'{year:04d}']['missing'] < missing_index_yearly_threshold:
                result[f'{year:04d}']['value'] = result[f'{year:04d}']['count']

        index_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_{base_1:04d}_{base_2:04d}_15_CSDI.json')

        with open(index_filename, 'wt') as index_file:
            json.dump(result, index_file, indent=4)

        if self._plot:
            self._plot_annual_index(result)

        print('\t[OK]')


    def _index_16_dtr(self, station, dataset):

        print(f'Computing index "DTR" on station "{station}"', end='')

        base_1, base_2 = self._project.baseline
        
        result = {
            'station': station,
            'name': Station.instance()._name_state(station),
            'index': 'DTR',
            'description': 'DTR: Daily temperature range',
            'baseline': self._project.baseline,
            'units': u'Temperature range (\u00b0C)'
        }

        for year in range(base_1, base_2 + 1):
            result[f'{year:04d}'] = {
                'value': null, 'raw': 0.0, 'missing': 0,
                '01': {'value': 0.0, 'missing': 0},
                '02': {'value': 0.0, 'missing': 0},
                '03': {'value': 0.0, 'missing': 0},
                '04': {'value': 0.0, 'missing': 0},
                '05': {'value': 0.0, 'missing': 0},
                '06': {'value': 0.0, 'missing': 0},
                '07': {'value': 0.0, 'missing': 0},
                '08': {'value': 0.0, 'missing': 0},
                '09': {'value': 0.0, 'missing': 0},
                '10': {'value': 0.0, 'missing': 0},
                '11': {'value': 0.0, 'missing': 0},
                '12': {'value': 0.0, 'missing': 0}
            }

        for record in dataset:
            fields = record

            year = fields[0]
            month = fields[1]
            day = fields[2]

            tmax = fields[4]
            tmin = fields[5]

            if tmax == null or tmin == null:
                result[f'{year:04d}']['missing'] += 1
                result[f'{year:04d}'][f'{month:02d}']['missing'] += 1
            else:
                result[f'{year:04d}']['raw'] += tmax - tmin
                result[f'{year:04d}'][f'{month:02d}']['value'] += tmax - tmin

        for year in range(base_1, base_2 + 1):
            result[f'{year:04d}']['raw'] /= 365 + leap_year(year) - result[f'{year:04d}']['missing']
            for month in range(1, 13):
                delta_leap = 0
                if month == 2:
                    delta_leap = leap_year(year)
                #print(year, days_per_month[month], delta_leap, days_per_month[month] + delta_leap)
                try:
                    result[f'{year:04d}'][f'{month:02d}']['value'] /= days_per_month[month] + delta_leap - result[f'{year:04d}'][f'{month:02d}']['missing']
                except:
                    pass

        for year in range(base_1, base_2 + 1):
            if result[f'{year:04d}']['missing'] < missing_index_yearly_threshold:
                result[f'{year:04d}']['value'] = result[f'{year:04d}']['raw']
            else:
                result[f'{year:04d}']['value'] = math.nan

            for month in range(1, 13):
                if result[f'{year:04d}'][f'{month:02d}']['missing'] > missing_index_monthly_threshold:
                    result[f'{year:04d}'][f'{month:02d}']['value'] = math.nan

        index_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_{base_1:04d}_{base_2:04d}_16_DTR.json')

        with open(index_filename, 'wt') as index_file:
            json.dump(result, index_file, indent=4)

        if self._plot:
            self._plot_annual_index(result)

        print('\t[OK]')

    def _index_17_etr(self, station, dataset):

        print(f'Computing index "ETR" on station "{station}"', end='')

        base_1, base_2 = self._project.baseline
        
        result = {
            'station': station,
            'name': Station.instance()._name_state(station),
            'index': 'ETR',
            'description': 'ETR: Extreme temperature range',
            'baseline': self._project.baseline,
            'units': u'Temperature range (\u00b0C)'
        }

        for year in range(base_1, base_2 + 1):
            result[f'{year:04d}'] = {
                'value': null, 'raw': 0.0, 'tmax': null, 'tmin': -null, 'missing': 0,
                '01': {'value': null, 'tmax': null, 'tmin': -null, 'missing': 0},
                '02': {'value': null, 'tmax': null, 'tmin': -null, 'missing': 0},
                '03': {'value': null, 'tmax': null, 'tmin': -null, 'missing': 0},
                '04': {'value': null, 'tmax': null, 'tmin': -null, 'missing': 0},
                '05': {'value': null, 'tmax': null, 'tmin': -null, 'missing': 0},
                '06': {'value': null, 'tmax': null, 'tmin': -null, 'missing': 0},
                '07': {'value': null, 'tmax': null, 'tmin': -null, 'missing': 0},
                '08': {'value': null, 'tmax': null, 'tmin': -null, 'missing': 0},
                '09': {'value': null, 'tmax': null, 'tmin': -null, 'missing': 0},
                '10': {'value': null, 'tmax': null, 'tmin': -null, 'missing': 0},
                '11': {'value': null, 'tmax': null, 'tmin': -null, 'missing': 0},
                '12': {'value': null, 'tmax': null, 'tmin': -null, 'missing': 0}
            }

        for record in dataset:
            fields = record

            year = fields[0]
            month = fields[1]
            day = fields[2]

            tmax = fields[4]
            tmin = fields[5]
            """
            if tmax == null or tmin == null:
                result[f'{year:04d}']['missing'] += 1
                result[f'{year:04d}'][f'{month:02d}']['missing'] += 1
            else:
                result[f'{year:04d}']['raw'] += tmax - tmin
                result[f'{year:04d}'][f'{month:02d}']['value'] += tmax - tmin
            """

            if tmax == null or tmin == null:
                result[f'{year:04d}']['missing'] += 1
                result[f'{year:04d}'][f'{month:02d}']['missing'] += 1

            if tmax != null:
                if tmax > result[f'{year:04d}']['tmax']:
                    result[f'{year:04d}']['tmax'] = tmax
                if tmax > result[f'{year:04d}'][f'{month:02d}']['tmax']:
                    result[f'{year:04d}'][f'{month:02d}']['tmax'] = tmax

            if tmin != null:
                if tmin < result[f'{year:04d}']['tmin']:
                    result[f'{year:04d}']['tmin'] = tmin
                if tmin < result[f'{year:04d}'][f'{month:02d}']['tmin']:
                    result[f'{year:04d}'][f'{month:02d}']['tmin'] = tmin

        for year in range(base_1, base_2 + 1):
            result[f'{year:04d}']['raw'] = result[f'{year:04d}']['tmax'] - result[f'{year:04d}']['tmin']
            if result[f'{year:04d}']['missing'] < missing_index_yearly_threshold:
                result[f'{year:04d}']['value'] = result[f'{year:04d}']['raw']
            else:
                result[f'{year:04d}']['value'] = math.nan

            for month in range(1, 13):
                if result[f'{year:04d}'][f'{month:02d}']['tmax'] != null and result[f'{year:04d}'][f'{month:02d}']['tmin'] != -null:
                    result[f'{year:04d}'][f'{month:02d}']['value'] = result[f'{year:04d}'][f'{month:02d}']['tmax'] - result[f'{year:04d}'][f'{month:02d}']['tmin']
                else:
                    if result[f'{year:04d}'][f'{month:02d}']['tmax'] == null:
                        result[f'{year:04d}'][f'{month:02d}']['tmax'] = math.nan
                    if result[f'{year:04d}'][f'{month:02d}']['tmin'] == -null:
                        result[f'{year:04d}'][f'{month:02d}']['tmin'] = math.nan
                
                if result[f'{year:04d}'][f'{month:02d}']['missing'] > missing_index_monthly_threshold:
                    result[f'{year:04d}'][f'{month:02d}']['value'] = math.nan

        index_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_{base_1:04d}_{base_2:04d}_17_ETR.json')

        with open(index_filename, 'wt') as index_file:
            json.dump(result, index_file, indent=4)

        if self._plot:
            self._plot_annual_index(result)

        print('\t[OK]')

    def _index_18_rx1day(self, station, dataset):

        print(f'Computing index "Rx1Day" on station "{station}"', end='')

        base_1, base_2 = self._project.baseline
        
        result = {
            'station': station,
            'name': Station.instance()._name_state(station),
            'index': 'RX1DAY',
            'description': 'Rx1day: Maximum 1-day precipitation',
            'baseline': self._project.baseline,
            'units': 'Precipitation (mm)'
        }

        for year in range(base_1, base_2 + 1):
            result[f'{year:04d}'] = {
                'value': null, 'raw': null, 'missing': 0,
                '01': null, '02': null, '03': null, '04': null,
                '05': null, '06': null, '07': null, '08': null,
                '09': null, '10': null, '11': null, '12': null
            }

        for record in dataset:
            fields = record

            year = fields[0]
            month = fields[1]
            day = fields[2]

            prcp = float(fields[3])

            if prcp == -99.9:
                result[f'{year:04d}']['missing'] += 1
            else:
                if prcp > result[f'{year:04d}']['raw']:
                    result[f'{year:04d}']['raw'] = prcp
                if prcp > result[f'{year:04d}'][f'{month:02d}']:
                    result[f'{year:04d}'][f'{month:02d}'] = prcp

        for year in range(base_1, base_2 + 1):
            if result[f'{year:04d}']['missing'] < missing_index_yearly_threshold:
                result[f'{year:04d}']['value'] = result[f'{year:04d}']['raw']
            else:
                result[f'{year:04d}']['value'] = math.nan

        index_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_{base_1:04d}_{base_2:04d}_18_RX1DAY.json')

        with open(index_filename, 'wt') as index_file:
            json.dump(result, index_file, indent=4)
           
        if self._plot:
            self._plot_annual_index(result)

        print('\t[OK]')

    def _index_19_rx5day(self, station, dataset):

        print(f'Computing index "Rx5day" on station "{station}"', end='')

        base_1, base_2 = self._project.baseline
        
        result = {
            'station': station,
            'name': Station.instance()._name_state(station),
            'index': 'RX5DAY',
            'description': 'Rx5day: Maximum consecutive 5-day precipitation',
            'baseline': self._project.baseline,
            'units': 'Precipitation (mm)'
        }

        prcp_days = {}

        for year in range(base_1, base_2 + 1):
            result[f'{year:04d}'] = {
                'value': null, 'raw': null, 'missing': 0,
                'max_spell': []
            }

            prcp_days[f'{year:04d}'] = {'prcp': [], 'day_of_year': []}

        for record in dataset:
            fields = record

            year = fields[0]
            month = fields[1]
            day = fields[2]

            prcp = float(fields[3])

            if prcp == -99.9:
                result[f'{year:04d}']['missing'] += 1
            else:
                if prcp > 0:
                    prcp_days[f'{year:04d}']['prcp'].append(prcp)
                    prcp_days[f'{year:04d}']['day_of_year'].append(datetime.datetime(year, month, day).timetuple().tm_yday)

        #print(prcp_days)

        for year in range(base_1, base_2 + 1):
            #print(prcp_days[f'{year:04d}'])
            spells = self._get_spells(prcp_days[f'{year:04d}']['day_of_year'])
            #print(spells)
            for spell in spells:
                if len(spell) >= 5:
                    #print(spell)
                    no_of_sub_spells = len(spell) - 5 + 1
                    for i in range(no_of_sub_spells):
                        sub_spell = spell[i:i + 5]
                        #print(sub_spell)
                        sub_spell_prcp = 0.0
                        for day_of_year in sub_spell:
                            day_of_year_index = prcp_days[f'{year:04d}']['day_of_year'].index(day_of_year)
                            day_of_year_prcp = prcp_days[f'{year:04d}']['prcp'][day_of_year_index]

                            sub_spell_prcp += day_of_year_prcp
                            #print(day_of_year, day_of_year_prcp)

                        if sub_spell_prcp > result[f'{year:04d}']['raw']:
                            result[f'{year:04d}']['raw'] = sub_spell_prcp
                            sub_spell_dates = []
                            for day_of_year in sub_spell:
                                sub_spell_dates.append(
                                    (datetime.datetime(int(year), 1, 1) + datetime.timedelta(day_of_year - 1)).strftime('%Y-%m-%d')
                                )
                            result[f'{year:04d}']['max_spell'] = sub_spell_dates

        for year in range(base_1, base_2 + 1):
            if result[f'{year:04d}']['missing'] > missing_index_yearly_threshold or result[f'{year:04d}']['raw'] == null:
                result[f'{year:04d}']['value'] = math.nan
            else:
                result[f'{year:04d}']['value'] = result[f'{year:04d}']['raw']

        index_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_{base_1:04d}_{base_2:04d}_19_RX5DAY.json')

        with open(index_filename, 'wt') as index_file:
            json.dump(result, index_file, indent=4)
           
        if self._plot:
            self._plot_annual_index(result)

        print('\t[OK]')


    def _index_20_sdii(self, station, dataset):

        print(f'Computing index "SDII" on station "{station}"', end='')

        base_1, base_2 = self._project.baseline
        
        result = {
            'station': station,
            'name': Station.instance()._name_state(station),
            'index': 'SDII',
            'description': 'SDII: Simple precipitation intensity index',
            'baseline': self._project.baseline,
            'units': u'Intensity (mm/day)'
        }

        for year in range(base_1, base_2 + 1):
            result[f'{year:04d}'] = {
                'value': math.nan, 'raw': 0.0, 'w': 0, 'missing': 0,
                '01': {'value': math.nan, 'raw': 0.0, 'w': 0, 'missing': 0},
                '02': {'value': math.nan, 'raw': 0.0, 'w': 0, 'missing': 0},
                '03': {'value': math.nan, 'raw': 0.0, 'w': 0, 'missing': 0},
                '04': {'value': math.nan, 'raw': 0.0, 'w': 0, 'missing': 0},
                '05': {'value': math.nan, 'raw': 0.0, 'w': 0, 'missing': 0},
                '06': {'value': math.nan, 'raw': 0.0, 'w': 0, 'missing': 0},
                '07': {'value': math.nan, 'raw': 0.0, 'w': 0, 'missing': 0},
                '08': {'value': math.nan, 'raw': 0.0, 'w': 0, 'missing': 0},
                '09': {'value': math.nan, 'raw': 0.0, 'w': 0, 'missing': 0},
                '10': {'value': math.nan, 'raw': 0.0, 'w': 0, 'missing': 0},
                '11': {'value': math.nan, 'raw': 0.0, 'w': 0, 'missing': 0},
                '12': {'value': math.nan, 'raw': 0.0, 'w': 0, 'missing': 0}
            }

        for record in dataset:
            fields = record

            year = fields[0]
            month = fields[1]
            day = fields[2]

            prcp = float(fields[3])

            if prcp == -99.9:
                result[f'{year:04d}']['missing'] += 1
                result[f'{year:04d}'][f'{month:02d}']['missing'] += 1
            elif prcp >= 1.0:
                result[f'{year:04d}']['raw'] += prcp
                result[f'{year:04d}']['w'] += 1
                result[f'{year:04d}'][f'{month:02d}']['raw'] += prcp
                result[f'{year:04d}'][f'{month:02d}']['w'] += 1


        #print(result)
        for year in range(base_1, base_2 + 1):
            if result[f'{year:04d}']['missing'] < missing_index_yearly_threshold:
                if result[f'{year:04d}']['w'] > 0:
                    result[f'{year:04d}']['value'] = result[f'{year:04d}']['raw'] / result[f'{year:04d}']['w']
            #else:
            #    result[f'{year:04d}']['value'] = math.nan

            for month in range(1, 13):
                if result[f'{year:04d}'][f'{month:02d}']['missing'] < missing_index_monthly_threshold:
                    if result[f'{year:04d}'][f'{month:02d}']['raw'] > 0:
                    #    result[f'{year:04d}'][f'{month:02d}']['value'] = math.nan
                    #else:
                        result[f'{year:04d}'][f'{month:02d}']['value'] = result[f'{year:04d}'][f'{month:02d}']['raw'] / result[f'{year:04d}'][f'{month:02d}']['w']
                #else:
                #    result[f'{year:04d}'][f'{month:02d}']['missing'] = math.nan

        index_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_{base_1:04d}_{base_2:04d}_20_SDII.json')

        with open(index_filename, 'wt') as index_file:
            json.dump(result, index_file, indent=4)

        if self._plot:
            self._plot_annual_index(result)

        print('\t[OK]')

    def _index_21_r10mm(self, station, dataset):

        print(f'Computing index "R10mm" on station "{station}"', end='')

        base_1, base_2 = self._project.baseline
        
        result = {
            'station': station,
            'name': Station.instance()._name_state(station),
            'index': 'R10MM',
            'description': 'R10mm: Annual count of days when PRCP ≥ 10mm',
            'baseline': self._project.baseline,
            'units': 'Number of days (count)'
        }
        for year in range(base_1, base_2 + 1):
            result[f'{year:04d}'] = {
                'value': 0, 'missing': 0,                # count ########################################################
                '01': 0, '02': 0, '03': 0, '04': 0,
                '05': 0, '06': 0, '07': 0, '08': 0,
                '09': 0, '10': 0, '11': 0, '12': 0
            }

        for record in dataset:
            fields = record

            year = fields[0]
            month = fields[1]
            day = fields[2]

            prcp = float(fields[3])

            if prcp == -99.9:
                result[f'{year:04d}']['missing'] += 1
            elif prcp >= 10.0:
                result[f'{year:04d}']['value'] += 1
                result[f'{year:04d}'][f'{month:02d}'] += 1

        index_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_{base_1:04d}_{base_2:04d}_21_R10MM.json')

        with open(index_filename, 'wt') as index_file:
            json.dump(result, index_file, indent=4)

        if self._plot:
            self._plot_annual_index(result)

        print('\t[OK]')

    def _index_22_r20mm(self, station, dataset):

        print(f'Computing index "R20mm" on station "{station}"', end='')

        base_1, base_2 = self._project.baseline

        result = {
            'station': station,
            'name': Station.instance()._name_state(station),
            'index': 'R20MM',
            'description': 'R20mm: Annual count of days when PRCP ≥ 20mm',
            'baseline': self._project.baseline,
            'units': 'Number of days (count)'
        }
        for year in range(base_1, base_2 + 1):
            result[f'{year:04d}'] = {
                'value': 0, 'missing': 0,                # count ########################################################
                '01': 0, '02': 0, '03': 0, '04': 0,
                '05': 0, '06': 0, '07': 0, '08': 0,
                '09': 0, '10': 0, '11': 0, '12': 0
            }

        for record in dataset:
            fields = record

            year = fields[0]
            month = fields[1]
            day = fields[2]

            prcp = float(fields[3])

            if prcp == -99.9:
                result[f'{year:04d}']['missing'] += 1
            elif prcp >= 20.0:
                result[f'{year:04d}']['value'] += 1
                result[f'{year:04d}'][f'{month:02d}'] += 1

        index_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_{base_1:04d}_{base_2:04d}_22_R20MM.json')

        with open(index_filename, 'wt') as index_file:
            json.dump(result, index_file, indent=4)

        if self._plot:
            self._plot_annual_index(result)

        print('\t[OK]')

    def _index_23_rnnmm(self, station, dataset): #, threshold):

        if self._prcp_threshold is None:
            return

        #print(f'Computing index "Rnnmm" on station "{station}"', end='')

        base_1, base_2 = self._project.baseline


        if self._prcp_threshold.is_integer():
            self._prcp_threshold = int(self._prcp_threshold)

        print(f'Computing index "R{self._prcp_threshold}mm" on station "{station}"', end='')

        result = {
            'station': station,
            'name': Station.instance()._name_state(station),
            'index': f'R{self._prcp_threshold}MM',
            #'index': f'RNNMM',
            'description': f'Rnnmm: Annual count of days when PRCP ≥ {self._prcp_threshold} mm',
            'baseline': self._project.baseline,
            'units': 'Number of days (count)'
        }

        for year in range(base_1, base_2 + 1):
            result[f'{year:04d}'] = {
                'value': 0, 'count': 0, 'missing': 0,
                '01': 0, '02': 0, '03': 0, '04': 0,
                '05': 0, '06': 0, '07': 0, '08': 0,
                '09': 0, '10': 0, '11': 0, '12': 0
            }

        for record in dataset:
            fields = record

            year = fields[0]
            month = fields[1]
            day = fields[2]

            prcp = float(fields[3])

            if prcp == -99.9:
                result[f'{year:04d}']['missing'] += 1
            elif prcp >= self._prcp_threshold:
                result[f'{year:04d}']['count'] += 1
                result[f'{year:04d}'][f'{month:02d}'] += 1

        for year in range(base_1, base_2 + 1):
            if result[f'{year:04d}']['missing'] < missing_index_yearly_threshold:
                result[f'{year:04d}']['value'] = result[f'{year:04d}']['count']
            else:
                result[f'{year:04d}']['value'] = math.nan

        index_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_{base_1:04d}_{base_2:04d}_23_R{self._prcp_threshold}MM.json')

        with open(index_filename, 'wt') as index_file:
            json.dump(result, index_file, indent=4)

        self._prcp_threshold = None

        if self._plot:
            self._plot_annual_index(result)

        print('\t[OK]')

    def _index_24_cdd(self, station, dataset):

        print(f'Computing index "CDD" on station "{station}"', end='')

        base_1, base_2 = self._project.baseline
        
        result = {
            'station': station,
            'name': Station.instance()._name_state(station),
            'index': 'CDD',
            'description': 'CDD: Maximum length of dry spell',
            'baseline': self._project.baseline,
            'units': 'Number of days (count)'
        }
        cdd = {}
        for year in range(base_1, base_2 + 1):
            result[f'{year:04d}'] = {
                'value': 0, 'missing': 0,                # count ########################################################
                'maximum_spell': []
            }
            cdd[f'{year:04d}'] = []

        for i, record in enumerate(dataset):
            fields = record

            year = fields[0]
            month = fields[1]
            day = fields[2]

            prcp = float(fields[3])

            
            if prcp == -99.9:
                result[f'{year:04d}']['missing'] += 1
            elif prcp < 1.0:
                cdd[f'{year:04d}'].append(datetime.datetime(year, month, day).timetuple().tm_yday)

        for year, spell in cdd.items():
            year_rows = []
            current_row = []
            
            for i in range(1, len(spell)):
                difference = spell[i] - spell[i - 1]

                if difference == 1:
                    in_spell = True
                else:
                    in_spell = False

                if in_spell:
                    if len(current_row) == 0:
                        current_row.append(spell[i - 1])
                    current_row.append(spell[i])
                else:
                    if len(current_row) > 0:
                        year_rows.append(current_row)
                    current_row = []

            if len(current_row) > 0:
                year_rows.append(current_row)
                current_row = []


            for row in year_rows:
                if len(row) > result[year]['value']:
                    result[year]['value'] = len(row)
                    result[year]['maximum_spell'] = []
                    for day in row:
                        result[year]['maximum_spell'].append(
                            (datetime.datetime(int(year), 1, 1) + datetime.timedelta(day - 1)).strftime('%Y-%m-%d')
                        )

        # datetime.datetime(2021, 1, 1) + datetime.timedelta(day - 1)

        index_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_{base_1:04d}_{base_2:04d}_24_CDD.json')

        with open(index_filename, 'wt') as index_file:
            json.dump(result, index_file, indent=4)

        if self._plot:
            self._plot_annual_index(result)

        print('\t[OK]')

    def _index_25_cwd(self, station, dataset):

        print(f'Computing index "CWD" on station "{station}"', end='')

        base_1, base_2 = self._project.baseline
        
        result = {
            'station': station,
            'name': Station.instance()._name_state(station),
            'index': 'CWD',
            'description': 'CWD: Maximum length of wet spell',
            'baseline': self._project.baseline,
            'units': 'Number of days (count)'
        }

        cwd = {}
        for year in range(base_1, base_2 + 1):
            result[f'{year:04d}'] = {
                'value': 0, 'raw': 0, 'missing': 0,
                'maximum_spell': []
            }
            cwd[f'{year:04d}'] = []

        for record in dataset:
            fields = record

            year = fields[0]
            month = fields[1]
            day = fields[2]

            prcp = float(fields[3])

            if prcp == -99.9:
                result[f'{year:04d}']['missing'] += 1
            elif prcp > 1.0:
                cwd[f'{year:04d}'].append(datetime.datetime(year, month, day).timetuple().tm_yday)

        for year, wet_days in cwd.items():
            #print(year, wet_days)
            spells = self._get_spells(wet_days)
            #print(spells)

            for spell in spells:
                if len(spell) > result[year]['raw']:
                    result[year]['raw'] = len(spell)
                    result[year]['maximum_spell'] = []
                    for day in spell:
                        result[year]['maximum_spell'].append(
                            (datetime.datetime(int(year), 1, 1) + datetime.timedelta(day - 1)).strftime('%Y-%m-%d')
                        )

        for year in range(base_1, base_2 + 1):
            if result[f'{year:04d}']['missing'] < missing_index_yearly_threshold:
                result[f'{year:04d}']['value'] = result[f'{year:04d}']['raw']
            else:
                result[f'{year:04d}']['value'] = math.nan

        index_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_{base_1:04d}_{base_2:04d}_25_CWD.json')

        with open(index_filename, 'wt') as index_file:
            json.dump(result, index_file, indent=4)

        if self._plot:
            self._plot_annual_index(result)

        print('\t[OK]')

    def _index_26_r95p(self, station, dataset, verbose=True):

        if verbose: 
            print(f'Computing index "R95P" on station "{station}"', end='')

        percentile_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_1961_1990_00_PRCP_percentiles.json')

        try:
            with open(percentile_filename, 'rt') as percentile_file:
                prcp_percentiles = json.load(percentile_file)
        except:
            print('\t[FAILED]')
            print(f'climex.Index.compute_index(): Percentile data file "{str(station)}_1961_1990_00_PRCP_percentiles.json" not found')
            return

        base_1, base_2 = self._project.baseline

        result = {
            'station': station,
            'name': Station.instance()._name_state(station),
            'index': 'R95P',
            'description': 'R95p: Annual total PRCP when RR > 95th percentile',
            'baseline': self._project.baseline,
            'units': 'Precipitation (mm)'
        }

        for year in range(base_1, base_2 + 1):
            result[f'{year:04d}'] = {
                'value': 0, 'raw': 0, 'missing': 0,
                '01': 0, '02': 0, '03': 0, '04': 0,
                '05': 0, '06': 0, '07': 0, '08': 0,
                '09': 0, '10': 0, '11': 0, '12': 0
            }

        for record in dataset:
            fields = record

            year = fields[0]
            month = fields[1]
            day = fields[2]

            prcp = float(fields[3])

            if prcp == -99.9:
                result[f'{year:04d}']['missing'] += 1
            #elif prcp >= prcp_percentiles['percentiles'][f'{year:04d}']['95']:
            elif prcp >= prcp_percentiles['baseline']['95']:
                result[f'{year:04d}']['raw'] += prcp
                result[f'{year:04d}'][f'{month:02d}'] += prcp


        for year in range(base_1, base_2 + 1):
            if result[f'{year:04d}']['missing'] < missing_index_yearly_threshold:
                result[f'{year:04d}']['value'] = result[f'{year:04d}']['raw']
            else:
                result[f'{year:04d}']['value'] = math.nan

        index_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_{base_1:04d}_{base_2:04d}_26_R95P.json')

        with open(index_filename, 'wt') as index_file:
            json.dump(result, index_file, indent=4)

        if self._plot:
            self._plot_annual_index(result)

        if verbose:
            print('\t[OK]')

    def _index_27_r99p(self, station, dataset):

        print(f'Computing index "R99P" on station "{station}"', end='')

        percentile_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_1961_1990_00_PRCP_percentiles.json')

        try:
            with open(percentile_filename, 'rt') as percentile_file:
                prcp_percentiles = json.load(percentile_file)
        except:
            print('\t[FAILED]')
            print(f'climex.Index.compute_index(): Percentile data file "{str(station)}_1961_1990_00_PRCP_percentiles.json" not found')
            return

        base_1, base_2 = self._project.baseline

        result = {
            'station': station,
            'name': Station.instance()._name_state(station),
            'index': 'R99P',
            'description': 'R99p: Annual total PRCP when RR > 99th percentile',
            'baseline': self._project.baseline,
            'units': 'Precipitation (mm)'
        }

        for year in range(base_1, base_2 + 1):
            result[f'{year:04d}'] = {
                'value': 0, 'raw': 0, 'missing': 0,
                '01': 0, '02': 0, '03': 0, '04': 0,
                '05': 0, '06': 0, '07': 0, '08': 0,
                '09': 0, '10': 0, '11': 0, '12': 0
            }

        for record in dataset:
            fields = record

            year = fields[0]
            month = fields[1]
            day = fields[2]

            prcp = float(fields[3])

            if prcp == -99.9:
                result[f'{year:04d}']['missing'] += 1
            #elif prcp >= prcp_percentiles['percentiles'][f'{year:04d}']['99']:
            elif prcp >= prcp_percentiles['baseline']['99']:
                result[f'{year:04d}']['raw'] += prcp
                result[f'{year:04d}'][f'{month:02d}'] += prcp


        for year in range(base_1, base_2 + 1):
            if result[f'{year:04d}']['missing'] < missing_index_yearly_threshold:
                result[f'{year:04d}']['value'] = result[f'{year:04d}']['raw']
            else:
                result[f'{year:04d}']['value'] = math.nan

        index_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_{base_1:04d}_{base_2:04d}_27_R99P.json')

        with open(index_filename, 'wt') as index_file:
            json.dump(result, index_file, indent=4)

        if self._plot:
            self._plot_annual_index(result)

        print('\t[OK]')

    def _index_28_r95ptot(self, station, dataset):

        print(f'Computing index "R95PTOT" on station "{station}"', end='')

        base_1, base_2 = self._project.baseline

        r95p_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_{base_1:04d}_{base_2:04d}_26_R95P.json')

        r95p_result = {}

        try:
            with open(r95p_filename, 'rt') as r95p_file:
                r95p_result = json.load(r95p_file)
        except:
            self._index_26_r95p(station, dataset)

        if not r95p_result:
            try:
                with open(r95p_filename, 'rt') as r95p_file:
                    r95p_result = json.load(r95p_file)
            except:
                print(f'climex.Index.index_batch(): file {str(station)}_{base_1:04d}_{base_2:04d}_26_R95P.json not found')
                return
        
        prcptot_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_{base_1:04d}_{base_2:04d}_30_PRCPTOT.json')

        prcptot_result = {}

        try:
            with open(prcptot_filename, 'rt') as prcptot_file:
                prcptot_result = json.load(prcptot_file)
        except:
            self._index_30_prcptot(station, dataset, verbose=False)

        if not prcptot_result:
            try:
                with open(prcptot_filename, 'rt') as prcptot_file:
                    prcptot_result = json.load(prcptot_file)
            except:
                print(f'climex.Index.index_batch(): file {str(station)}_{base_1:04d}_{base_2:04d}_30_PRCPTOT.json not found')
                return



        result = {
            'station': station,
            'name': Station.instance()._name_state(station),
            'index': 'R95PTOT',
            'description': 'R95pTOT: Contribution to total precipitation from very wet days',
            'baseline': self._project.baseline,
            'units': 'Percentage (%)'
        }

        for year in range(base_1, base_2 + 1):
            result[f'{year:04d}'] = {
                'value': math.nan, 'raw': 0, 'missing': 0,
                '01': math.nan, '02': math.nan, '03': math.nan, '04': math.nan,
                '05': math.nan, '06': math.nan, '07': math.nan, '08': math.nan,
                '09': math.nan, '10': math.nan, '11': math.nan, '12': math.nan
            }

        for year in range(base_1, base_2 + 1):
            if math.isnan(r95p_result[f'{year:04d}']['value']): continue
            if math.isnan(prcptot_result[f'{year:04d}']['value']): continue
            if prcptot_result[f'{year:04d}']['value'] == 0: continue

            #    result[f'{year:04d}']['value'] = math.nan
            #else:
            #    result[f'{year:04d}']['value'] = 100 * r95p_result[f'{year:04d}']['value'] / prcptot_result[f'{year:04d}']['value']

            result[f'{year:04d}']['value'] = 100 * r95p_result[f'{year:04d}']['value'] / prcptot_result[f'{year:04d}']['value']

            #print('R95P', r95p_result[f'{year:04d}']['value'], 'PRCPTOT', prcptot_result[f'{year:04d}']['value']) 

        index_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_{base_1:04d}_{base_2:04d}_28_R95PTOT.json')

        with open(index_filename, 'wt') as index_file:
            json.dump(result, index_file, indent=4)

        if self._plot:
            self._plot_annual_index(result)

        print('\t[OK]')
            
    def _index_29_r99ptot(self, station, dataset):

        print(f'Computing index "R99PTOT" on station "{station}"', end='')

        base_1, base_2 = self._project.baseline

        r99p_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_{base_1:04d}_{base_2:04d}_27_R99P.json')

        r99p_result = {}

        try:
            with open(r99p_filename, 'rt') as r99p_file:
                r99p_result = json.load(r99p_file)
        except:
            self._index_27_r99p(station, dataset)

        if not r99p_result:
            try:
                with open(r99p_filename, 'rt') as r99p_file:
                    r99p_result = json.load(r99p_file)
            except:
                print(f'climex.Index.index_batch(): file {str(station)}_{base_1:04d}_{base_2:04d}_27_R99P.json not found')
                return
        
        prcptot_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_{base_1:04d}_{base_2:04d}_30_PRCPTOT.json')

        prcptot_result = {}

        try:
            with open(prcptot_filename, 'rt') as prcptot_file:
                prcptot_result = json.load(prcptot_file)
        except:
            self._index_30_prcptot(station, dataset, verbose=False)

        if not prcptot_result:
            try:
                with open(prcptot_filename, 'rt') as prcptot_file:
                    prcptot_result = json.load(prcptot_file)
            except:
                print(f'climex.Index.index_batch(): file {str(station)}_{base_1:04d}_{base_2:04d}_30_PRCPTOT.json not found')
                return

        result = {
            'station': station,
            'name': Station.instance()._name_state(station),
            'index': 'R99PTOT',
            'description': 'R99pTOT: Contribution to total precipitation from extremely wet days',
            'baseline': self._project.baseline,
            'units': 'Percentage (%)'
        }

        for year in range(base_1, base_2 + 1):
            result[f'{year:04d}'] = {
                'value': math.nan, 'raw': 0, 'missing': 0,
                '01': math.nan, '02': math.nan, '03': math.nan, '04': math.nan,
                '05': math.nan, '06': math.nan, '07': math.nan, '08': math.nan,
                '09': math.nan, '10': math.nan, '11': math.nan, '12': math.nan
            }

        for year in range(base_1, base_2 + 1):
            if math.isnan(r99p_result[f'{year:04d}']['value']): continue
            if math.isnan(prcptot_result[f'{year:04d}']['value']): continue
            if prcptot_result[f'{year:04d}']['value'] == 0: continue

            #    result[f'{year:04d}']['value'] = math.nan
            #else:
            #    result[f'{year:04d}']['value'] = 100 * r99p_result[f'{year:04d}']['value'] / prcptot_result[f'{year:04d}']['value']

            result[f'{year:04d}']['value'] = 100 * r99p_result[f'{year:04d}']['value'] / prcptot_result[f'{year:04d}']['value']


        index_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_{base_1:04d}_{base_2:04d}_29_R99PTOT.json')

        with open(index_filename, 'wt') as index_file:
            json.dump(result, index_file, indent=4)

        if self._plot:
            self._plot_annual_index(result)

        print('\t[OK]')

    def _index_30_prcptot(self, station, dataset, verbose=True):

        if verbose: 
            print(f'Computing index "PRCPTOT" on station "{station}"', end='')

        base_1, base_2 = self._project.baseline
        
        result = {
            'station': station,
            'name': Station.instance()._name_state(station),
            'index': 'PRCPTOT',
            'description': 'PRCPTOT: Annual total precipitation on wet days',
            'baseline': self._project.baseline,
            'units': 'Precipitation (mm)'
        }

        for year in range(base_1, base_2 + 1):
            result[f'{year:04d}'] = {
                'value': 0.0, 'missing': 0,                # count ########################################################
                '01': 0.0, '02': 0.0, '03': 0.0, '04': 0.0,
                '05': 0.0, '06': 0.0, '07': 0.0, '08': 0.0,
                '09': 0.0, '10': 0.0, '11': 0.0, '12': 0.0
            }

        for record in dataset:
            fields = record

            year = fields[0]
            month = fields[1]
            day = fields[2]

            prcp = float(fields[3])

            if prcp == -99.9:
                result[f'{year:04d}']['missing'] += 1
            else:
                result[f'{year:04d}']['value'] += prcp
                result[f'{year:04d}'][f'{month:02d}'] += prcp

        index_filename = os.path.join(self._project._project_dir, 'INDEX', f'{str(station)}_{base_1:04d}_{base_2:04d}_30_PRCPTOT.json')

        with open(index_filename, 'wt') as index_file:
            json.dump(result, index_file, indent=4)

        if self._plot:
            self._plot_annual_index(result)

        if verbose:
            print('\t[OK]')
