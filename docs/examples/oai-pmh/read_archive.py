import requests
import sys
import json
import urllib.parse
import xml.etree.ElementTree as ET


# Extrahera grunddata, referenskod, typ, titel, datering och länkar
#
def base_data(ead, ref, unit_type, archive_data):
    unitid = ref.find('./{urn:isbn:1-931666-22-9}unitid')
    archive_data['referenskod'] = unitid.text
    if unit_type is not None:
        archive_data['arkivenhetstyp'] = unit_type.capitalize()
    unittitle = ref.find('./{urn:isbn:1-931666-22-9}unittitle')
    if unittitle is not None:
        archive_data['titel'] = unittitle.text
    unitdate = ref.find('./{urn:isbn:1-931666-22-9}unitdate')
    if unitdate is not None:
        archive_data['datering'] = unitdate.text
    url_ref = ead.find('./{urn:isbn:1-931666-22-9}archdesc//{urn:isbn:1-931666-22-9}otherfindaid/{urn:isbn:1-931666-22-9}p/{urn:isbn:1-931666-22-9}extref')
    url = url_ref.attrib.get('{http://www.w3.org/1999/xlink}href')
    archive_data['persistent_id'] = url.split('/')[-1]
    archive_data['url'] = url
    for link in ead.findall('./{urn:isbn:1-931666-22-9}archdesc/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}dao'):
        role = link.attrib.get('{http://www.w3.org/1999/xlink}role')
        if role == 'IMAGE':
            archive_data['bildvisning'] = link.attrib.get('{http://www.w3.org/1999/xlink}href')
        elif role == 'MANIFEST':
            archive_data['iiif_manifest'] = link.attrib.get('{http://www.w3.org/1999/xlink}href')


# Extrahera data om arkivinstitution
#
def institution_data(ref, archive_data):
    eadid = ref.find('./{urn:isbn:1-931666-22-9}eadid')
    if eadid is not None:
        institution = eadid.attrib.get('mainagencycode')
        if institution is not None:
            institution = institution.replace('-', '/')
            archive_data['arkivinstitution'] = {
                'referenskod': institution,
                'url': f'https://sok.riksarkivet.se/nad?postid=ArkisRef+{urllib.parse.quote_plus(institution)}&type=2&s=balder'
            }


# Extrahera data om arkivbildare, organisation eller person
def origin_data(ref, archive_data):
    origin = ref.find('./{urn:isbn:1-931666-22-9}origination/{urn:isbn:1-931666-22-9}corpname')
    if origin is None:
        origin = ref.find('./{urn:isbn:1-931666-22-9}origination/{urn:isbn:1-931666-22-9}persname')
    if origin is not None:
        origin_data = {}
        origin_data['namn'] = origin.text
        origin_refcode = origin.attrib.get('authfilenumber')
        if origin_refcode is not None:
            origin_data['referenskod'] = origin_refcode
            origin_data['url'] = f'https://sok.riksarkivet.se/?postid=ArkisRef+{urllib.parse.quote_plus(origin_refcode)}'
        archive_data['arkivbildare'] = origin_data


# Extrahera data om omfång
#
def extent_data(ref, archive_data):
    extent = ref.find('./{urn:isbn:1-931666-22-9}physdesc/{urn:isbn:1-931666-22-9}extent')
    if extent is not None:
        archive_data['omfång'] = f'{extent.text} {extent.attrib.get("unit")}'


# Extrahera data om villkor för åtkomst och användning
#
def restrict_data(ref, key, archive_data):
    if ref is not None:
        data = {}
        specification = ref.attrib.get('type')
        if specification is not None:
            data['omfattning'] = specification
        note = ref.find('./{urn:isbn:1-931666-22-9}p')
        if note is not None:
            if note.text is not None:
                data['anmärkning'] = note.text
            else: 
                extref = note.find('./{urn:isbn:1-931666-22-9}extref')
                if extref is not None:
                    data['anmärkning'] = extref.attrib.get('{http://www.w3.org/1999/xlink}href')
        all_restrict = archive_data.get('villkor')
        if all_restrict is None:
            all_restrict = {}
            archive_data['villkor'] = all_restrict
        all_restrict[key] = data


