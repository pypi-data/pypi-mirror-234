
import sys

import easygui
import shapefile


def bounding_box(entity):
    """Computes the bounding box of a collection of points"""

    # Bounding box consists of computing min and max

    # Init bounding box
    x_min = entity[0][0]
    x_max = entity[0][0]
    y_min = entity[0][1]
    y_max = entity[0][1]

    for point in entity:
        x, y = point

        if x < x_min:
            x_min = x
        elif x > x_max:
            x_max = x

        if y < y_min:
            y_min = y
        elif y > y_max:
            y_max = y

    bounds = [x_min, y_min, x_max, y_max]

    return bounds


def point_in_rectangle(x, y, rectangle):
    """Returns True if point (x,y) lies within rectangle [x_min, y_min, x_max, y_max] and False otherwise"""

    inside = False

    xmin, ymin, xmax, ymax = rectangle

    if x >= xmin and x <= xmax and y >= ymin and y <= ymax:
        inside = True

    return inside


def point_in_polygon(x, y, polygon):
    """Returns True if point (x,y) lies within polygon and False otherwise"""
    
    is_inside = False

    for i in range(1, len(polygon)): # Scan all segments of polygon
        if y > min(polygon[i - 1][1], polygon[i][1]):
            # polygon[i - 1][1] = y coordinate of previous vertex
            # polygon[i][1] = y coordinate of current vertex
            # In this case there can be intersect
            if y <= max(polygon[i - 1][1], polygon[i][1]):
                # In this case there can be intersect
                if x <= max(polygon[i - 1][0], polygon[i][0]):
                    # In this case there can be intersect
                    if polygon[i - 1][1] != polygon[i][1]:
                        x_int = (polygon[i][0] - polygon[i - 1][0]) * \
                                (y - polygon[i - 1][1]) /      \
                                (polygon[i][1] - polygon[i - 1][1]) + \
                                polygon[i - 1][0]
                        if x <= x_int:
                            is_inside = not is_inside

    return is_inside


def point_in_multipart_polygon(x, y, polygon):
    """Returns True if point (x,y) lies within polygon and False otherwise"""
    
    is_inside = False

    for part in polygon:
        for i in range(1, len(part)):
            x1, y1 = part[i - 1]
            x2, y2 = part[i]
            
            if y > min(y1, y2) and y <= max(y1, y2) and y1 != y2 and x <= max(x1, x2):
                x_int = (((x2 - x1) * (y - y1)) / (y2 - y1)) + x1
                if x <= x_int:
                    is_inside = not is_inside

    return is_inside


def describe_shapefile(shapefilename=None):

    if 'shapefile' not in sys.modules.keys():
        print('climex.geo.describe_shapefile(): Package "shapefile" not found (pip install pyshp)')
        return
    
    if shapefilename is None:

        if 'easygui' not in sys.modules.keys():
            print('climex.geo.describe_shapefile(): Package "easygui" not found (pip install easygui)')
            return

        shapefilename = easygui.fileopenbox(
            default='*.shp', filetypes=['*.shp']
        )

    if shapefilename is None:
        return
    # TODO: CRS
    details = {
        'entity': None,
        'records': None,
        'fields': []
    }

    try:
        shape = shapefile.Reader(shapefilename)

        details['entity'] = shape.shapeTypeName
        details['records'] = shape.numRecords
        details['fields'] = shape.fields[1:]
    except:
        details = {}

    return details


##def read_shapefile(shapefilename=None):
##    """Reads a Shapefile dataset and returns the dataset in JSON format"""
##
##    if 'shapefile' not in sys.modules.keys():
##        print('climex.geo.describe_shapefile(): Package "shapefile" not found (pip install pyshp)')
##        return
##    
##    if shapefilename is None:
##
##        if 'easygui' not in sys.modules.keys():
##            print('climex.geo.describe_shapefile(): Package "easygui" not found (pip install easygui)')
##            return
##
##        shapefilename = easygui.fileopenbox(
##            default='*.shp', filetypes=['*.shp']
##        )
##
##    if shapefilename is None:
##        return
##    # TODO: CRS
##    vector = {
##        'type': None,
##        'fields': [],
##        'geometries': [],
##        'bbox': [],
##        'attributes': []
##    }
##
##    shape = shapefile.Reader(shapefilename)
##
##    vector['type'] = shape.shapeTypeName
##
##    for record in shape.shapeRecords():
##
##        vector['geometries'].append(record.shape.points)
##        vector['attributes'].append(record.record[:])
##
##        if vector['type'] in ['POLYLINE', 'POLYGON']:
##            vector['bbox'].append(
##                bounding_box(record.shape.points)
##            )
##
##    for field in shape.fields[1:]:
##        vector['fields'].append(field[0])
##    
##
##    return vector


def read_shapefile(shapefilename=None):
    """Reads a Shapefile dataset and returns the dataset in JSON format"""

    if 'shapefile' not in sys.modules.keys():
        print('climex.geo.describe_shapefile(): Package "shapefile" not found (pip install pyshp)')
        return
    
    if shapefilename is None:

        if 'easygui' not in sys.modules.keys():
            print('climex.geo.describe_shapefile(): Package "easygui" not found (pip install easygui)')
            return

        shapefilename = easygui.fileopenbox(
            default='*.shp', filetypes=['*.shp']
        )

    if shapefilename is None:
        return
    # TODO: CRS
    vector = {
        'type': None,
        'fields': [],
        'geometries': [],
        'bbox': [],
        'attributes': []
    }

    shape = shapefile.Reader(shapefilename)

    vector['type'] = shape.shapeTypeName

    for record in shape.shapeRecords():

        shifts = record.shape.parts
        shifts.append(len(record.shape.points))

        parts = []
        for i in range(1, len(shifts)):
            parts.append(record.shape.points[shifts[i - 1]:shifts[i]])
        
        vector['geometries'].append(parts)
        vector['attributes'].append(record.record[:])

##        if vector['type'] in ['POLYLINE', 'POLYGON']:
##            vector['bbox'].append(
##                bounding_box(record.shape.points)
##            )


        

    for field in shape.fields[1:]:
        vector['fields'].append(field[0])
    

    return vector


def read_ascii_grid(filename=None, data_type=int):
    """Reads a raster dataset in ARC/INFO ASCII GRID format"""

    grid = {
        'ncols': None,
        'nrows': None,
        'xllcorner': None,
        'yllcorner': None,
        'xllcenter': None,
        'yllcenter': None,
        'cellsize': None,
        'nodata_value': -9999,
        'data': []
    }

    with open(filename, 'rt') as  ascii_file:
        data_shift = 0
        for record in ascii_file.readlines():
            try:
                keyword, value = record.split()

                if keyword.lower() in grid.keys():
                    if keyword in ['ncols', 'nrows']:
                        grid[keyword.lower()] = int(value)
                    else:
                        grid[keyword.lower()] = float(value)

            except:
                if data_type == int:
                    tokens = list(map(int, record.split()))
                elif data_type == float:
                    tokens = list(map(float, record.split()))

                grid['data'].insert(0, tokens)
            
    if grid['ncols'] is None or grid['nrows'] is None or \
       grid['cellsize'] is None:
        grid = {}
    elif grid['xllcorner'] is None and grid['yllcorner'] is None and \
         grid['xllcenter'] is None and grid['yllcenter'] is None:
        grid = {}
    

    return grid
