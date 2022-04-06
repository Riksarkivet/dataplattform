import requests
import sys
import json
import zipfile
import re
import os


URL_BASE = 'https://lbiiif.riksarkivet.se/collection/arkiv/'


def process_collection(collection, zip_file):
    for item in collection.get('items', []):
        res = requests.get(item.get('id'))
        if res.status_code == 200:
            item_json = res.json()
            if item.get('type') == 'Collection':
                process_collection(item_json, zip_file)
            else:
                process_manifest(item_json, zip_file)

def process_manifest(manifest, zip_file):
    for canvas in manifest.get('items', []):
        for annotation_page in canvas.get('items', []):
            for annotation in annotation_page.get('items', []):
                image_url = annotation.get('body', {}).get('id')
                if image_url:
                    regex = re.compile('.*\!(.*)\/full.*')
                    result = regex.match(image_url)
                    if result:
                        image_id = result.group(1)
                        try:
                            file_name = f'{image_id}.jpg'
                            print(f'Processing {file_name}')
                            download_file(image_url, file_name)
                            zip_file.write(file_name, file_name)
                            os.remove(file_name)
                        except Exception as e:
                            print(e)

def download_file(url, file_name):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(file_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)

def main():
    if len(sys.argv) > 1:
        pid = sys.argv[1]
        res = requests.get(f'{URL_BASE}{pid}')
        if res.status_code == 200:
            collection = res.json()
            with zipfile.ZipFile(f'{pid}.zip', 'w') as zip_file:
                process_collection(collection, zip_file)
    else:
        print('Usage dowload <pid>')

if __name__== "__main__":
    main()
