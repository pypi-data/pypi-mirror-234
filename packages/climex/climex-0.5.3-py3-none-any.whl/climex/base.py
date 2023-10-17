
import glob
import io
import json
import os
import zipfile

import requests
import shutil

from . config import Config


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


def ls():
    """Lists all existing CLIMEX projects"""

    project_dir = os.path.join(Config.instance().climex_dir, 'PROJECTS')
    print(f'CLIMEX projects [{project_dir}]\n')

    project_dir_contents = sorted(glob.glob(os.path.join(project_dir, '*')))
    for item in project_dir_contents:
        if os.path.isdir(item):
            print('    ', os.path.basename(item))


#def describe(project):
#    """Prints information about a given CLIMEX project"""
#    print(Config.instance().climex_dir)


def delete(project):
    """Deletes a CLIMEX project"""

    project_dir = os.path.join(Config.instance().climex_dir, 'PROJECTS')
    project_dir_contents = sorted(glob.glob(os.path.join(project_dir, '*')))

    project_dir_basenames = []
    for item in project_dir_contents:
        project_dir_basenames.append(os.path.basename(item))
    
    if project.upper() not in project_dir_basenames:
        print(f'climex.delete(): project {project.upper()} not found.')
        return

    shutil.rmtree(
        os.path.join(Config.instance().climex_dir, 'PROJECTS', project.upper())
    )


def _conagua_kml_to_geojson(kml):
    """Converts CONAGUA KML dataset to GeoJSON"""

    conagua_all = {'type': 'FeatureCollection', 'features': []}
    conagua_all_by_id = {}
    conagua_all_by_state = {}

    conagua_operating = {'type': 'FeatureCollection', 'features': []}
    conagua_operating_by_id = {}
    conagua_operating_by_state = {}

    features = []
    s1 = 0

    while True:

        # Extract <Placemark> element..
        p1 = kml.find('<Placemark>', s1)
        p2 = kml.find('</Placemark>', s1)

        if p1 == -1 or p2 == -1:
            break

        placemark = kml[p1:p2+len('</Placemark>')]

        # Process <Placemark> element...

        # Element <name>...
        n1 = placemark.find('<name>')
        n2 = placemark.find('</name>')

        name = placemark[n1+len('<name>'):n2]

        # Element <coordinates>...
        c1 = placemark.find('<coordinates>')
        c2 = placemark.find('</coordinates>')

        coord = list(
            map(
                float,
                placemark[c1+len('<coordinates>'):c2].split(',')
            )
        )

        # Element <description>...
        d1 = placemark.find('<description>')
        d2 = placemark.find('</description>')

        desc = placemark[d1+len('<description>'):d2]

        # Field "Operación"...
        o1 = desc.find('<h3>')
        o2 = desc.find('</h3>', o1)

        op = desc[o1+len('<h3>'):o2]

        o3 = op.rfind('-')

        nom = op[:o3-1]
        act = op[o3+2:]

        # Field "Estado"...
        e1 = desc.find('<p><b>Estado : </b>')
        e2 = desc.find('</p>', e1)

        est = desc[e1+len('<p><b>Estado : </b>'):e2]

        # Field "Municipio"...
        m1 = desc.find('<p><b>Municipio : </b>')
        m2 = desc.find('</p>', m1)

        mun = desc[m1+len('<p><b>Municipio : </b>'):m2]

        # Field "Organismo"...
        g1 = desc.find('<p><b>Organismo : </b>')
        g2 = desc.find('</p>', g1)

        org = desc[g1+len('<p><b>Organismo : </b>'):g2]

        # Field "Cuenca hidrográfica"...
        h1 = desc.find('<p><b>Cuenca : </b>')
        h2 = desc.find('</p>', h1)

        ch = desc[h1+len('<p><b>Cuenca : </b>'):h2]

        # Field "URL"...
        u1 = desc.find('<p><a href=')
        u2 = desc.find('</a></p>', u1)

        url = desc[u1+len('<p><a href='):u2]

        ###u3 = url.find('>Climatología diaria')
        u3 = url.find('>Climatolog')

        if u3 != -1:
            url = desc[u1+len('<p><a href='):u1+len('<p><a href=')+u3]
        else:
            url = ''

        """
        # GeoJSON properties...
        properties = {
            'EID': name,
            'Nombre': nom,
            'Actividad': act,
            'Estado': est,
            'Municipio': mun,
            'Organismo': org,
            'Cuenca': ch,
            'URL': url
        }
        """

        geojson_feature = {
            'id': name,
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': coord
            },
            'properties': {
                'EID': name,
                'Nombre': nom,
                'Actividad': act,
                'Estado': est,
                'Municipio': mun,
                'Organismo': org,
                'Cuenca': ch,
                'URL': url
            }
        }

        features.append(geojson_feature)

        conagua_all['features'].append(geojson_feature)
        conagua_all_by_id[name] = geojson_feature

        try:
            conagua_all_by_state[est].append(geojson_feature)
        except:
            conagua_all_by_state[est] = [geojson_feature]


        if act == 'OPERANDO':
            conagua_operating['features'].append(geojson_feature)
            conagua_operating_by_id[name] = geojson_feature

            try:
                conagua_operating_by_state[est].append(geojson_feature)
            except:
                conagua_operating_by_state[est] = [geojson_feature]

        # Index to search in the next iteration...
        s1 = p2 + len('</Placemark>')

    return [conagua_all, conagua_all_by_id, conagua_all_by_state,
            conagua_operating, conagua_operating_by_id, conagua_operating_by_state]


