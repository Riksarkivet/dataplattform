import requests
import sys
import urllib.parse
import xml.etree.ElementTree as ET

if __name__ == "__main__":
    if len(sys.argv) > 1:
        res = requests.get(f'https://oai-pmh.riksarkivet.se/OAI?verb=GetRecord&identifier={urllib.parse.quote_plus(sys.argv[1])}&metadataPrefix=oai_ape_ead')
        if res.status_code == 200:
            tree = ET.fromstring(res.content)
            ref = tree.find('.//{*}ead/{*}archdesc/{*}otherfindaid/{*}p/{*}extref')
            if ref is not None:
                ref_url = ref.attrib.get('{http://www.w3.org/1999/xlink}href')
                print(f'Reference code: {ref_url.split("/")[-1]}')
            else:
                print('Cannot find PID reference')
        else:
            print(f'Error: {res.status_code}')
    else:
        print('Usage: python refcode_to_pid.py <pid>')
