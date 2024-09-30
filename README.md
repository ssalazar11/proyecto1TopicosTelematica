# Sistema de Archivos Distribuidos

## Descripción

Este proyecto implementa un sistema de archivos distribuidos utilizando un cliente, un NameNode y varios DataNodes. Los usuarios pueden cargar y descargar archivos a través de la red, aprovechando la replicación de bloques para asegurar la disponibilidad.

### Estructura de Archivos

- **client.py**: Este archivo implementa un cliente que permite a los usuarios cargar y descargar archivos a través de un interfaz de línea de comandos (CLI). 
  - **Funciones Clave**:
    - `upload_file(filename)`: Carga un archivo, dividiéndolo en bloques que se almacenan en dos DataNodes para replicación.
    - `download_file(filename)`: Descarga un archivo a partir de su nombre, recuperando los bloques desde los DataNodes.
    - `list_files()`: Lista todos los archivos registrados en el sistema.

- **namenode.py**: Este archivo implementa el servidor NameNode que registra la información de los archivos y sus bloques.
  - **Funciones Clave**:
    - `register_file()`: Registra un archivo y sus bloques en el sistema.
    - `get_file_info(filename)`: Proporciona información sobre un archivo registrado.
    - `list_files()`: Devuelve una lista de todos los archivos en el sistema.

- **datanode.py**: Este archivo implementa el servidor DataNode que almacena los bloques de datos.
  - **Funciones Clave**:
    - `store_block()`: Almacena un bloque de datos enviado por el cliente.
    - `get_block(block_id)`: Recupera un bloque almacenado por su identificador.

## Requisitos
- Flask (instalar con `pip install Flask`)
- Requests (instalar con `pip install requests`)

## Instrucciones de Uso
1. **Iniciar los DataNodes**:
   Ejecuta `datanode.py` en varios terminales, asignando un puerto diferente (6001 a 6004).

   ```bash
   python datanode.py
   ```
2. **Iniciar el NameNode**:
   Iniciar el NameNode: Ejecuta `namenode.py` en una terminal.

   ```bash
   python namenode.py
   ```
3. **Ejectuar el cliente**:
   Ejecutar el Cliente: Ejecuta `client.p`y en otra terminal.

   ```bash
   python client.py
   ```

4. **Comandos del cliente**
- Para subir un archivo: put <nombre_del_archivo>
- Para descargar un archivo: get <nombre_del_archivo>
- Para listar archivos: ls

