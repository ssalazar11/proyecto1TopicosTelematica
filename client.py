import os
import requests


namenode_url = 'http://localhost:6000'


datanode_urls = [
    'http://localhost:6001',
    'http://localhost:6002',
    'http://localhost:6003',
]


BLOCK_SIZE = 1024

def upload_file(filename):
    if not os.path.isfile(filename):
        print(f"Error: el archivo '{filename}' no existe.")
        return

    file_basename = os.path.basename(filename)
    blocks = []
    datanode_block_map = {}  

    with open(filename, 'rb') as f:
        block_number = 0
        while True:
            block_data = f.read(BLOCK_SIZE)
            if not block_data:
                break

            block_id = f"{file_basename}_block_{block_number}"
            blocks.append(block_id)

           
            index1 = block_number % len(datanode_urls)
            index2 = (index1 + 1) % len(datanode_urls)

            datanode_url_1 = datanode_urls[index1]
            datanode_url_2 = datanode_urls[index2]

           
            upload_block([datanode_url_1, datanode_url_2], block_id, block_data)

            
            datanode_block_map[block_id] = [datanode_url_1, datanode_url_2]

            block_number += 1

    
    register_file_in_namenode(file_basename, blocks, datanode_block_map)

def upload_block(datanode_urls, block_id, block_data):
    block_data_encoded = {'block_id': block_id, 'data': block_data.hex()}
    
    for datanode_url in datanode_urls:
        try:
            response = requests.post(f'{datanode_url}/storeblock', json=block_data_encoded)
            response.raise_for_status()
            print(f"Block {block_id} almacenado en {datanode_url}")
        except requests.exceptions.RequestException as e:
            print(f"Error al almacenar el bloque {block_id} en {datanode_url}: {e}")

def register_file_in_namenode(filename, blocks, datanode_block_map):
    data = {'filename': filename, 'blocks': blocks, 'datanodes': datanode_block_map}
    response = requests.post(f'{namenode_url}/register', json=data)
    print(response.json())


def download_file(filename):
    response = requests.get(f'{namenode_url}/fileinfo/{filename}')
    file_info = response.json()

    if 'error' in file_info:
        print(f"Error: {file_info['error']}")
        return

    blocks = file_info['blocks']
    datanodes = file_info['datanodes']

    with open(f'downloaded_{filename}', 'wb') as f:
        for block_id in blocks:
            datanode_urls = datanodes[block_id]
            
            block_data = None
            for datanode_url in datanode_urls:
                try:
                    block_response = requests.get(f'{datanode_url}/getblock/{block_id}')
                    block_response.raise_for_status()
                    block_data = block_response.json().get('data')
                    if block_data:
                        print(f'Block {block_id} descargado desde {datanode_url}.')
                        break
                except requests.exceptions.RequestException as e:
                    print(f"Error al descargar el bloque {block_id} desde {datanode_url}: {e}")

            if block_data:
                f.write(bytes.fromhex(block_data))
            else:
                print(f"Error: no se pudo descargar el bloque {block_id} desde ningún DataNode.")


def list_files():
    response = requests.get(f'{namenode_url}/list')
    print("Archivos en el sistema:", response.json())

def execute_command(command):
    if command.startswith('put '):
        filename = command.split(' ')[1]
        upload_file(filename)
    elif command.startswith('get '):
        filename = command.split(' ')[1]
        download_file(filename)
    elif command == 'ls':
        list_files()
    else:
        print(f"Comando no reconocido: {command}")

if __name__ == '__main__':
    while True:
        command = input("dfs> ")
        execute_command(command)
