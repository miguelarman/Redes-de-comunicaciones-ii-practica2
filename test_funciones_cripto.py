from securebox_crypto import encript, decrypt


ruta_encriptado = encript('rsa/publica.pem', 'fichero_para_cifrar', 'fichero_cifrado.bin', verbose=True)


ruta_desencriptado = decrypt('rsa/privada.pem', 'fichero_cifrado.bin', 'fichero_descifrado', verbose=True)
