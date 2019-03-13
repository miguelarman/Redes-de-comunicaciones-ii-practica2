import requests
import credenciales
import generales

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
