import credenciales

url_servidor = 'http://vega.ii.uam.es:8080'
header_autorizacion = {'Authorization': 'Bearer {}'.format(credenciales.my_token)}
BLOCK_SIZE = 16
AES_KEY_LENGTH = int (256 / 8)
