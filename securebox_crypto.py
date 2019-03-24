from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad
import sys
import os
import generales

# Falta introducir firma con HASH antes de cifrar el archivo,
# y comprobación de la misma al descifrarlo
# Tambien falta cambiar el tamaño de clave AES de 16 a 256

# Este fichero se encarga de la parte de criptografía de la práctica:
# cifrar, firmar y descifrar ficheros
# Para ello, se va a usar el esquema de cifrado híbrido con firma visto en clase:
# - Para cifrar el fichero:
#   1- Se genera una clase AES de sesión (aleatoria)
#   2- Se cifra el archivo con esta clave y con un IV aleatorio
#   3- Se cifra la clave simétrica AES con la clave publica del receptor
#   4- Se envían ambas claves y el IV al receptor
# - Para descifrar el fichero:
#   1- Separa la clave AES cifrada por RSA y el IV del fichero cifrado por AES
#   2- Descifra la clave AES con su clave privada RSA
#   3- Descifra el fichero con la clave AES una vez descifrada y con el IV

def encript(rsa_publicKey_path, input_file_path, output_file_path, verbose=False):

    fichero_a_cifrar = open(input_file_path, 'rb')
    data = fichero_a_cifrar.read()

    print('Leyendo clave pública...', end='\r')
    sys.stdout.flush()
    recipient_key = RSA.import_key(open(rsa_publicKey_path).read())
    print('Leyendo clave pública... OK')


    print('Generando clave AES aleatoria...', end='\r')
    sys.stdout.flush()
    session_key = get_random_bytes(generales.AES_KEY_LENGTH)
    print('Generando clave AES aleatoria... OK')

    # Encrypt the data with the AES session key
    print('Cifrando el archivo con AES...', end='\r')
    sys.stdout.flush()
    cipher_aes = AES.new(session_key, AES.MODE_CBC)
    ciphertext = cipher_aes.encrypt(pad(data, generales.BLOCK_SIZE))
    print('Cifrando el archivo con AES... OK')

    # Encrypt the session key and iv with the public RSA key
    print('Cifrando la clave AES y el IV con RSA...', end='\r')
    sys.stdout.flush()
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    cipher_iv = cipher_aes.iv
    enc_cipher_iv = cipher_rsa.encrypt(cipher_iv)
    enc_session_key = cipher_rsa.encrypt(session_key)
    print('Cifrando la clave AES y el IV con RSA... OK')

    print('Creando el nuevo fichero cifrado...', end='\r')
    sys.stdout.flush()
    file_out = open(output_file_path, 'wb')
    [ file_out.write(x) for x in (enc_session_key, enc_cipher_iv, ciphertext) ]
    file_out.close()
    print('Creando el nuevo fichero cifrado... OK')

    decyphered_bytes = os.path.getsize(input_file_path)
    cyphered_bytes = os.path.getsize(output_file_path)
    print('{} bytes cifrados correctamente a {} bytes'.format(decyphered_bytes, cyphered_bytes))

    return output_file_path

def decrypt(rsa_privateKey_path, input_file_path, output_file_path, verbose=False):

    print('Leyendo la clave privada...', end='\r')
    sys.stdout.flush()
    private_key = RSA.import_key(open(rsa_privateKey_path).read())
    print('Leyendo la clave privada... OK')

    print('Leyendo la clave AES y el fichero cifrados...', end='\r')
    sys.stdout.flush()
    file_in = open(input_file_path, 'rb')
    enc_session_key, enc_cipher_iv, ciphertext = \
       [ file_in.read(x) for x in (private_key.size_in_bytes(), private_key.size_in_bytes(), -1) ]
    file_in.close()
    print('Leyendo la clave AES y el fichero cifrados... OK')

    # Decrypt the session key with the private RSA key
    print('Desencriptando la clave AES y el IV...', end='\r')
    sys.stdout.flush()
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)
    cipher_iv = cipher_rsa.decrypt(enc_cipher_iv)
    print('Desencriptando la clave AES y el IV... OK')

    # Decrypt the data with the AES session key
    print('Desencriptando los datos con la clave AES...', end='\r')
    sys.stdout.flush()
    cipher_aes = AES.new(session_key, AES.MODE_CBC, iv=cipher_iv)
    data = unpad(cipher_aes.decrypt(ciphertext), generales.BLOCK_SIZE)
    print('Desencriptando los datos con la clave AES... OK')

    print('Guardando los datos descifrados en el nuevo fichero...', end='\r')
    sys.stdout.flush()
    fichero_descifrado = open(output_file_path, 'wb')
    fichero_descifrado.write(data)
    fichero_descifrado.close()
    print('Guardando los datos descifrados en el nuevo fichero... OK')

    cyphered_bytes = os.path.getsize(input_file_path)
    decyphered_bytes = os.path.getsize(output_file_path)
    print('{} bytes descifrados correctamente a {} bytes'.format(cyphered_bytes, decyphered_bytes))

    return output_file_path
