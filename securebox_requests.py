import sys
import requests
import credenciales
import generales

def search(a_buscar):

    url = generales.url_servidor + '/api/users/search'

    args = {'data_search': sys.argv[1]}
    headers = {'Authorization': 'Bearer ' + credenciales.my_token}

    print('Buscando usuario \'' + sys.argv[1] + '\' en el servidor...OK')
    r = requests.post(url, json=args, headers=headers)

    # print(r.status_code)
    # print(r.headers['content-type'])
    # print(r.encoding)
    # print(r.text)
    # print(r.json())

    resultados = r.json()

    print('Hay ' + str(len(resultados)) + ' resultados a la consulta')
    for i in range(len(resultados)):
        resultado = resultados[i]
        # print(resultado)
        print('[' + str(i + 1) + '] ' + str(resultado['nombre']) + ' ' + resultado['email'] + ' ' + resultado['userID'])


def getPublicKey(nia):

    url = generales.url_servidor + '/api/users/getPublicKey'
    args = {'userID': nia}
    headers = {'Authorization': 'Bearer ' + credenciales.my_token}

    r = requests.post(url, json=args, headers=headers)

    resultado = r.json()

    if ('publicKey' in resultado):
        return resultado['publicKey']
    else:
        return None
