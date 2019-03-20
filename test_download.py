import requests
import credenciales
import generales
import sys
from securebox_requests import _imprime_error

if (len(sys.argv) < 2):
    print('Especifica el id del archivo')
    exit()

url = generales.url_servidor + '/api/files/download'
headers = {'Authorization': 'Bearer {}'.format(credenciales.my_token)}
args={'file_id': '{}'.format(sys.argv[1])}

response = requests.post(url, json=args, headers=headers)
if response.status_code != 200:
    # TODO
    print('Error con la petición:')
    _imprime_error(response)
    exit()
    # return None

resultado = response.json()
print(resultado)

# return resultado
