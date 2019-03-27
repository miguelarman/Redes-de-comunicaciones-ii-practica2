import argparse
import os

from Crypto.PublicKey import RSA

from securebox_requests import *
from securebox_crypto import *
from _securebox_crypto import *

def parse_options():
    parser = argparse.ArgumentParser(description="Cliente de SecureBox")

    # Gestión de usuarios e identidades
    parser.add_argument("--create_id", nargs="*")
    parser.add_argument("--search_id")
    parser.add_argument("--delete_id")

    # Subida y descarga de ficheros
    parser.add_argument("--upload")
    parser.add_argument("--source_id")
    parser.add_argument("--dest_id")
    parser.add_argument("--list_files", action="store_true")
    parser.add_argument("--download")
    parser.add_argument("--delete_file")

    # Cifrado y firma de ficheros local
    parser.add_argument("--encrypt")
    parser.add_argument("--sign")
    parser.add_argument("--enc_sign")

    # Devolvemos los argumentos como diccionario en vez de Namespace
    return parser.parse_args()


def get_my_publickey():
    try:
        file_in = open('rsa/publica.pem', 'rb')
        return RSA.import_key(file_in.read())
    except:
        print("ERROR: rsa/publica.pem no existe")
        return None

def get_my_privatekey():
    try:
        file_in = open('rsa/privada.pem', 'rb')
        return RSA.import_key(file_in.read())
    except:
        print("ERROR: rsa/privada.pem no existe")
        return None


def process_options(opts):
    if opts.create_id:
        process_create_id(opts.create_id)
    elif opts.search_id:
        process_search_id(opts.search_id)
    elif opts.delete_id:
        process_delete_id(opts.delete_id)
    else:
        return None


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
        return 'ERROR'
    if not nombre or not email:
        return 'ERROR'

    # Crea la identidad, clave publica y privada
    print('Generando par de claves RSA de 2048 bits...', end='\r')
    privatekey = RSA.generate(2048)
    print('Generando par de claves RSA de 2048 bits... OK')

    file_out = open("rsa/privada.pem", "wb")
    file_out.write(privatekey.export_key())

    publickey = key.publickey()
    file_out = open("rsa/publica.pem", "wb")
    file_out.write(publickey.export_key())

    print(publickey.export_key().decode())

    # La registra en SecureBox
    user_register(nombre, email, publicKey, verbose=True)

def process_search_id(cadena):
    if not cadena:
        return 'ERROR'
    user_search(cadena, verbose=True)

def process_delete_id(id):
    if not id:
        return 'ERROR'
    user_delete(id, verbose=True)

def process_list_files():
    file_list()

def process_encrypt(fichero, dest_id):
    if not fichero:
        return 'ERROR'
    ret = user_getPublicKey(dest_id, verbose=True)
    if not ret:
        return 'ERROR'
    publickey = RSA.import_key(ret)

    file_in = open(fichero, 'rb')
    data = file_in.read()
    enc_data = encrypt(data, publickey)
    # Si el fichero es a/b/c.ext lo guardamos en enc/a/b/enc-c.data
    file_out = open('enc/' + os.path.dirname(fichero) + 'enc-' + os.path.basename(fichero) + fichero, 'wb')
    file_out.write(enc_data)


def process_sign(fichero):
    if not fichero:
        return 'ERROR'
    privatekey = get_my_privatekey()
    if not privatekey:
        return 'ERROR'

    file_in = open(fichero, 'rb')
    data = file_in.read()
    sign_data = sign(data, privatekey)
    # Si el fichero es a/b/c.ext lo guardamos en enc/a/b/sign-c.data
    file_out = open('enc/' + os.path.dirname(fichero) + 'sign-' + os.path.basename(fichero) + fichero, 'wb')
    file_out.write(sign_data)


def process_enc_sign(fichero, dest_id):
    if not fichero:
        return 'ERROR'
    ret = user_getPublicKey(dest_id, verbose=True)
    if not ret:
        return 'ERROR'
    publickey = RSA.import_key(ret)
    privatekey = get_my_privatekey()

    file_in = open(fichero, 'rb')
    data = file_in.read()
    sign_data = sign(data, privatekey)
    enc_sign_data = encrypt(sign_data, publickey)
    # Si el fichero es a/b/c.ext lo guardamos en enc/a/b/enc-sign-c.data
    file_out = open('enc/' + os.path.dirname(fichero) + 'enc-sign-' + os.path.basename(fichero) + fichero, 'wb')
    file_out.write(enc_sign_data)
