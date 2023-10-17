
import json
import math
import os


def gauss(x):
    """Algorithm 209 - Gauss (https://doi.org/10.1145/367651.367664)"""

    if x == 0:
        p = 0.0
    else:
        y = math.fabs(x)/2

        if y >= 3.0:
            p = 1.0
        elif y < 1.0:
            w = y*y

            p = ((((((((0.000124818987 * w \
                - 0.001075204047) * w + 0.005198775019) * w \
                - 0.019198292004) * w + 0.059054035642) * w \
                - 0.151968751364) * w + 0.319152932694) * w \
                - 0.531923007300) * w + 0.797884560593) * y * 2.0
        else:
            y = y - 2.0

            p = (((((((((((((-0.000045255659 * y \
                + 0.000152529290) * y - 0.000019538132) * y \
                - 0.000676904986) * y + 0.001390604284) * y \
                - 0.000794620820) * y - 0.002034254874) * y \
                + 0.006549791214) * y - 0.010557625006) * y \
                + 0.011630447319) * y - 0.009279453341) * y \
                + 0.005353579108) * y - 0.002141268741) * y \
                + 0.000535310849) * y + 0.999936657524

    if x > 0.0:
        p = (p + 1.0)/2.0
    else:
        p = (1.0 - p)/2.0

    return p


def student(t, n):
    """Algorithm 395 - Student's t (https://doi.org/10.1145/355598.362775)"""

    t = t*t
    y = t/n
    b = y + 1.0

    if y > 1.0E-6:
        y = math.log(b)

    a = n - 0.5
    b = 48.0*a*a
    y = a*y

    y = (((((-0.4 * y - 3.3) * y - 24.0) * y - 85.5) /    \
        (0.8 * y * y + 100.0 + b) + y + 3.0) / b + 1.0) * \
        math.sqrt(y)

    p = 2.0*gauss(-y)

    return p


def percentile(data, p=50):

    # Code from: https://stackoverflow.com/questions/8137391/percentile-calculation
    # Documented here: https://doi.org/10.2307%2F2684934
    #                  https://en.wikipedia.org/wiki/Percentile

    data.sort()

    n = len(data)

    rank = p / 100 * (n - 1)

    index, frac = divmod(rank, 1)

    if (index + 1) < n:
        percentile_value = data[int(index)] * (1 - frac) + data[int(index) + 1] * frac
    else:
        percentile_value = data[int(index)]
        #percentile_value = data[-1]

    return percentile_value

    ###################################### REVIEW podio !!!!!!!


def percentile_nist(data, p=50):
    # Code from: https://www.itl.nist.gov/div898/handbook/prc/section2/prc262.htm

    data.sort()

    n = len(data)

    rank = p / 100 * (n + 1)

    index, frac = divmod(rank, 1)

    if (index + 1) < n:
        percentile_value = data[int(index) - 1] + (data[int(index)] - data[int(index) - 1]) * frac
    else:
        percentile_value = data[int(index)]

    return percentile_value


def annual_regression_line(x, y):
    """Computes regression line, error of slope and p-value of arrays x and y. NaNs are not allowed"""

    #print('stats.annual_regression_line()')

    n = len(x)

    if n == 0:
        return

    x_mean = 0.0
    y_mean = 0.0
    for i in range(n):
        x_mean += x[i]
        y_mean += y[i]

    x_mean /= n
    y_mean /= n

    a_numerator = 0.0
    a_denominator = 0.0
    for i in range(n):
        a_numerator += (x[i] - x_mean) * (y[i] - y_mean)
        a_denominator += (x[i] - x_mean) * (x[i] - x_mean)

    try:
        a = a_numerator / a_denominator
        b = y_mean - (a * x_mean)
    except:
        return {}
    
    #print(a_numerator)
    #print(a_denominator)

    #print(a)
    #print(b)

    error_numerator = 0.0
    for i in range(n):
        y_estimate = a * x[i] + b

        error_numerator += (y[i] - y_estimate) * (y[i] - y_estimate)

    degrees_of_freedom = n - 2

    error_of_slope = math.sqrt(error_numerator / degrees_of_freedom) / math.sqrt(a_denominator)
 
    try:
        p_value = student(a / error_of_slope, degrees_of_freedom)
    except:
        p_value = math.nan

    regression = {
        'a': a,
        'b': b,
        'dof': degrees_of_freedom,
        'error': error_of_slope,
        'p-value': p_value
    }

    return regression

    # Result from scipy.stats.linregress() station 11001
    # LinregressResult(slope=-0.21477832512315287, intercept=740.6088669950742, rvalue=-0.07903631158485658, pvalue=0.6836113398537875, 
    # stderr=0.5213401686477341)


def monthly_regression_line(x, y):
    pass


def temp_percentiles(station, dataset, baseline, percentile_filename):
    pass


def prcp_percentiles(station, dataset, baseline, percentile_filename):
    """Computes percentiles 95 and 99 of PRCP dataset"""

    if dataset is None:
        return

    print(f'Computing PRCP percentiles on station "{station}"', end='')

    #percentile_filename = os.path.join(project._project_dir, 'INDEX', f'{str(station)}_1961_1990_00_PRCP_percentiles.txt')
    #print(percentile_filename)


    base_1, base_2 = baseline

    percentiles = {}
    data = {}
    for year in range(base_1, base_2 + 1):
        percentiles[f'{year:04d}'] = {'95': math.nan, '99': math.nan}
        data[f'{year:04d}'] = {'missing': 0, 'wet_days': []}

    result = {
        'baseline': {'period': baseline, '95': math.nan, '99': math.nan},
        'percentiles': percentiles,
        'data': data
    }
    #print(result)
    for record in dataset:
        fields = record

        year = fields[0]
        month = fields[1]
        day = fields[2]

        prcp = float(fields[3])

        if prcp == -99.9:
            result['data'][f'{year:04d}']['missing'] += 1
        else:
            if prcp >= 1.0:
                result['data'][f'{year:04d}']['wet_days'].append(prcp)

    total_wet_days_in_period = []
    for year in range(base_1, base_2 + 1):
        result['data'][f'{year:04d}']['wet_days'].sort()
        wet_days_dataset = result['data'][f'{year:04d}']['wet_days']

        total_wet_days_in_period += wet_days_dataset

        if len(wet_days_dataset) > 4:
            result['percentiles'][f'{year:04d}']['95'] = percentile(wet_days_dataset, 95)
            result['percentiles'][f'{year:04d}']['99'] = percentile(wet_days_dataset, 99)

    result['baseline']['95'] = percentile(total_wet_days_in_period, 95)
    result['baseline']['99'] = percentile(total_wet_days_in_period, 99)

    #print('stats.prcp_percentiles()')
    #return

    #with open(percentile_filename, 'wt') as percentile_file:
    #    json.dump(result, percentile_file, indent=4)


    try:
        with open(percentile_filename, 'wt') as percentile_file:
            json.dump(result, percentile_file, indent=4)
        #print(percentile_filename)
    except:
        pass

    print('\t[OK]')

    #return result
