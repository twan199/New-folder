import xml.etree.ElementTree as ET
from xml.dom import minidom
from bs4 import BeautifulSoup
import csv
import glob
import os.path
import pandas as pd
from geopy.geocoders import Nominatim
# import country_converter as coco
import shutil


def find_country(coordinates):
    geolocator = Nominatim(user_agent="foo_bar")
    location = geolocator.reverse(
        coordinates, language='en', timeout=None)
    country = location.address.split(',')[-1].strip()
    # country_code = coco.convert(country, to='ISO3', not_found=None)
    # print(country_code)
    # if not os.path.exists(f'//ChickenServer/Data/GPX files/{country}/{newname}'):
    #     shutil.move(
    #         filename, f'//ChickenServer/Data/GPX files/{country}/{newname}')
    #     print(country + "---" + newname + "\n")
    return country


def create_placemark(name, coordinates):
    placemark = ET.SubElement(document, 'Placemark')
    ET.SubElement(placemark, 'name').text = name
    style = ET.SubElement(placemark, 'Style')
    icon_style = ET.SubElement(style, 'IconStyle')
    ET.SubElement(icon_style, 'scale').text = '0.9'
    icon = ET.SubElement(icon_style, 'Icon')
    ET.SubElement(
        icon, 'href').text = 'https://maps.google.com/mapfiles/kml/paddle/red-circle.png'
    point = ET.SubElement(placemark, 'Point')
    ET.SubElement(point, 'extrude').text = '0'
    ET.SubElement(point, 'altitudeMode').text = 'clampToGround'
    ET.SubElement(point, 'coordinates').text = coordinates


listofcsv = (glob.glob("export/*.csv"))

country_list = []
for i in listofcsv:
    df = pd.read_csv(i)
    newfilename = i.split("_")[1][:-4] + ".kml"
    df["Country"] = ""
    for index, row in df.iterrows():
        df.loc[index, "Country"] = find_country([row["lat"], row["long"]])
    for country in df['Country'].unique():
        print(country)
        df1 = df.loc[df['Country'] == country]
        # Create the root element <kml>
        kml = ET.Element('kml', attrib={
            "xmlns": "http://www.opengis.net/kml/2.2",
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xmlns:kmlx": "http://www.google.com/kml/ext/2.2",
            "xmlns:atom": "http://www.w3.org/2005/Atom",
            "xmlns:gpxx": "http://www.garmin.com/xmlschemas/GpxExtensions/v3"
        })
        # Create the <Document> element
        document = ET.SubElement(kml, 'Document')
        # Add name to the Document element
        ET.SubElement(document, 'name').text = newfilename[:-4]
        # Create the <Style> element
        style = ET.SubElement(document, 'Style', id="point")
        icon_style = ET.SubElement(style, 'IconStyle')
        ET.SubElement(icon_style, 'scale').text = '0.9'
        icon = ET.SubElement(icon_style, 'Icon')
        ET.SubElement(
            icon, 'href').text = 'https://maps.google.com/mapfiles/kml/paddle/red-circle.png'

        # Create <Placemark> elements

        # description = i.split("_")[1][:-4]
        for index, row in df1.iterrows():
            name = row["Name"]
            lat = row["lat"]
            long = row["long"]
            create_placemark(name, str(long) + "," + str(lat))

        # Create XML string
        tree = ET.ElementTree(kml)
        xml_str = ET.tostring(kml, encoding='utf-8', method='xml')
        xml_str_pretty = minidom.parseString(xml_str).toprettyxml(indent="  ")
        # if not os.path.exists(f'export/{country}'):
        #     os.makedirs(f'export/{country}/')
        # with open(f'export/{country}/{newfilename}', 'w', encoding='utf-8') as f:
        #     f.write(xml_str_pretty)
        if not os.path.exists(f'//ChickenServer/Data/GPX files/{country}'):
            os.makedirs(f'//ChickenServer/Data/GPX files/{country}/')
        with open(f'//ChickenServer/Data/GPX files/{country}/{newfilename}', 'w', encoding='utf-8') as f:
            f.write(xml_str_pretty)
