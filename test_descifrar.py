from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import sys

if (len(sys.argv) < 2):
    print('Especifica la ruta del archivo a descifrar')
    exit()

file_in = open(sys.argv[1], 'rb')

private_key = RSA.import_key(open('rsa/privada.pem').read())

enc_session_key, nonce, ciphertext = \
   [ file_in.read(x) for x in (private_key.size_in_bytes(), 16, -1) ]

file_in.close()

# Decrypt the session key with the private RSA key
cipher_rsa = PKCS1_OAEP.new(private_key)
session_key = cipher_rsa.decrypt(enc_session_key)

# Decrypt the data with the AES session key
cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
data = cipher_aes.decrypt(ciphertext)

print('Descifrado completado')


fichero_descifrado = open('fichero_descifrado', 'wb')
fichero_descifrado.write(data)
fichero_descifrado.close()
