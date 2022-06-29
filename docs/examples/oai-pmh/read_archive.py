import requests
import sys
import json
import urllib.parse
import xml.etree.ElementTree as ET

def base_data(ead, ref, archive_data):
    unitid = ref.find('./{*}unitid')
    archive_data['referenskod'] = unitid.text
    unittitle = ref.find('./{*}unittitle')
    if unittitle is not None:
        archive_data['titel'] = unittitle.text
    unitdate = ref.find('./{*}unitdate')
    if unitdate is not None:
        archive_data['datering'] = unitdate.text
    url_ref = ead.find('./{*}archdesc//{*}otherfindaid/{*}p/{*}extref')
    url = url_ref.attrib.get('{http://www.w3.org/1999/xlink}href')
    archive_data['persistent_id'] = url.split('/')[-1]
    archive_data['url'] = url
    for link in ead.findall('./{*}archdesc/{*}did/{*}dao'):
        role = link.attrib.get('{http://www.w3.org/1999/xlink}role')
        if role == 'IMAGE':
            archive_data['bildvisning'] = link.attrib.get('{http://www.w3.org/1999/xlink}href')
        elif role == 'MANIFEST':
            archive_data['iiif_manifest'] = link.attrib.get('{http://www.w3.org/1999/xlink}href')

def institution_data(ref, archive_data):
    eadid = ref.find('./{*}eadid')
    if eadid is not None:
        institution = eadid.attrib.get('mainagencycode')
        if institution is not None:
            institution = institution.replace('-', '/')
            archive_data['arkivinstitution'] = {
                'referenskod': institution,
                'url': f'https://sok.riksarkivet.se/nad?postid=ArkisRef+{urllib.parse.quote_plus(institution)}&type=2&s=balder'
            }


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


def restrict_data(ref, key, archive_data):
    if ref is not None:
        data = {}
        specification = ref.attrib.get('type')
        if specification is not None:
            data['omfattning'] = specification
        note = ref.find('./{*}p')
        if note is not None:
            if note.text is not None:
                data['anmärkning'] = note.text
            else: 
                extref = note.find('./{*}extref')
                if extref is not None:
                    data['anmärkning'] = extref.attrib.get('{http://www.w3.org/1999/xlink}href')
        all_restrict = archive_data.get('villkor')
        if all_restrict is None:
            all_restrict = {}
            archive_data['villkor'] = all_restrict
        all_restrict[key] = data


def unit_data(ead, unit_root, target_data):
    did = unit_root.find('./{*}did')
    if did is not None:
        base_data(ead, did, target_data)
        header = ead.find('./{*}eadheader')
        institution_data(header, target_data)
        origin_data(did, target_data)
        extent_data(did, target_data)
    restrict = archdesc.find('./{*}accessrestrict')
    restrict_data(restrict, 'åtkomst', target_data)
    restrict = archdesc.find('./{*}userestrict')
    restrict_data(restrict, 'användning', target_data)
    target_data['innehåll'] = []
    for child in unit_root.findall('./{*}dsc/{*}c'):
        child_data = {}
        unit_data(ead, child, child_data)
        target_data['innehåll'].append(child_data)
    for child in unit_root.findall('./{*}c'):
        child_data = {}
        unit_data(ead, child, child_data)
        target_data['innehåll'].append(child_data)
    if len(target_data['innehåll']) == 0:
        del(target_data['innehåll'])

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ref_code = urllib.parse.quote_plus(sys.argv[1])
        res = requests.get(f'https://oai-pmh-acc.riksarkivet.se/OAI?verb=GetRecord&identifier={ref_code}&metadataPrefix=oai_ape_ead')
        if res.status_code == 200:
            archive_data = {}
            tree = ET.fromstring(res.content)
            ead = tree.find('.//{*}ead')
            archdesc = ead.find('./{*}archdesc')
            unit_data(ead, archdesc, archive_data)
            print(json.dumps(archive_data, indent=3, ensure_ascii=False))
        else:
            print(f'Error: {res.status_code}')
    else:
        print('Usage: python refcode_to_pid.py <pid>')
