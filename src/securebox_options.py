"""
    Prácticas de Redes de comunicaciones 2

    Autores:
        Miguel Arconada Manteca
        Mario García Pascual

    securebox_options:
        En este fichero se implementa el parseo de los argumentos y todas
        las funcionalidades que tiene el programa a alto nivel. Lo que
        tiene que ver con criptografia esta en securebox_crypto y lo que tiene
        que ver con peticinones al servidor en securebox_requests.
        Las funcionalidades que se implementan son:
            -crear un id
            -borrar un id
            -buscar un id
            -subir un fichero
            -descargar un fichero
            -cifrar un fichero localmente
            -descifrar un fichero localmente
            -firmar un fichero localmente
            -verificar la firma de un fichero localmente
            -firmar y cifrar un fichero localmente
            -descifrar y verificar un fichero localmente
"""

import argparse
import os

from Crypto.PublicKey import RSA

from src.securebox_requests import *
from src.securebox_crypto import *
from src.securebox_crypto import *


class SecureBoxError(Exception):
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return str(self.text)

"""
Parsea los argumentos del cliente.

Returns:
    La estructura que contiene los argumentos del cliente.
"""
def parse_options():
    parser = argparse.ArgumentParser(description='Cliente de SecureBox')

    # Gestión de usuarios e identidades
    parser.add_argument('--create_id', nargs='*',
                        help='nombre email [alias]. Crea una nueva identidad')
    parser.add_argument('--search_id', help='Busca un usuario')
    parser.add_argument('--delete_id', help='Borra una identidad')

    # Subida y descarga de ficheros
    parser.add_argument('--upload', help='Envia un fichero a otro usuario.')
    parser.add_argument('--source_id', help='ID del emisor')
    parser.add_argument('--dest_id', help='ID del receptor')
    parser.add_argument('--list_files', action='store_true',
                        help='lista todos los ficheros del usuario')
    parser.add_argument('--download', help='Descarga un fichero de un usuario')
    parser.add_argument('--delete_file', help='Borra un fichero')

    # Cifrado y firma de ficheros local
    parser.add_argument('--encrypt', help='Cifra un fichero')
    parser.add_argument('--sign', help='Firma un fichero')
    parser.add_argument('--enc_sign', help='Cifra y firma un fichero')

    # Devolvemos los argumentos como diccionario en vez de Namespace
    return parser.parse_args()

"""
Obtiene la clave publica RSA que esta almacenada localmente.

Returns:
    La clave publica del usuario.
"""
def get_my_publickey():
    return RSA.import_key(open('rsa/publica.pem', 'rb').read())

"""
Obtiene la clave privada RSA que esta almacenada localmente

Returns:
    La clave privada del usuario.
"""
def get_my_privatekey():
    return RSA.import_key(open('rsa/privada.pem', 'rb').read())


"""
Procesa los argumentos y ejecuta la funcionalidad que corresponda.

Args:
    opts: Los argumentos del cliente.

Returns:
    Nada.
"""
def process_options(opts):
    try:
        if opts.create_id:
            process_create_id(opts.create_id)
        elif opts.search_id:
            process_search_id(opts.search_id)
        elif opts.delete_id:
            process_delete_id(opts.delete_id)
        elif opts.encrypt:
            process_encrypt(opts.encrypt, opts.dest_id)
        elif opts.sign:
            process_sign(opts.sign)
        elif opts.enc_sign:
            process_enc_sign(opts.enc_sign, opts.dest_id)
        elif opts.upload:
            process_upload(opts.upload, opts.dest_id)
        elif opts.list_files:
            process_list_files()
        elif opts.download:
            process_download(opts.download, opts.source_id)
        elif opts.delete_file:
            process_delete_file(opts.delete_file)
        else:
            return None
    except SecureBoxError as e:
        print(e)

