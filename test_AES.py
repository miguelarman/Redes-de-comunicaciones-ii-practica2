from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

BLOCK_SIZE = 16
key_size = 16

fichero_a_cifrar = open('fichero_para_cifrar', 'rb')
# texto = fichero_a_cifrar.read()
# data = texto.encode('utf-8')
data = fichero_a_cifrar.read()

file_out = open('datos_cifrados_AES.bin', 'wb')

session_key = get_random_bytes(key_size)

cipher_aes = AES.new(session_key, AES.MODE_CBC)
# data = bytes(data)
ciphertext = cipher_aes.encrypt(pad(data, BLOCK_SIZE))
cipher_iv = cipher_aes.iv

[ file_out.write(x) for x in (session_key, cipher_iv, ciphertext) ]

file_out.close()

print('Cifrado completado')


print('##############################################################')


file_in = open('datos_cifrados_AES.bin', 'rb')

session_key, cipher_iv, ciphertext = \
   [ file_in.read(x) for x in (key_size, BLOCK_SIZE,-1) ]

file_in.close()

cipher_aes = AES.new(session_key, AES.MODE_CBC, iv=cipher_iv)
data = unpad(cipher_aes.decrypt(ciphertext), BLOCK_SIZE)

print('Descifrado completado')

fichero_descifrado = open('fichero_descifrado_aes', 'wb')
fichero_descifrado.write(data)
fichero_descifrado.close()
