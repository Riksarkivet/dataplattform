import requests
import os
from sys import argv
import json
import urllib.parse
import xml.etree.ElementTree as ET
import re
from datetime import datetime

OAI_NS = '{http://www.openarchives.org/OAI/2.0/}'
RA_EAD_NS = '{http://xml.ra.se/EAD}'

ET.register_namespace('', 'http://xml.ra.se/EAD')
ET.register_namespace('xlink', 'http://xml.ra.se/xlink')

data_errors = []
failed = []

def harvest_archive(ref_code):
    print(f'Harvesting {ref_code}')
    res = requests.get(f'https://oai-pmh.riksarkivet.se/OAI?verb=GetRecord&identifier={ref_code}&metadataPrefix=oai_ra_ead')
    if res.status_code == 200:
        print(f'Got {len(res.text)} bytes')
        file_name = f'./tmp/{ref_code.replace("/", "_")}.xml'
        xml_text = res.content
        re_result = re.search(r'&#(x[0-9a-fA-F]*);', xml_text.decode())
        if re_result is not None:
            xml_text = re.sub(r'&#x[0-9a-fA-F]*;', f'[[{re_result.group(1)}]]', xml_text.decode()).encode()
        if xml_text.find(str.encode('•')) > -1:
            xml_text = xml_text.replace(str.encode('•'), b'')
        oai_xml = ET.fromstring(xml_text)
        ead_xml = ET.ElementTree(element=oai_xml.find(f'./{OAI_NS}GetRecord/{OAI_NS}record/{OAI_NS}metadata/*'))
        #ead_xml.write(file_name, encoding='UTF-8', xml_declaration=True)
        sub_archives = ead_xml.findall(f'./{RA_EAD_NS}archdesc/{RA_EAD_NS}dsc/{RA_EAD_NS}c[@level="fonds"]')
        pass

if __name__ == '__main__':
    ref_code = 'SE/RA/1214' #argv[1]
    harvest_archive(ref_code)
