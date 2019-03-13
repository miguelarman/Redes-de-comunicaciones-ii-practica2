import sys
from securebox_requests import *

if (len(sys.argv) < 2):
    print('Introduce los datos a buscar')
    exit()

search(sys.argv[1], flag_imprimir=True)
