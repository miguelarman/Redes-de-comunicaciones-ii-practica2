from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
import sys

BLOCK_SIZE = 16

fichero_a_cifrar = open('fichero_para_cifrar', 'rb')
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
cipher_aes = AES.new(session_key, AES.MODE_CBC)
# data = bytes(data)
ciphertext = cipher_aes.encrypt(pad(data, BLOCK_SIZE))
cipher_iv = cipher_aes.iv

[ file_out.write(x) for x in (enc_session_key, cipher_iv, ciphertext) ]

file_out.close()

print('Cifrado completado')


print('##############################################################')


file_in = open('datos_cifrados.bin', 'rb')

private_key = RSA.import_key(open('rsa/privada.pem').read())

enc_session_key, cipher_iv, ciphertext = \
   [ file_in.read(x) for x in (private_key.size_in_bytes(), BLOCK_SIZE,-1) ]

file_in.close()

# Decrypt the session key with the private RSA key
cipher_rsa = PKCS1_OAEP.new(private_key)
session_key = cipher_rsa.decrypt(enc_session_key)

# Decrypt the data with the AES session key
cipher_aes = AES.new(session_key, AES.MODE_CBC, iv=cipher_iv)
data = unpad(cipher_aes.decrypt(ciphertext), BLOCK_SIZE)

print('Descifrado completado')

fichero_descifrado = open('fichero_descifrado', 'wb')
fichero_descifrado.write(data)
fichero_descifrado.close()
