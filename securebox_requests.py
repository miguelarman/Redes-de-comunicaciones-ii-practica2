import sys
import requests
import credenciales
import generales
import json
from Crypto.PublicKey import RSA


# En este fichero se definen las funciones auxiliares que se encargan de cada
# una de las funcionalidades:
#   Funciones relacionadas con la gestión de identidades
#       /users/register - registra un usuario en el sistema
#       /users/getPublicKey - obtiene la clave pública de un usuario
#       /users/search - obtiene datos de un usuario por nombre o correo electrónico
#       /user/delete - borrar un usuario
#   Funciones relacionadas con la gestión de ficheros
#       /files/upload - sube un fichero al sistema
#       /files/download - descarga un fichero
#       /files/list - lista todos los ficheros pertenecientes a un usuario
#       /files/delete - borra un fichero

# Funcion que registra un usuario en el sistema
def register(nombre, email, flag_imprimir=False):

    print('Generando par de claves RSA de 2048 bits...OK')

    key = RSA.generate(2048)

    private_key = key.export_key()
    file_out = open("rsa/privada.pem", "wb")
    file_out.write(private_key)

    public_key = key.publickey().export_key()
    file_out = open("rsa/publica.pem", "wb")
    file_out.write(public_key)

    publicKey = public_key.decode()

    print(publicKey)

    url = generales.url_servidor + '/api/users/register'
    args = {
        'nombre': nombre,
        'email': email,
        'publicKey': publicKey
    }
    headers = {'Authorization': 'Bearer {}'.format(credenciales.my_token)}

    if flag_imprimir:
        print('Se va a registrar el usuario {} y con email {}'.format(nombre, email))

    response = requests.post(url, json=args, headers=headers)
    if response.status_code != 200:
        # TODO
        print('Error con la petición:')
        _imprime_error(response)
        return None
    resultado = response.json()

    return resultado

# Funcion que se encarga de buscar un usuario por nombre o correo electrónico
def getPublicKey(nia):
    url = generales.url_servidor + '/api/users/getPublicKey'
    args = {'userID': nia}
    headers = {'Authorization': 'Bearer {}'.format(credenciales.my_token)}

    response = requests.post(url, json=args, headers=headers)
    if response.status_code != 200:
        # TODO
        print('Error con la petición:')
        _imprime_error(response)
        return None
    resultado = response.json()

    if ('publicKey' in resultado):
        return resultado['publicKey']
    else:
        return None


# Funcion que se encarga de buscar un usuario por nombre o correo electrónico
def search(a_buscar, flag_imprimir=False):
    url = generales.url_servidor + '/api/users/search'
    args = {'data_search': a_buscar}
    headers = {'Authorization': 'Bearer {}'.format(credenciales.my_token)}

    if flag_imprimir:
        print('Buscando usuario \'{}\' en el servidor...OK'.format(a_buscar))

    response = requests.post(url, json=args, headers=headers)
    if response.status_code != 200:
        # TODO
        print('Error con la petición:')
        _imprime_error(response)
        return None
    resultados = response.json()

    if flag_imprimir:
        print('{} usuarios encontrados:'.format(str(len(resultados))))
        for i in range(len(resultados)):
            resultado = resultados[i]

            nombre = str(resultado['nombre'])
            email = resultado['email']
            nia = resultado['userID']
            print('[{}] {}, {}, ID: {}'.format(str(i + 1), nombre, email, nia))

    return resultados

# Funcion que elimina a un usuario del sistema
def delete(nia, flag_imprimir=False):
    url = generales.url_servidor + '/api/users/delete'
    args = {'userID': nia}

    headers = {'Authorization': 'Bearer {}'.format(credenciales.my_token)}

    if flag_imprimir:
        print('Se va a eliminar el usuario con ID {}'.format(nia))

    response = requests.post(url, json=args, headers=headers)
    if response.status_code != 200:
        # TODO
        print('Error con la petición:')
        _imprime_error(response)
        return None
    resultado = response.json()

    return resultado



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

# print(r.status_code)
# print(r.headers['content-type'])
# print(r.encoding)
# print(r.text)
# print(r.json())


# curl --verbose -H "Authorization: Bearer AaFBe2d7894C1D63" -H "Content-Type: application/json" --data '{"data_search": "miguel.ar"}' -X POST http://vega.ii.uam.es:8080/api/users/register
# curl --verbose -H "Authorization: Bearer AaFBe2d7894C1D63" -H "Content-Type: application/json" --data '{"nombre": "Miguel Arconada","email": "miguel.arconada@estudiante.uam.es","publicKey": "publicKey"}' -X POST http://vega.ii.uam.es:8080/api/users/register
