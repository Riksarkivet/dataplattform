import requests
import sys
import json
import urllib.parse
import xml.etree.ElementTree as ET

def base_data(ead, ref, archive_data):
    unitid = ref.find('./{*}unitid')
    archive_data['referenskod'] = unitid.text
    unittitle = ref.find('./{*}unittitle')
    archive_data['titel'] = unittitle.text
    unitdate = ref.find('./{*}unitdate')
    if unitdate is not None:
        archive_data['datering'] = unitdate.text
    url_ref = ead.find('./{*}archdesc//{*}otherfindaid/{*}p/{*}extref')
    url = url_ref.attrib.get('{http://www.w3.org/1999/xlink}href')
    archive_data['persistent_id'] = url.split('/')[-1]
    archive_data['url'] = url


def origin_data(ref, archive_data):
    origin = ref.find('./{*}origination/{*}corpname')
    if origin is not None:
        origin_data = {}
        origin_data['namn'] = origin.text
        origin_refcode = origin.attrib.get('authfilenumber')
        if origin_refcode is not None:
            origin_data['referenskod'] = origin_refcode
            origin_data['url'] = f'https://sok.riksarkivet.se/?postid=ArkisRef+{urllib.parse.quote_plus(origin_refcode)}'
        archive_data['arkivbildare'] = origin_data


def extent_data(ref, archive_data):
    extent = ref.find('./{*}physdesc/{*}extent')
    if extent is not None:
        archive_data['omfång'] = f'{extent.text} {extent.attrib.get("unit")}'


def restrict_data(ref, archive_data):
    if ref is not None:
        data = {}
        data['omfattning'] = ref.attrib.get('type')
        note = ref.find('./{*}p')
        if note is not None:
            data['anmärkning'] = note.text
        archive_data['villkor'] = data


if __name__ == "__main__":
    if len(sys.argv) > 1:
        ref_code = urllib.parse.quote_plus(sys.argv[1])
        res = requests.get(f'https://oai-pmh.riksarkivet.se/OAI?verb=GetRecord&identifier={ref_code}&metadataPrefix=oai_ape_ead')
        if res.status_code == 200:
            archive_data = {}
            tree = ET.fromstring(res.content)
            ead = tree.find('.//{*}ead')
            did = ead.find('./{*}archdesc/{*}did')
            if did is not None:
                base_data(ead, did, archive_data)
                origin_data(did, archive_data)
                extent_data(did, archive_data)
            restrict = ead.find('./{*}archdesc/{*}userestrict')
            restrict_data(restrict, archive_data)
            print(json.dumps(archive_data, indent=3))
        else:
            print(f'Error: {res.status_code}')
    else:
        print('Usage: python refcode_to_pid.py <pid>')
