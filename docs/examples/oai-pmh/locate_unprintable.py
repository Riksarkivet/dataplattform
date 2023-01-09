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
APE_EAD_NS = '{urn:isbn:1-931666-22-9}'

ET.register_namespace('', 'http://xml.ra.se/EAD')
ET.register_namespace('xlink', 'http://xml.ra.se/xlink')

data_errors = []
failed = []

def process_archive(archive_node, ref_code):
    local_id = archive_node.find(f'./{APE_EAD_NS}did/{APE_EAD_NS}unitid').text
    subarchive_ref_code = f'{ref_code}/{local_id}'
    #print(f'Underarkiv: {subarchive_ref_code}')
    series = archive_node.findall(f'./{APE_EAD_NS}c[@level="series"]')
    if series is not None:
        for series_node in series:
            local_id = series_node.find(f'./{APE_EAD_NS}did/{APE_EAD_NS}unitid').text
            series_ref_code = f'{subarchive_ref_code}/{local_id}'
            process_series(series_node, series_ref_code)

def process_series(series_node, ref_code):
    #print(f'Serie: {ref_code}')
    sub_series = series_node.findall(f'./{APE_EAD_NS}c[@level="series"]')
    if sub_series is not None:
        for sub_series_node in sub_series:
            local_id = sub_series_node.find(f'./{APE_EAD_NS}did/{APE_EAD_NS}unitid').text
            series_ref_code = f'{ref_code}/{local_id}'
            process_series(sub_series_node, series_ref_code)
    leaves = series_node.findall(f'./{APE_EAD_NS}c[@level="otherlevel"]')
    if leaves is not None:
        for leaf_node in leaves:
            local_id = leaf_node.find(f'./{APE_EAD_NS}did/{APE_EAD_NS}unitid').text
            leaf_ref_code = f'{ref_code}/{local_id}'
            txt_node = leaf_node.find(f'./{APE_EAD_NS}scopecontent/{APE_EAD_NS}p')
            if txt_node is not None:
                txt = txt_node.text
                re_result = re.search(r'!! (x[0-9a-fA-F]*) !!', txt)
                if re_result is not None:
                    url_node = leaf_node.find(f'./{APE_EAD_NS}otherfindaid/{APE_EAD_NS}p/{APE_EAD_NS}extref')
                    url = '' if url_node is None else url_node.attrib.get('{http://xml.ra.se/xlink}href')
                    print(f'{leaf_ref_code} [{url}] - {re_result.group(1)}')
            #print(f'Lövnod: {leaf_ref_code}')

def harvest_archive(ref_code):
    print(f'Harvesting {ref_code}')
    res = requests.get(f'https://oai-pmh.riksarkivet.se/OAI?verb=GetRecord&identifier={ref_code}&metadataPrefix=oai_ape_ead')
    if res.status_code == 200:
        print(f'Got {len(res.text)} bytes')
        file_name = f'./tmp/{ref_code.replace("/", "_")}.xml'
        xml_text = res.content
        re_result = re.search(r'&#(x[0-9a-fA-F]*);', xml_text.decode())
        if re_result is not None:
            xml_text = re.sub(r'&#x[0-9a-fA-F]*;', f'!! {re_result.group(1)} !!', xml_text.decode()).encode()
        if xml_text.find(str.encode('•')) > -1:
            xml_text = xml_text.replace(str.encode('•'), b'')
        oai_xml = ET.fromstring(xml_text)
        ead_xml = ET.ElementTree(element=oai_xml.find(f'./{OAI_NS}GetRecord/{OAI_NS}record/{OAI_NS}metadata/*'))
        #ead_xml.write(file_name, encoding='UTF-8', xml_declaration=True)
        sub_archives = ead_xml.findall(f'./{APE_EAD_NS}archdesc/{APE_EAD_NS}dsc/{APE_EAD_NS}c[@level="fonds"]')
        if sub_archives is not None:
            for archive_node in sub_archives:
                process_archive(archive_node, ref_code)
        series = ead_xml.findall(f'./{APE_EAD_NS}c[@level="series"]')
        for series_node in series:
            process_series(series_node, ref_code)

if __name__ == '__main__':
    ref_code = 'SE/RA/1214' #argv[1]
    harvest_archive(ref_code)
