import requests
import os
import zipfile
import json
import urllib.parse
import xml.etree.ElementTree as ET
import re
from datetime import datetime

top_codes = [
    'SE_RA',
    'SE_KrA',
    'SE_GLA',
    'SE_HLA',
    'SE_LLA',
    'SE_ULA',
    'SE_VALA',
    'SE_ViLA',
    'SE_ÖLA'
    # 'SE_ViLA'
]

OAI_NS = '{http://www.openarchives.org/OAI/2.0/}'

ET.register_namespace('', 'http://xml.ra.se/EAD')
ET.register_namespace('xlink', 'http://xml.ra.se/xlink')

data_errors = []
failed = []

def harvest_archive(top_code, ref_code, zip):
    print(f'Harvesting {top_code}/{ref_code}')
    res = requests.get(f'https://oai-pmh.riksarkivet.se/OAI?verb=GetRecord&identifier={ref_code}&metadataPrefix=oai_ra_ead')
    if res.status_code == 200:
        print(f'Got {len(res.text)} bytes')
        file_name = f'./{top_code}/{ref_code.replace("/", "_")}.xml'
        xml_text = res.content
        re_result = re.search(r'(&#x[0-9a-fA-F]*;)', xml_text.decode())
        if re_result is not None:
            data_errors.append((ref_code, re_result.group(0)))
            xml_text = re.sub(r'&#x[0-9a-fA-F]*;', '', xml_text.decode()).encode()
        if xml_text.find(str.encode('•')) > -1:
            data_errors.append((ref_code, '•'))
            xml_text = xml_text.replace(str.encode('•'), b'')
        oai_xml = ET.fromstring(xml_text)
        ead_xml = ET.ElementTree(element=oai_xml.find(f'./{OAI_NS}GetRecord/{OAI_NS}record/{OAI_NS}metadata/*'))
        ead_xml.write(file_name, encoding='UTF-8', xml_declaration=True)
        if os.path.isfile(file_name):
            zip.write(file_name, compress_type=zipfile.ZIP_DEFLATED)


def run_harvest(code, zip):
    res = requests.get(f'https://oai-pmh.riksarkivet.se/OAI/{code}?verb=ListIdentifiers')
    if res.status_code == 200:
        oai_xml = ET.fromstring(res.content)
        for id_elem in oai_xml.findall(f'./{OAI_NS}ListIdentifiers/{OAI_NS}header/{OAI_NS}identifier'):
            remaining_tries = 3
            while remaining_tries > 0:
                try:
                    harvest_archive(code, id_elem.text, zip)
                    remaining_tries = 0
                except:
                    remaining_tries = remaining_tries - 1
                    if remaining_tries == 0:
                        failed.append(code)

def harvest_all():
    if not os.path.isdir('./tmp'):
        os.makedirs('./tmp')
    zip = zipfile.ZipFile(f'./tmp/Riksarkivet-{datetime.today().strftime("%Y-%m-%d")}.zip', 'w')
    for code in top_codes:
        dir_name = f'./tmp/{code}'
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name)
        os.chdir('./tmp')
        run_harvest(code, zip)
        os.chdir('..')
    zip.close()

if __name__ == "__main__":
    harvest_all()
    print('Data errors:')
    for data_error in data_errors:
        print(f'{data_error[0]}, character {data_error[1]}')
    print('Failed:')
    for failed_harvest in failed:
        print(failed_harvest)