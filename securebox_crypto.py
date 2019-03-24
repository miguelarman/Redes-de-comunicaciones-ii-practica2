from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP


# Falta introducir firma con HASH antes de cifrar el archivo,
# y comprobación de la misma al descifrarlo

# Este fichero se encarga de la parte de criptografía de la práctica:
# cifrar, firmar y descifrar ficheros
# Para ello, se va a usar el esquema de cifrado híbrido con firma visto en clase:
# - Para cifrar el fichero:
#   1- Se genera una clase AES de sesión (aleatoria)
#   2- Se cifra el archivo con esta clave
#   3- Se cifra la clave simétrica AES con la clave publica del receptor
#   4- Se envían ambas al receptor
# - Para descifrar el fichero:
#   1- Separa la clave AES cifrada por RSA del fichero cifrado por AES
#   2- Descifra la clave AES con su clave privada RSA
#   3- Descifra el fichero con la clave AES una vez descifrada

def encript(rsa_publicKey_path, input_file_path, output_file_path, verbose=False):

    fichero_a_cifrar = open(input_file_path, 'rb')
    data = fichero_a_cifrar.read()

    print('Leyendo clave pública...', end='\r')
    sys.stdout.flush()
    recipient_key = RSA.import_key(open(rsa_publicKey_path).read())
    print('Leyendo clave pública... OK')


    print('Generando clave AES aleatoria...', end='\r')
    sys.stdout.flush()
    session_key = get_random_bytes(16)
    print('Generando clave AES aleatoria... OK')

    # Encrypt the session key with the public RSA key
    print('Cifrando la clave AES con RSA...', end='\r')
    sys.stdout.flush()
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_session_key = cipher_rsa.encrypt(session_key)
    print('Cifrando la clave AES con RSA... OK')

    # Encrypt the data with the AES session key
    print('Cifrando el archivo con AES...', end='\r')
    sys.stdout.flush()
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext = cipher_aes.encrypt(data)
    print('Cifrando el archivo con AES... OK')

    print('Creando el nuevo fichero cifrado...', end='\r')
    sys.stdout.flush()
    file_out = open(output_file_path, 'wb')
    [ file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, ciphertext) ]
    file_out.close()
    print('Creando el nuevo fichero cifrado... OK')

    cyphered_bytes = os.path.getsize(output_file_path)
    print('{} bytes cifrados correctamente'.format(cyphered_bytes))

    return output_file_path

def decrypt(rsa_privateKey_path, input_file_path, output_file_path, verbose=False):

    print('Leyendo la clave privada...', end='\r')
    sys.stdout.flush()
    private_key = RSA.import_key(open(rsa_privateKey_path).read())
    print('Leyendo la clave privada... OK')

    print('Leyendo la clave AES y el fichero cifrados...', end='\r')
    sys.stdout.flush()
    file_in = open(input_file_path, 'rb')
    enc_session_key, nonce, ciphertext = \
       [ file_in.read(x) for x in (private_key.size_in_bytes(), 16, -1) ]
    file_in.close()
    print('Leyendo la clave AES y el fichero cifrados... OK')

    # Decrypt the session key with the private RSA key
    print('Desencriptando la clave AES...', end='\r')
    sys.stdout.flush()
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)
    print('Desencriptando la clave AES... OK')

    # Decrypt the data with the AES session key
    print('Desencriptando los datos con la clave AES...', end='\r')
    sys.stdout.flush()
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    data = cipher_aes.decrypt(ciphertext)
    print('Desencriptando los datos con la clave AES... OK')

    print('Guardando los datos descifrados en el nuevo fichero...', end='\r')
    sys.stdout.flush()
    fichero_descifrado = open(output_file_path, 'wb')
    fichero_descifrado.write(data)
    fichero_descifrado.close()
    print('Guardando los datos descifrados en el nuevo fichero... OK')

    decyphered_bytes = os.path.getsize(output_file_path)
    print('{} bytes descifrados correctamente'.format(decyphered_bytes))

    return output_file_path