"""
Funcion que implementa la funcionalidad de crear una identidad.

Args:
    args: los argumentos para crear la identidad.

Returns:
    Nada.

Raises:
    SecureBoxError: si los argumentos son invalidos o insuficientes.
"""
def process_create_id(args):
    # Se comprueba que los argumentos son validos
    if len(args) is 2:
        nombre = args[0]
        email = args[1]
        alias = None
    elif len(args) is 3:
        nombre = args[0]
        email = args[1]
        alias = args[2] # No se utilizada para nada
    else:
        raise SecureBoxError('Estructura de argumentos de create_id invalida')
    if not nombre or not email:
        raise SecureBoxError('Nombre y email son argumentos obligatorios para crear una identidad')

    # Crea la identidad, clave publica y privada
    print('Generando par de claves RSA de 2048 bits...', end='\r')
    privatekey = RSA.generate(2048)
    print('Generando par de claves RSA de 2048 bits... OK')

    filename = 'rsa/privada.pem'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as f:
        f.write(privatekey.export_key())

    publickey = privatekey.publickey()
    filename = 'rsa/publica.pem'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as f:
        f.write(publickey.export_key())

    print(publickey.export_key().decode())

    # La registra en SecureBox
    user_register(nombre, email, publickey.export_key(), verbose=True)

"""
Funcion que implementa la funcionalidad de buscar una identidad.

Args:
    cadena (str): identidad que se quiere buscar.

Returns:
    Nada.

Raises:
    SecureBoxError: si la cadena introducida es invalida.
"""
def process_search_id(cadena):
    if not cadena:
        raise SecureBoxError('Cadena es un argumento obligatorio para buscar una identidad')
    user_search(cadena, verbose=True)

"""
Funcion que implementa la funcionalidad de borrar una identidad.

Args:
    id: identidad que se quiere borrar.

Returns:
    Nada.

Raises:
    SecureBoxError: si la id introducida es invalida.
"""
def process_delete_id(id):
    if not id:
        raise SecureBoxError('Id es un argumento obligatorio para borrar una identidad')
    user_delete(id, verbose=True)

def process_list_files():
    file_list()

def process_delete_file(id):
    if not id:
        raise SecureBoxError('Id fichero es un argumento obligatorio para borrar un fichero')
    file_delete(id)

"""
Funcion que implementa la funcionalidad de subir un fichero.

Args:
    fichero: ruta del fichero que se quiere subir.
    dest_id: id del destinatario.

Returns:
    Nada.

Raises:
    SecureBoxError: si los argumentos son invalidos o insuficientes.
"""
def process_upload(fichero, dest_id):
    if not fichero or not dest_id:
        raise SecureBoxError('Fichero e Id destino son argumentos obligatorios para subir un fichero')
    ret = user_getPublicKey(dest_id, verbose=True)
    if not ret:
        raise SecureBoxError('No se ha podido obtener la clave pública del id ' + str(dest_id))
    publickey = RSA.import_key(ret)
    privatekey = get_my_privatekey()

    with open(fichero, 'rb') as f:
        data = f.read()
    sign_data = sign(data, privatekey)
    enc_sign_data = encrypt(sign_data, publickey)
    # Si el fichero es a/b/c.ext lo guardamos en enc/a/b/sign-c.ext
    filename = 'uploads/' + os.path.basename(fichero)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as f:
        f.write(enc_sign_data)

    file_upload(filename, verbose=True)