def geojson():
    """Downloads CONAGUA stations in GeoJSON format"""

    response = requests.get(Config.instance().climex_geo_url)

    if response.status_code != 200:
        print(f'climex.geojson(): HTTP request failed with status code [{response.status_code}]')
        return

    # Get KMZ and decompress to KML...
    kmz = zipfile.ZipFile(io.BytesIO(response.content))
    kml = kmz.open('doc.kml', 'r').read().decode('utf-8')

    geojson_all = _conagua_kml_to_geojson(kml)

    try:
        conagua_all_filename = os.path.join(Config.instance().climex_dir, 'GEOJSON', 'conagua_all.geojson')
        with open(conagua_all_filename, 'wt') as json_file:
            json.dump(geojson_all[0], json_file, indent=4)
    except:
        pass

    try:
        conagua_all_by_id_filename = os.path.join(Config.instance().climex_dir, 'GEOJSON', 'conagua_all_by_id.json')
        with open(conagua_all_by_id_filename, 'wt') as json_file:
            json.dump(geojson_all[1], json_file, indent=4)
    except:
        pass

    try:
        conagua_all_by_state_filename = os.path.join(Config.instance().climex_dir, 'GEOJSON', 'conagua_all_by_state.json')
        with open(conagua_all_by_state_filename, 'wt') as json_file:
            json.dump(geojson_all[2], json_file, indent=4)
    except:
        pass

    try:
        conagua_operating_filename = os.path.join(Config.instance().climex_dir, 'GEOJSON', 'conagua_operating.geojson')
        with open(conagua_operating_filename, 'wt') as json_file:
            json.dump(geojson_all[3], json_file, indent=4)
    except:
        pass

    try:
        conagua_operating_by_id_filename = os.path.join(Config.instance().climex_dir, 'GEOJSON', 'conagua_operating_by_id.json')
        with open(conagua_operating_by_id_filename, 'wt') as json_file:
            json.dump(geojson_all[4], json_file, indent=4)
    except:
        pass

    try:
        conagua_operating_by_state_filename = os.path.join(Config.instance().climex_dir, 'GEOJSON', 'conagua_operating_by_state.json')
        with open(conagua_operating_by_state_filename, 'wt') as json_file:
            json.dump(geojson_all[5], json_file, indent=4)
    except:
        pass


def html_popup(entity):
    """Converts the set of properties of a GeoJSON entity to a HTML table"""

    html = '<table border= "1px" bordercolor="#FFFFFF">\n'

    for key, value in entity['properties'].items():
        html += f'<tr> <td bgcolor="#DCDCDC"> &emsp; <b>{key}</b>&emsp;</td> <td> &emsp; {value} &emsp; </td> </tr>'

    html += '</table>'

    return html


def parse_item(item):
    """Parses \'item\' and returns an integer, float, or string"""
    
    # This funcions may not be completely safe
    
    float_digits = '.eE'
    int_digits = '-0123456789'
    str_digits = '_abcdefghijklmnopqrstuvwxyz'

    type_of_item = {'float': 0, 'int': 0, 'str': 0, 'other': 0}
    for character in str(item):
        if character in int_digits:
            type_of_item['int'] += 1
        elif character in float_digits:
            type_of_item['float'] += 1
        elif character.lower() in str_digits:
            type_of_item['str'] += 1
        else:
            type_of_item['other'] += 1

    if type_of_item['other'] > 0:
        return str(item)
    elif type_of_item['float'] > 0:
        try:
            return float(str(item))
        except:
            return str(item)
    elif type_of_item['int'] > 0:
        try:
            return int(str(item))
        except:
            return str(item)
    elif type_of_item['str'] > 0:
        return str(item)
    else:
        return None

