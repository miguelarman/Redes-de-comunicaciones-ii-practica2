import argparse
import os

from Crypto.PublicKey import RSA

from securebox_requests import *
from securebox_crypto import *
from securebox_crypto import *

class SecureBoxError(Exception):
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return str(self.text)

def parse_options():
    parser = argparse.ArgumentParser(description='Cliente de SecureBox')

    # Gestión de usuarios e identidades
    parser.add_argument('--create_id', nargs='*')
    parser.add_argument('--search_id')
    parser.add_argument('--delete_id')

    # Subida y descarga de ficheros
    parser.add_argument('--upload')
    parser.add_argument('--source_id')
    parser.add_argument('--dest_id')
    parser.add_argument('--list_files', action='store_true')
    parser.add_argument('--download')
    parser.add_argument('--delete_file')

    # Cifrado y firma de ficheros local
    parser.add_argument('--encrypt')
    parser.add_argument('--sign')
    parser.add_argument('--enc_sign')

    # Devolvemos los argumentos como diccionario en vez de Namespace
    return parser.parse_args()


def get_my_publickey():
    return RSA.import_key(open('rsa/publica.pem', 'rb').read())

def get_my_privatekey():
    return RSA.import_key(open('rsa/privada.pem', 'rb').read())


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

def process_search_id(cadena):
    if not cadena:
        raise SecureBoxError('Cadena es un argumento obligatorio para buscar una identidad')
    user_search(cadena, verbose=True)

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
