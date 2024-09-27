from flask import Flask, request, jsonify

app = Flask(__name__)

# Acá se guardan los bloques
blocks = {}

@app.route('/storeblock', methods=['POST'])
def store_block():
    data = request.json
    print(f"Almacenando bloque: {data['block_id']} en el nodo actual")
    block_id = data['block_id']
    block_data_hex = data['data']
    
    # Convertimos los datos de hexadecimal a binario
    block_data = bytes.fromhex(block_data_hex)
    
    # Almacenar el bloque de datos
    blocks[block_id] = block_data
    return jsonify({'message': f'Block {block_id} stored successfully'}), 200

@app.route('/getblock/<block_id>', methods=['GET'])
def get_block(block_id):
    if block_id in blocks:
        return jsonify({'block_id': block_id, 'data': blocks[block_id].hex()}), 200
    else:
        return jsonify({'error': 'Block not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6004)
