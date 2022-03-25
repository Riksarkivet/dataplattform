import requests
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        res = requests.get(f'https://lbiiif.riksarkivet.se/collection/arkiv/{sys.argv[1]}')
        if res.status_code == 200:
            collection = res.json()
            print(collection.get("items", [{}])[0].get("id", ""))
        else:
            print(f'Error: {res.status_code}')
    else:
        print("Usage: python pid_to_image_id.py <pid>")
