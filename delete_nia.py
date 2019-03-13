from securebox_requests import *
import sys

if (len(sys.argv) < 2):
    print('Introduce los nias a borrar')
    exit()

for nia in sys.argv[1:]:
    delete(nia, flag_imprimir=True)
