from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import sys

if (len(sys.argv) < 2):
    print('Especifica la ruta del archivo a cifrar')
    exit()

fichero_a_cifrar = open(sys.argv[1], 'rb')
# texto = fichero_a_cifrar.read()
# data = texto.encode('utf-8')
data = fichero_a_cifrar.read()

file_out = open('datos_cifrados.bin', 'wb')

recipient_key = RSA.import_key(open('rsa/publica.pem').read())
session_key = get_random_bytes(16)

# Encrypt the session key with the public RSA key
cipher_rsa = PKCS1_OAEP.new(recipient_key)
enc_session_key = cipher_rsa.encrypt(session_key)

# Encrypt the data with the AES session key
cipher_aes = AES.new(session_key, AES.MODE_EAX)
# data = bytes(data)
ciphertext = cipher_aes.encrypt(data)

[ file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, ciphertext) ]

file_out.close()

print('Cifrado completado')
