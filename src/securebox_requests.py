"""
    Prácticas de Redes de comunicaciones 2

    Autores:
        Miguel Arconada Manteca
        Mario García Pascual

    securebox_requests:
        En este fichero se definen las funciones auxiliares que se encargan de
        realizar peticiones al servidor SecureBox aportado:
            Funciones relacionadas con la gestión de identidades
               /users/register      - registra un usuario en el sistema
               /users/getPublicKey  - obtiene la clave pública de un usuario
               /users/search        - obtiene datos de un usuario por nombre o correo electrónico
               /user/delete         - borrar un usuario
           Funciones relacionadas con la gestión de ficheros
               /files/upload        - sube un fichero al sistema
               /files/download      - descarga un fichero
               /files/list          - lista todos los ficheros pertenecientes a un usuario
               /files/delete        - borra un fichero
"""

import sys
import os
import requests
import json

from Crypto.PublicKey import RSA

import src.credenciales
import src.generales

# Falta poner los print solo cuando la flag verbose esté a true




# Funcion que registra un usuario en el sistema
"""
This is an example of Google style.

Args:
    nombre: This is the first param.
    email: This is a second param.
    publicKey: blabla
    verbose: blabla

Returns:
    This is a description of what is returned.

Raises:
    KeyError: Raises an exception.
"""
def user_register(nombre, email, publicKey, verbose=False):

    url = generales.url_servidor + '/api/users/register'
    args = {
        'nombre': nombre,
        'email': email,
        'publicKey': publicKey
    }
    headers = generales.header_autorizacion

    if verbose:
        print('Se va a registrar el usuario {} y con email {}'.format(nombre, email))
        print('Registrando al usuario...', end='\r')

    response = requests.post(url, json=args, headers=headers)
    if response.status_code != 200:
        print('Error con la petición:')
        _imprime_error(response)
        return None

    if verbose:
        print('Registrando al usuario... OK')

    resultado = response.json()

    user_id = resultado['nombre']

    return user_id

# Funcion que se encarga de buscar un usuario por nombre o correo electrónico
"""
This is an example of Google style.

Args:
    userID: This is the first param.
    verbose: This is a second param.

Returns:
    This is a description of what is returned.

Raises:
    KeyError: Raises an exception.
"""
def user_getPublicKey(userID, verbose=False):
    url = generales.url_servidor + '/api/users/getPublicKey'
    args = {'userID': userID}
    headers = generales.header_autorizacion

    print('Accediendo a la clave pública del usuario {}...'.format(userID), end='\r')

    response = requests.post(url, json=args, headers=headers)
    if response.status_code != 200:
        print('Error con la petición:')
        _imprime_error(response)
        return None
    resultado = response.json()

    print('Accediendo a la clave pública del usuario {}... OK'.format(userID))

    if ('publicKey' in resultado):
        return resultado['publicKey']
    else:
        return None


"""
This is an example of Google style.

Args:
    a_buscar: This is the first param.
    verbose: This is a second param.

Returns:
    This is a description of what is returned.

Raises:
    KeyError: Raises an exception.
"""
def user_search(a_buscar, verbose=False):
    url = generales.url_servidor + '/api/users/search'
    args = {'data_search': a_buscar}
    headers = generales.header_autorizacion

    if verbose:
        print('Buscando usuario \'{}\' en el servidor...'.format(a_buscar), end='\r')

    response = requests.post(url, json=args, headers=headers)
    if response.status_code != 200:
        print('Error con la petición:')
        _imprime_error(response)
        return None
    resultados = response.json()

    print('Buscando usuario \'{}\' en el servidor... OK'.format(a_buscar))

    if verbose:
        print('{} usuarios encontrados:'.format(str(len(resultados))))
        for i in range(len(resultados)):
            resultado = resultados[i]

            nombre = str(resultado['nombre'])
            email = resultado['email']
            userID = resultado['userID']
            print('[{}] {}, {}, ID: {}'.format(str(i + 1), nombre, email, userID))

    return resultados

"""
This is an example of Google style.

Args:
    userID: This is the first param.
    verbose: This is a second param.

Returns:
    This is a description of what is returned.

Raises:
    KeyError: Raises an exception.
"""
def user_delete(userID, verbose=False):
    url = generales.url_servidor + '/api/users/delete'
    args = {'userID': userID}
    headers = generales.header_autorizacion

    if verbose:
        print('Eliminando el usuario...', end='\r')

    response = requests.post(url, json=args, headers=headers)
    if response.status_code != 200:
        print('Error con la petición:')
        _imprime_error(response)
        return None

    resultado = response.json()

    id_borrado = resultado['userID']

    print('Eliminando el usuario con... OK')

    print('Se ha eliminado el usuario con ID {}'.format(id_borrado))

    return id_borrado

