import xml.etree.ElementTree as ET
from xml.dom import minidom
from bs4 import BeautifulSoup
import csv
import glob
import os.path
import pandas as pd


listofcsv = (glob.glob("export/*.csv"))


def create_placemark(name, coordinates):
    placemark = ET.SubElement(document, 'Placemark')
    ET.SubElement(placemark, 'name').text = name
    style = ET.SubElement(placemark, 'Style')
    icon_style = ET.SubElement(style, 'IconStyle')
    ET.SubElement(icon_style, 'scale').text = '0.9'
    icon = ET.SubElement(icon_style, 'Icon')
    ET.SubElement(
        icon, 'href').text = 'http://maps.google.com/mapfiles/kml/pushpin/blue-pushpin.png'
    point = ET.SubElement(placemark, 'Point')
    ET.SubElement(point, 'extrude').text = '0'
    ET.SubElement(point, 'altitudeMode').text = 'clampToGround'
    ET.SubElement(point, 'coordinates').text = coordinates


for i in listofcsv:
    df = pd.read_csv(i)
    newfilename = i.split("_")[1][:-4] + ".kml"
#     kmlfile = """<?xml version="1.0" encoding="utf-8"?>
# <kml xmlns="http://www.opengis.net/kml/2.2"
#      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
#      xmlns:kmlx="http://www.google.com/kml/ext/2.2"
#      xmlns:atom="http://www.w3.org/2005/Atom"
#      xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3">
#     <Document>
#         <Style id="point">
#             <IconStyle>
#                 <scale>0.9</scale>
#                 <Icon>
#                     <href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href>
#                 </Icon>
#             </IconStyle>
#         </Style>
#         <Folder>
#             <name>Waypoints</name>"""

    # description = i.split("_")[1][:-4]
    # for index, row in df.iterrows():
    #     name = row["Name"]
    #     lat = row["lat"]
    #     long = row["long"]

#         kmlfile = kmlfile + (f"""
#             <Placemark>
#                 <name>{name}</name>
#                 <Style>
#                     <IconStyle>
#                         <scale>0.9</scale>
#                         <Icon>
#                             <href>http://maps.google.com/mapfiles/kml/pushpin/blue-pushpin.png</href>
#                         </Icon>
#                     </IconStyle>
#                 </Style>
#                 <Point>
#                     <extrude>0</extrude>
#                     <altitudeMode>clampToGround</altitudeMode>
#                     <coordinates>{long},{lat}</coordinates>
#                 </Point>
#             </Placemark>""")
#     kmlfile = kmlfile + ("""</Folder>
#     </Document>
# </kml>""")

#     bs = BeautifulSoup(open(kmlfile), 'lxml', from_encoding='utf-8')
#     pretty_xml = bs.prettify()
#     with open(f'export/{newfilename}', 'w', encoding="utf-8") as f:
#         f.write(str(pretty_xml))

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
        icon, 'href').text = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'

    # Create <Placemark> elements

    # description = i.split("_")[1][:-4]
    for index, row in df.iterrows():
        name = row["Name"]
        lat = row["lat"]
        long = row["long"]
        create_placemark(name, str(long) + "," + str(lat))

    # Create XML string
    tree = ET.ElementTree(kml)
    xml_str = ET.tostring(kml, encoding='utf-8', method='xml')
    xml_str_pretty = minidom.parseString(xml_str).toprettyxml(indent="  ")
    with open(f'export/{newfilename}', 'w', encoding='utf-8') as f:
        f.write(xml_str_pretty)
        # tree.write(f, encoding="utf-8")
    # Print or save the XML string
    # print(xml_str.decode('utf-8'))


# Pretty print the XML string
