from flask import Flask, request, jsonify

app = Flask(__name__)

# Acá se guarda la información de los archivos.
files = {}

@app.route('/register', methods=['POST'])
def register_file():
    data = request.json
    print(f"Registrando archivo: {data['filename']}, Bloques: {data['blocks']}, DataNodes: {data['datanodes']}")
    filename = data['filename']
    blocks = data['blocks']
    datanodes = data['datanodes']
    
    # Guardar la información del archivo.
    files[filename] = {'blocks': blocks, 'datanodes': datanodes}
    return jsonify({'message': f'File {filename} registered successfully'}), 200

@app.route('/fileinfo/<filename>', methods=['GET'])
def get_file_info(filename):
    if filename in files:
        return jsonify(files[filename]), 200
    else:
        return jsonify({'error': 'File not found'}), 404

@app.route('/list', methods=['GET'])
def list_files():
    return jsonify(list(files.keys())), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
