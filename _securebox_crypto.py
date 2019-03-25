import os
import sys

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15

import generales


"""
    Importante: publickey es de tipo RsaKey
"""
def encrypt(plaintext, publickey):
    # Se genera la clave simetrica
    session_key = get_random_bytes(generales.AES_KEY_LENGTH)

    # Se encripta el texto plano con la clave simetrica
    cipher_aes = AES.new(session_key, AES.MODE_CBC)
    ciphertext = cipher_aes.encrypt(pad(plaintext, generales.BLOCK_SIZE))

    # Se obtiene el iv y se encripta la clave simetrica
    cipher_rsa = PKCS1_OAEP.new(publickey)
    iv = cipher_aes.iv
    enc_session_key = cipher_rsa.encrypt(session_key)

    return iv + enc_session_key + ciphertext


"""
    Importante: privatekey es de tipo RsaKey
"""
def decrypt(enveloped, privatekey):
    # Sacamos los campos del texto cifrado
    cipher_iv = enveloped[:16]
    enc_session_key = enveloped[16:16+256]
    ciphertext = enveloped[16+256:]

    # Se encripta el texto plano con la clave simetrica
    cipher_rsa = PKCS1_OAEP.new(privatekey)
    session_key = cipher_rsa.decrypt(enc_session_key)

    # Se desencripta el texto cifrado con la clave simetrica
    cipher_aes = AES.new(session_key, AES.MODE_CBC, iv=cipher_iv)
    plaintext = unpad(cipher_aes.decrypt(ciphertext), generales.BLOCK_SIZE)

    return plaintext


"""
    Importante: privatekey es de tipo RsaKey
"""
def sign(plaintext, privatekey):
    # Se obtiene el hash del texto plano
    hashed_plaintext = SHA256.new(plaintext)
    signature = pkcs1_15.new(privatekey).sign(hashed_plaintext)
    return signature + plaintext

"""
    Importante: publickey es de tipo RsaKey

    Devuelve True si la firma es correcta, False en caso contrario
"""
def verify(signed, publickey):
    # Sacamos los campos
    signature = signed[:256]
    plaintext = signed[256:]

    # Se obtiene el hash del texto plano
    hashed_plaintext = SHA256.new(plaintext)
    try:
        pkcs1_15.new(publickey).verify(hashed_plaintext, signature)
        return True
    except:
        return False


print("prueba de que las cosas funcionan")
key = RSA.generate(2048)
pvk = key
pbk = key.publickey()
plaintext = "hola pedazo de hijo de puta como estas".encode()
print("texto plano:",plaintext)
msg = encrypt(plaintext, pbk)
print("texto cifrado:",msg)
nuevo = decrypt(msg, pvk)
print("texto descifrado:", nuevo)

signed = sign(plaintext, pvk)
print("cosa firmada:", signed)
print("se comprueba si la firma es correcta:", verify(signed, pbk))
