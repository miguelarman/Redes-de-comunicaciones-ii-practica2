"""
    Prácticas de Redes de comunicaciones 2

    Autores:
        Miguel Arconada Manteca
        Mario García Pascual

    generales.py:
        Este fichero contiene algunas constantes útiles para el resto de
        módulos.
"""

import src.credenciales

url_servidor = 'http://vega.ii.uam.es:8080'
header_autorizacion = {'Authorization': 'Bearer {}'.format(src.credenciales.my_token)}
BLOCK_SIZE = 16
AES_KEY_LENGTH = int (256 / 8)
