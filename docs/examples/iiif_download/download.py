import re
import sys
import zipfile

import httpx #pip install "httpx[http2]"

URL_BASE = 'https://lbiiif.riksarkivet.se/collection/arkiv/'
IMAGE_ID_RE = re.compile(r'.*!(.*)/full.*')

def get_json(client, url):
    try:
        response = client.get(url)
        response.raise_for_status()
        return response.json()
    except (httpx.HTTPError, ValueError) as e:
        print(f'Could not fetch {url}: {e}')
        return None

def process_collection(client, collection, zip_file):
    for item in collection.get('items', []):
        item_json = get_json(client, item['id'])
        if item_json is None:
            continue

        if item.get('type') == 'Collection':
            process_collection(client, item_json, zip_file)
        elif item.get('type') == 'Manifest':
            process_manifest(client, item_json, zip_file)

def process_manifest(client, manifest, zip_file):
    for canvas in manifest.get('items', []):
        for annotation_page in canvas.get('items', []):
            for annotation in annotation_page.get('items', []):
                image_url = annotation.get('body', {}).get('id')
                if not image_url:
                    continue

                match = IMAGE_ID_RE.match(image_url)
                if not match:
                    continue

                file_name = f'{match.group(1)}.jpg'
                download_image(client, image_url, file_name, zip_file)

def download_image(client, url, file_name, zip_file):
    print(f'Downloading {file_name}')
    try:
        response = client.get(url)
        response.raise_for_status()
        zip_file.writestr(file_name, response.content)
    except httpx.HTTPError as e:
        print(f'Could not download {file_name}: {e}')

def main():
    if len(sys.argv) != 2:
        print('Usage: python download.py <pid>')
        sys.exit(1)

    pid = sys.argv[1]

    with httpx.Client(http2=True, timeout=60.0, follow_redirects=True) as client:
        collection = get_json(client, f'{URL_BASE}{pid}')
        if collection is None:
            sys.exit(1)

        with zipfile.ZipFile(f'{pid}.zip', 'w') as zip_file:
            process_collection(client, collection, zip_file)

    print(f'Done: {pid}.zip')

if __name__ == '__main__':
    main()