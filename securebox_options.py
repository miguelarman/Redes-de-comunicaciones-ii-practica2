import argparse
from securebox_requests import *

# Todos los posibles argumentos
opts = ["--create_id", "--search_id", "--delete_id", \
        "--upload", "--source_id", "--dest_id", \
        "--list_files", "--download", "--delete_file", \
        "--encrypt", "--sign", "--enc_sign"]

# Los argumentos activos (todos menos source_id y dest_id)
active_opts = ["--create_id", "--search_id", "--delete_id", \
               "--upload", \
               "--list_files", "--download", "--delete_file", \
               "--encrypt", "--sign", "--enc_sign"]

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
    return vars(parser.parse_args())


def process_opt(opt, opts):
    if opt is "--create_id":
        process_create_id(args)
    elif opt is "--search_id":
        process_search_id(args)
    elif opt is "--delete_id":
        process_delete(args)
    elif opt is "--upload":
        process_upload(args)
    elif opt is "--list_files":
        process_list_files(args)
    elif opt is "--download":
        process_download(args)
    elif opt is "--delete_id":
        process_delete_id(args)
    elif opt is "--encrypt":
        process_encrypt(args)
    elif opt is "--sign":
        process_sign(args)
    elif opt is "--enc_sign":
        process_enc_sign(args)
    else:
        return (-1, "error: invalid option")
    return (0, "ok")

def process_options(opts):
    for opt in active_opts:
        if opts[opt]:
            process_opt(opt, opts)


def process_create_id(nombre, email, alias):
    # TODO crear la clave pública y clave privada
    users_register(nombre, email, publicKey)


def process_search_id(cadena):
    users_search(data_search, verbose=True)


def process_delete_id(id):
    users_delete(userID, verbose=True)


def process_upload(fichero, dest):

def process_list_files():
    list(verbose=True)

def process_download(id_fichero, source):

def process_delete_file(id_fichero):
    delete

def process_encrypt(fichero):

def process_sign(fichero):

def process_enc_sign(fichero):
