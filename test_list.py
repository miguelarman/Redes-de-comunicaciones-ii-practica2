import requests
import credenciales
import generales

url = generales.url_servidor + '/api/files/list'
headers = {'Authorization': 'Bearer {}'.format(credenciales.my_token)}

response = requests.post(url, headers=headers)
if response.status_code != 200:
    # TODO
    print('Error con la petición:')
    # _imprime_error(response)
    exit()
    # return None

resultado = response.json()
print(resultado)

# return resultado




#  Pruebas con curl
 # Subir un fichero
  # curl --verbose -H "Authorization: Bearer 7E4DA9B6a2C0beF3" -F "ufile=@/home/miguelarman/Escritorio/Universidad/Redes-II/practica2/test.py" http://vega.ii.uam.es:8080/api/files/upload
 # Borrar un fichero
  # curl --verbose -H "Authorization: Bearer AaFBe2d7894C1D63" -H "Content-Type: application/json" --data '{"file_id":"b10A7f36"}' -X POST http://vega.ii.uam.es:8080/api/files/delete
