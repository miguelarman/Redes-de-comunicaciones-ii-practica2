import requests
import credenciales
import generales
import sys
from securebox_requests import _imprime_error

if (len(sys.argv) < 2):
    print('Especifica la ruta del archivo')
    exit()

ruta = sys.argv[1]

url = generales.url_servidor + '/api/files/upload'
headers = generales.header_autorizacion
args = {'ufile': (ruta, open(ruta, 'rb'))}

response = requests.post(url, headers=headers, files=args)
if response.status_code != 200:
    # TODO
    print('Error con la petición:')
    _imprime_error(response)
    exit()
    # return None

resultado = response.json()
print(resultado)
