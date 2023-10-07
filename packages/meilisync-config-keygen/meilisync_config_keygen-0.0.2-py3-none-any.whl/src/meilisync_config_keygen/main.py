import click
import yaml
import os
import requests
import json

@click.command()
@click.option('--path', default="./config.example.yml", help="path to example config.yml file")
@click.option('--output', default="./config.yml", help="path to output config.yml file")
@click.option('--address', default="http://localhost:7700", help="address to meilisearch service")

def main(path, output, address):
    masterKey = os.environ['MEILI_MASTER_KEY']
    adminKey = create_admin_key(masterKey, address)
    write_key_in_yml(path, output, adminKey)

def get_file_content(path):
    with open(path, "r") as file:
        data = yaml.safe_load(file)
    return data

def create_admin_key(masterKey, address):
    r = make_request(masterKey, address)
    response = json.loads(r.text)
    return response['key']

def make_request(masterKey, address):
    payload = {
        'description': 'Admin key for meilisync app',
        'actions': ['*'],
        'indexes': ['*'],
        'expiresAt': None,
    }
    r = requests.post(f'{address}/keys',  
        headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {masterKey}'}, 
        data=json.dumps(payload),
    )
    return r

def write_key_in_yml(path, outputPath, key):
    data = get_file_content(path)
    data['meilisearch']['api_key'] = key

    with open(outputPath, "w") as file:
        yaml.dump(data, file)

if __name__ == "__main__":
    main()