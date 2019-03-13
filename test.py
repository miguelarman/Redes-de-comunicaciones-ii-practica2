import sys
from getPublicKey import *
from search import *

if (len(sys.argv) < 3):
    print('Introduce dos argumentos')
    exit()

print('Se va a buscar el usuario por el nombre')
a = search(sys.argv[1])
print(a)

r = getPublicKey(sys.argv[2])

print(r)