"""
This is an example of Google style.

Args:
    file_path: This is the first param.
    verbose: This is a second param.

Returns:
    This is a description of what is returned.

Raises:
    KeyError: Raises an exception.
"""
def file_upload(file_path, verbose=False):
    url = generales.url_servidor + '/api/files/upload'
    headers = generales.header_autorizacion
    args = {'ufile': (os.path.basename(file_path), open(file_path, 'rb'))}

    print('Subiendo archivo al servidor...', end='\r')

    response = requests.post(url, headers=headers, files=args)
    if response.status_code != 200:
        print('Error con la petición:')
        _imprime_error(response)
        return None

    print('Subiendo archivo al servidor... OK')

    resultado = response.json()
    file_id = resultado['file_id']
    print('El id del fichero es ' + str(file_id))

    return file_id

"""
This is an example of Google style.

Args:
    file_id: This is the first param.
    verbose: This is a second param.

Returns:
    This is a description of what is returned.

Raises:
    KeyError: Raises an exception.
"""
def file_download(file_id, verbose=False):
    url = generales.url_servidor + '/api/files/download'
    headers = generales.header_autorizacion
    args = {'file_id': '{}'.format(file_id)}

    print('Descargando fichero del servidor...', end='\r')

    response = requests.post(url, json=args, headers=headers)

    if response.status_code != 200:
        print('Error con la petición:')
        _imprime_error(response)
        return None

    filename = response.headers['Content-Disposition'].split('\"')[-2]
    data = response.content

    # print('Descargando fichero del servidor... OK')
    #
    # print('Guardando fichero...', end='\r')
    # salida = open(filename, 'wb')
    # salida.write(response.content)
    # salida.close()
    #
    # print('Guardando fichero... OK')
    #
    # writen_bytes = os.path.getsize(filename)
    # print('{} bytes guardados correctamente'.format(writen_bytes))

    return [filename, data]

"""
This is an example of Google style.

Args:
    verbose: This is the first param.

Returns:
    This is a description of what is returned.

Raises:
    KeyError: Raises an exception.
"""
def file_list(verbose=False):
    url = generales.url_servidor + '/api/files/list'
    headers = generales.header_autorizacion

    print('Buscando ficheros en el servidor...', end='\r')

    response = requests.post(url, headers=headers)
    if response.status_code != 200:
        print('Error con la petición:')
        _imprime_error(response)
        return None

    print('Buscando ficheros en el servidor... OK')

    resultado = response.json()

    lista = resultado['files_list']
    num = resultado['num_files']

    # Imprime el resultado
    print('Se han encontrado {} ficheros'.format(num))

    for i in range(0, num):
        file = lista[i]
        name = file['fileName']
        id = file['fileID']
        print('\tFichero: {} con id {}'.format(name, id))

    return resultado

"""
This is an example of Google style.

Args:
    file_id: This is the first param.
    verbose: This is a second param.

Returns:
    This is a description of what is returned.

Raises:
    KeyError: Raises an exception.
"""
def file_delete(file_id, verbose=False):
    url = generales.url_servidor + '/api/files/delete'
    headers = generales.header_autorizacion
    args={'file_id': '{}'.format(file_id)}

    print('Eliminando fichero del servidor...', end='\r')

    response = requests.post(url, json=args, headers=headers)
    if response.status_code != 200:
        print('Error con la petición:')
        _imprime_error(response)
        return None

    print('Eliminando fichero del servidor... OK')

    resultado = response.json()

    print('Se ha eliminado el fichero con id {}'.format(resultado['file_id']))

    return resultado['file_id']

"""
This is an example of Google style.

Args:
    respuesta: This is the first param.

Returns:
    This is a description of what is returned.

Raises:
    KeyError: Raises an exception.
"""
def _imprime_error(respuesta):
    try:
        error = respuesta.json()
    except ValueError:
        print('La respuesta no contiene datos json')
        print(respuesta)
        return

    print('Se ha recibido el siguiente error tras una petición:')
    print('Código error HTTP: {}'.format(error['http_error_code']))
    print('Código error: {}'.format(error['error_code']))
    print('Descripción: {}'.format(error['description']))
