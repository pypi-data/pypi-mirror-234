## CLIMEX Tutorial

Ángel Marqués-Mateu<sup>1</sup>, Azucena Pérez-Vega<sup>2</sup>, Adolfo Molada-Tebar<sup>3</sup>

<sup>1</sup> Universitat Politècnica de València (España) ([amarques@cgf.upv.es](mailto:amarques@cgf.upv.es))

<sup>2</sup> Universidad de Guanajuato (México)

<sup>3</sup> Universidad de Salamanca (España)

## Installation

CLIMEX can be installed using ```pip```

```python
$ pip install climex
```

## Introduction

CLIMEX is a Python package intended to support Climate Change computations and analyses from datasets hosted at the [CONAGUA](https://smn.conagua.gob.mx/) web site. CLIMEX is primarily intended to support climate research in México.

The typical workflow in CLIMEX takes the following steps:

1. Import CLIMEX

2. Create a CLIMEX project

3. Configure the set of stations and baseline

4. Download data files

5. Pass quality control

6. Compute climate indices

7. Export data to tabular or map formats

Sections below explain each step in detail.

## 1. Import CLIMEX

In order to use CLIMEX, import the package as usual:

```python
>>> import climex
```

When CLIMEX is imported for the first time, it creates a folder in the local disk and a number of files using contents from the CONAGUA web site.

## 2. Create a CLIMEX project

The CLIMEX package defines a number of classes, but users should interact with one only class named ```Project()```. There are different ways to create a project, the easiest is to create a new, empty project as follows:

```python
>>> test = climex.Project('test')
```

where ```'test'``` is a text string containing the name of the project. This line creates an instance of the class ```Project()``` which can be accesed by label ```test``` and a folder on the local disk to store data. In order to see the contents of the project, just type the variable name:

```python
>>> test
{
    "created": "2022-05-13 12:39:08",
    "updated": "2022-05-13 12:39:08",
    "operating": true,
    "baseline": [
        1961,
        1990
    ],
    "stations": []
}
```

At this point, the project is almost empty; it has creation and updating dates, a default baseline 1961-1990 and no stations.

## 3. Basic configuration: stations and baseline

The next step is to add stations to the project. In this example, we add several stations from Guanajuato with IDs 11020, 11025, 11040, 11045, 11053 and 11095. The `stations` property is used to add stations to the project.

```python
>>> test.stations = [11020, 11025, 11040, 11045, 11053]
>>> test
{
    "created": "2022-05-15 09:34:53",
    "updated": "2022-05-15 09:35:15",
    "operating": true,
    "baseline": [
        1961,
        1990
    ],
    "stations": [
        "11020",
        "11025",
        "11040",
        "11045",
        "11053"
    ]
}
```

Users can add more stations at any time. If we want to add a new station with ID=11095 we type the following line.

```python
>>> test.stations = 11095
>>> test
{
    "created": "2022-05-15 09:34:53",
    "updated": "2022-05-15 09:36:52",
    "operating": true,
    "baseline": [
        1961,
        1990
    ],
    "stations": [
        "11020",
        "11025",
        "11040",
        "11045",
        "11053",
        "11095"
    ]
}
```

The baseline can be updated using the corresponding `baseline` property.

```python
>>> test.baseline = [1971, 2000]
>>> test
{
    "created": "2022-05-15 09:34:53",
    "updated": "2022-05-15 09:38:33",
    "operating": true,
    "baseline": [
        1971,
        2000
    ],
    "stations": [
        "11020",
        "11025",
        "11040",
        "11045",
        "11053",
        "11095"
    ]
}
```

## 4. Download climate data

After tuning the parameters of the project, the next step is to download the data from the CONAGUA web site using the `.download()` method of the `Project()` instance.

```python
>>> test.download()
Downloading  https://smn.conagua.gob.mx/tools/RESOURCES/Diarios/11020.txt       [200]
Downloading  https://smn.conagua.gob.mx/tools/RESOURCES/Diarios/11025.txt       [200]
Downloading  https://smn.conagua.gob.mx/tools/RESOURCES/Diarios/11040.txt       [200]
Downloading  https://smn.conagua.gob.mx/tools/RESOURCES/Diarios/11045.txt       [200]
Downloading  https://smn.conagua.gob.mx/tools/RESOURCES/Diarios/11053.txt       [200]
Downloading  https://smn.conagua.gob.mx/tools/RESOURCES/Diarios/11095.txt       [200]
```

The label ```[200]``` means that the corresponding HTTP request worked well. However, it should be noted that network transactions (the download of files being a good example) can fail due to server side causes that are out of user control. Particularly, if you see any SSL related issues, please go to [SSL](http://personales.upv.es/amarques/CLIMEX/climex_ssl.md.html) link and check the details to install the SSL certificate in the Python local environment.

Users can check the contents in the project folder. In order to keep track of the files in a project we can use the `contents()` method.

```python
>>> test.contents()

[/home/climex/.climex/PROJECTS/CEAG/CONAGUA]

   11020.txt
   11025.txt
   11040.txt
   11045.txt
   11053.txt
   11095.txt

[/home/climex/.climex/PROJECTS/CEAG/CLIMDEX]

   11020.txt
   11020_1971_2000.txt
   11025.txt
   11025_1971_2000.txt
   11040.txt
   11040_1971_2000.txt
   11045.txt
   11045_1971_2000.txt
   11053.txt
   11053_1971_2000.txt
   11095.txt
   11095_1971_2000.txt
```

The output of `contents()` shows that there are files in two 
subfolders with datasets in two formats:

1. The original CONAGUA format
2. The well-known Climdex input format (See [Climdex User's Guide. Appendix C](http://etccdi.pacificclimate.org/ClimDex/climdex-v1-3-users-guide.pdf))

Note that in the particular case of the Climdex format, there is a file per station with data in the baseline period, in addition to the file with all the data. Filenames provide an overview of the file contents. 

## 5. Quality control

After the data download, it is convenient to check for missing data and other mistakes using the ```.qc()``` method. This method accepts a named plot parameter to create plots of the time series. Note that creating the plot graphical files may take a while.

```python
>>> test.qc(plot=True)
Running QC on station "11020"    [OK]
Running QC on station "11025"    [OK]
Running QC on station "11040"    [OK]
Running QC on station "11045"    [OK]
Running QC on station "11053"    [OK]
Running QC on station "11095"    [OK]
```

The ```.qc()``` method generates new files in the folder structure of the project. We can locate those files using ```contents()```.

```python
>>> test.contents()
   ...
   ...

[/home/climex/.climex/PROJECTS/CEAG/QC]

   11020_1971_2000_qc0.json
   11020_1971_2000_qc_prcp.png
   11020_1971_2000_qc_temp.png
   11025_1971_2000_qc0.json
   11025_1971_2000_qc_prcp.png
   11025_1971_2000_qc_temp.png
   11040_1971_2000_qc0.json
   11040_1971_2000_qc_prcp.png
   11040_1971_2000_qc_temp.png
   11045_1971_2000_qc0.json
   11045_1971_2000_qc_prcp.png
   11045_1971_2000_qc_temp.png
   11053_1971_2000_qc0.json
   11053_1971_2000_qc_prcp.png
   11053_1971_2000_qc_temp.png
   11095_1971_2000_qc0.json
   11095_1971_2000_qc_prcp.png
   11095_1971_2000_qc_temp.png
```

There is a JSON file and two PNG files per station. Plots in PNG files allow easily detecting missing data which are plotted in grey colour, whereas precipitation and temperature data that are plotted in blue or red. Figure 1 shows several years from 1992 to 1997 with very few data (some of those years have actually no available data).

## 6. Compute climate indices

The list of common indices in climate change research are located in the [Climdex](https://www.climdex.org/learn/indices/) web site. There are 17 heat/cold indices and 13 precipitation indices.

The CLIMEX module provides information about climate indices by means of the ```info()``` function. In order to see the whole list of indices run this functions without any arguments:

```python
>>> climex.info()
['FD', 'SU', 'ID', 'TR', 'GSL', 'TXX', 'TNX', 'TXN', 'TNN', 'TN10P', 'TX10P', 'TN90P', 'TX90P', 'WSDI', 'CSDI', 'DTR', 'ETR', 'RX1DAY', 'RX5DAY', 'SDII', 'R10MM', 'R20MM', 'RNNMM', 'CDD', 'CWD', 'R95P', 'R99P', 'R95PTOT', 'R99PTOT', 'PRCPTOT']
```

The detailed explanation of a given index is available by providing the specific index name as a parameter to function ```info()```:

```python
>>> climex.info('su')

SU: Number of summer days

Annual count of days when TX (daily maximum temperature) > 25 °C. Let TXij be 
daily minimum temperature on day i in year j. Count the number of days where 
TXij > 25°C.
```

The ```Project()``` class has a ```.compute_index()``` method that conducts all the computations needed to determine climate indices. This method requires the name of the index to be computed and can optionally create plots of the indices. The following line computes the SU index at all stations of the project and create the corresponding plots.

```python
>>> test.compute_index('su', plot=True)
Computing index "SU" on station "11020"        [OK]
Computing index "SU" on station "11025"        [OK]
Computing index "SU" on station "11040"        [OK]
Computing index "SU" on station "11045"        [OK]
Computing index "SU" on station "11053"        [OK]
Computing index "SU" on station "11095"        [OK]
```

The output of the ```.compute_index()``` method consists of JSON and PNG files. There is a JSON, and optionally a PNG file, per any station/index pair. Output files can be listed using ```.contents()``` as in previous examples.

```python
>>> test.contents()

...

[/home/climex/.climex/PROJECTS/TEST/INDEX]

   11020_1971_2000_02_SU.json
   11020_1971_2000_02_SU.png
   11025_1971_2000_02_SU.json
   11025_1971_2000_02_SU.png
   11040_1971_2000_02_SU.json
   11040_1971_2000_02_SU.png
   11045_1971_2000_02_SU.json
   11045_1971_2000_02_SU.png
   11053_1971_2000_02_SU.json
   11053_1971_2000_02_SU.png
   11095_1971_2000_02_SU.json
   11095_1971_2000_02_SU.png

...
```

Figure 2 contains the graphical output of the SU index. Note the absence of data points in years 1992 to 1997. The plot includes the data and the regression line so that users can see the trend of the index over the years (for a discussion of hypotehsis testing of the regression slope see this [stattrek](https://stattrek.com/regression/slope-test.aspx) link).

Another useful way of visualising climate data is by using a map. CLIMEX provides basic map visualisation with the method `.osm()` using the [OSM](https://www.openstreetmap.org/) base map on an HTML file: 

```
>>> test.osm(browser=True, climate_index='su', missing=True)
```

The`.osm()` method has three parameters to:

1. Show the HTML code on a web browser. The default value is True, which means that the HTML will be shown on the default wbe browser in the local system. Set to False only specific working environments such as Jupyter, which do not need a browser to render HTML files.
2. Set the climate index data joined to weather stations.
3. Print points in different colours, depending on the number of missing data in the climate index dataset.

The result of `.osm()` is an HTML point [map]((http://personales.upv.es/amarques/CLIMEX/climex_map.html)) of the stations included in the project.

## 7. Export

The last step in a CLIMEX project is to export the data to a specific format. The `export()` method allows exporting geographic coordinates, index values and other 
attributes to CSV, GeoJSON and Spahefile formats. These formats allows users to process climate datasets in other computing environments and combine them with other external datasets. Statistical packages and geographic information systems are known examples of such computing environments.

```python

```

## 8. SSL certificates