"""
Funcion que implementa la funcionalidad de descargar un fichero.

Args:
    id: id del fichero que se quiere descargar.
    source_id: id del emisor del fichero.

Returns:
    Nada.

Raises:
    SecureBoxError: si los argumentos son invalidos o insuficientes; si no se
        ha podido obtener la clave publica; si no se ha podido descargar el
        fichero; si no se ha podido verificar el fichero descargado.
"""
def process_download(id, source_id):
    if not id or not source_id:
        raise SecureBoxError('Id fichero es un argumento obligatorio para descargar un fichero')
    ret = user_getPublicKey(source_id, verbose=True)
    if not ret:
        raise SecureBoxError('No se ha podido obtener la clave pública del id ' + str(source_id))
    publickey = RSA.import_key(ret)
    privatekey = get_my_privatekey()
    ret = file_download(id, verbose=True)
    if not ret:
        raise SecureBoxError('No se ha podido descargar el fichero con id ' + str(source_id))

    fichero = ret[0]
    enc_sign_data = ret[1]
    sign_data = decrypt(enc_sign_data, privatekey)
    if verify(sign_data, publickey):
        print('El fichero se ha verificado correctamente')
    else:
        raise SecureBoxError('El fichero no se ha podido verificar, no se guarda localmente')
    filename = 'downloads/' + fichero
    print('Guardado en ' + filename)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as f:
        f.write(unsign(sign_data))



"""
Funcion que implementa la funcionalidad de cifrar un fichero localmente.

Args:
    fichero: ruta del fichero a cifrar.
    dest_id: id del destinatario.

Returns:
    Nada.

Raises:
    SecureBoxError: si los argumentos son insuficientes o invalidos; si no se
        ha podido obtener la clave publica.
"""
def process_encrypt(fichero, dest_id):
    if not fichero or not dest_id:
        raise SecureBoxError('Fichero e Id destino son argumentos obligatorios para cifrar')
    ret = user_getPublicKey(dest_id, verbose=True)
    if not ret:
        raise SecureBoxError('No se ha podido obtener la clave pública del id ' + str(dest_id))
    publickey = RSA.import_key(ret)

    with open(fichero, 'rb') as f:
        data = f.read()
    enc_data = encrypt(data, publickey)
    # Si el fichero es a/b/c.ext lo guardamos en enc/a/b/enc-c.ext
    filename = 'enc/' + os.path.dirname(fichero) + 'enc-' + os.path.basename(fichero)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as f:
        f.write(enc_data)

"""
Funcion que implementa la funcionalidad de firmar un fichero localmente.

Args:
    fichero: ruta del fichero a firmar.

Returns:
    Nada.

Raises:
    SecureBoxError: si el argumento es invalido.
"""
def process_sign(fichero):
    if not fichero:
        raise SecureBoxError('Fichero es un argumento obligatorio para firmar un fichero')
    privatekey = get_my_privatekey()

    with open(fichero, 'rb') as f:
        data = f.read()
    sign_data = sign(data, privatekey)
    # Si el fichero es a/b/c.ext lo guardamos en enc/a/b/sign-c.ext
    filename = 'enc/' + os.path.dirname(fichero) + 'sign-' + os.path.basename(fichero)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as f:
        f.write(sign_data)

"""
Funcion que implementa la funcionalidad de firmar y cifrar un fichero localmente.

Args:
    fichero: ruta del fichero a firmar.
    dest_id: id del destinatario del fichero.

Returns:
    Nada.

Raises:
    SecureBoxError: si los argumentos son invalidos o insuficientes: si no se ha
        podido obtener la clave publica.
"""
def process_enc_sign(fichero, dest_id):
    if not fichero or not dest_id:
        raise SecureBoxError('Fichero y Id destino son argumentos obligatorios para cifrar y firmar')
    ret = user_getPublicKey(dest_id, verbose=True)
    if not ret:
        raise SecureBoxError('No se ha podido obtener la clave pública del id ' + str(dest_id))
    publickey = RSA.import_key(ret)
    privatekey = get_my_privatekey()

    with open(fichero, 'rb') as f:
        data = f.read()
    sign_data = sign(data, privatekey)
    enc_sign_data = encrypt(sign_data, publickey)
    # Si el fichero es a/b/c.ext lo guardamos en enc/a/b/enc-sign-c.ext
    filename = 'enc/' + os.path.dirname(fichero) + 'enc-sign-' + os.path.basename(fichero)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as f:
        f.write(enc_sign_data)
