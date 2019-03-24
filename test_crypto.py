from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import sys

fichero_a_cifrar = open('fichero_para_cifrar.txt', 'r')
texto = fichero_a_cifrar.read()
data = texto.encode('utf-8')

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


print('##############################################################')


file_in = open('datos_cifrados.bin', 'rb')

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

print('Descifrado completado:')
frase_decodificada = data.decode('utf-8')

fichero_descifrado = open('fichero_descifrado.txt', 'w')
fichero_descifrado.write(frase_decodificada)
fichero_descifrado.close()