# Bestäm eller extrapolera arkivenhetstyp
# Som EAD ser ut är tillgängliga data <archdesc level="fonds" type="inventory"...
# för den översta nivån, oavsett om det är ett arkiv, en serie eller en volym
# eller annan "detaljpost". Då måste man gissa typen utifrån referenskoden. I
# normalfallet har ett arkiv tre komponenter, t.ex. SE/KrA/0425 och en serie
# fyra komponenter, t.ex. SE/ULA/10012/A I. Om det finns underarkiv eller
# underserier blir det dock fel, t.ex. SE/RA/720767/III/01 smo är ett (under-)
# arkiv men noteras som detaljnivå här.
# För underliggande arkivenheter finns
# <c level="series"... och <c level="otherlevel" otherlevel="volym" etc.
#
def unit_type(unit_root):
    type = unit_root.attrib.get('otherlevel')
    if type is None:
        type = unit_root.attrib.get('level')
        if type is not None:
            type = {
                'series': 'serie'
            }.get(type)
    if type is None:
        ref_code = unit_root.find('./{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unitid').text
        part_count = len(ref_code.split('/'))
        if part_count == 3:
            type = 'arkiv'
        elif part_count == 4:
            type = 'serie'
        else:
            type = 'detaljnivå: volym, karta/ritning etc.'
    return type


# Extrahera data om en arkivenhet från EAD-XML
#
def unit_data(ead, unit_root, no_children, target_data):
    did = unit_root.find('./{urn:isbn:1-931666-22-9}did')
    if did is not None:
        base_data(ead, did, unit_type(unit_root), target_data)
        header = ead.find('./{urn:isbn:1-931666-22-9}eadheader')
        institution_data(header, target_data)
        origin_data(did, target_data)
        extent_data(did, target_data)
    restrict = archdesc.find('./{urn:isbn:1-931666-22-9}accessrestrict')
    restrict_data(restrict, 'åtkomst', target_data)
    restrict = archdesc.find('./{urn:isbn:1-931666-22-9}userestrict')
    restrict_data(restrict, 'användning', target_data)
    if not no_children:
        # Extrahera data om underliggande arkivenheter (serier, volymer etc)
        target_data['innehåll'] = []
        for child in unit_root.findall('./{urn:isbn:1-931666-22-9}dsc/{urn:isbn:1-931666-22-9}c'):
            child_data = {}
            unit_data(ead, child, False, child_data)
            target_data['innehåll'].append(child_data)
        for child in unit_root.findall('./{urn:isbn:1-931666-22-9}c'):
            child_data = {}
            unit_data(ead, child, False, child_data)
            target_data['innehåll'].append(child_data)
        if len(target_data['innehåll']) == 0:
            del(target_data['innehåll'])


#
# Kommandoradsparametrar:
#    <referenskod>  Referenskod för arkivenheten, t.ex. "SE/KrA/0425"
#    j              Valfri, för att returnera endast en nivå utan underliggande arkivenheter
#
if __name__ == "__main__":
    if len(sys.argv) > 1:
        ref_code = urllib.parse.quote_plus(sys.argv[1])
        # Hämta data med OAI-PMH GetRecord
        res = requests.get(f'https://oai-pmh.riksarkivet.se/OAI?verb=GetRecord&identifier={ref_code}&metadataPrefix=oai_ape_ead')
        if res.status_code == 200:
            archive_data = {}
            tree = ET.fromstring(res.content)
            ead = tree.find('.//{urn:isbn:1-931666-22-9}ead')
            archdesc = ead.find('./{urn:isbn:1-931666-22-9}archdesc')
            no_children = len(sys.argv) > 2 and sys.argv[2].lower() == 'j'
            unit_data(ead, archdesc, no_children, archive_data)
            print(json.dumps(archive_data, indent=3, ensure_ascii=False))
        else:
            print(f'HTTP-fel: {res.status_code}')
    else:
        print('Användning: python refcode_to_pid.py <pid> [j]')
