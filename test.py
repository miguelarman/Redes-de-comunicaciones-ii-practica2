import sys
from securebox_requests import *

# Este programa prueba la funcionalidad de la parte de usuarios:
# 1- Registra al usuario
# 2- Busca al usuario en el sistema
# 3- Busca su clave pública
# 4- Elimina al usuario
# 5- Vuelve a buscarlo en el sistema

a_buscar = 'miguel.arconada'
nia = '361902'
nombre_completo = 'Miguel Arconada'
email = 'miguel.arconada@estudiante.uam.es'
clave_publica = 'publicKey'

# De momento guarda los datos fijados, no por argumentos
usuario = register(nombre_completo, email, clave_publica, flag_imprimir=True)
if (usuario == None):
    print('Error al registrar el usuario')
    exit()

usuarios = search(a_buscar, flag_imprimir=True)
if (len(usuarios) == 0):
    print('No se encontraron usuarios')
    exit()

exit()

print('Va a buscar la public key del primer usuario de la búsqueda')
public_key = getPublicKey(usuarios[0]['userID'])
print(public_key)

if (public_key == None):
    print('El usuario no dispone de clave pública')
    exit()

borrado = delete(nia, flag_imprimir=True)
if borrado == None:
    print('Error al borrar el usuario')
    exit()

usuarios = search(nia, flag_imprimir=True)
if (len(usuarios) == 0):
    print('No se encontraron usuarios en la segunda consulta')
    exit()
