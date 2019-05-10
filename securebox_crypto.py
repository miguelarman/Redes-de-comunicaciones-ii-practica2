"""
    Prácticas de Redes de comunicaciones 2

    Autores:
        Miguel Arconada Manteca
        Mario García Pascual
"""

import os
import sys

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15

from generales import *

"""
Funcion de cifrado usando un esquema híbrido.

Args:
    plaintext (str): El texto plano a cifrar.
    publickey (RsaKey): La clave pública RSA con la que se quiere cifrar

Returns:
    Devuelve el IV + Clave simétrica cifrada RSA + Texto cifrado AES
"""
def encrypt(plaintext, publickey):
    # Se genera la clave simetrica
    session_key = get_random_bytes(AES_KEY_LENGTH)

    # Se encripta el texto plano con la clave simetrica
    cipher_aes = AES.new(session_key, AES.MODE_CBC)
    ciphertext = cipher_aes.encrypt(pad(plaintext, BLOCK_SIZE))

    # Se obtiene el iv y se encripta la clave simetrica
    cipher_rsa = PKCS1_OAEP.new(publickey)
    iv = cipher_aes.iv
    enc_session_key = cipher_rsa.encrypt(session_key)

    return iv + enc_session_key + ciphertext


"""
Función de descifrado usando un esquema híbrido.

Args:
    enveloped (str): El sobre a descifrar.
    privatekey (RsaKey): La clave privada RSA con la que se quiere descifrar

Returns:
    Devuelve el texto plano obtenido.
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
    plaintext = unpad(cipher_aes.decrypt(ciphertext), BLOCK_SIZE)

    return plaintext


"""
Función de firmado.

Args:
    plaintext (str): Texto plano a firmar.
    privatekey (RsaKey): Clave privada RSA con la que se quiere firmar.

Returns:
    Devuelve la firma + texto plano.
"""
def sign(plaintext, privatekey):
    # Se obtiene el hash del texto plano
    hashed_plaintext = SHA256.new(plaintext)
    signature = pkcs1_15.new(privatekey).sign(hashed_plaintext)
    return signature + plaintext


"""
Función que quita la firma de un texto firmado.

Args:
    signed (str): texto firmado.

Returns:
    El texto sin la firma.
"""
def unsign(signed):
    return signed[256:]


"""
Función para verificar una firma.

Args:
    signed (str): texto firmado.
    publickey (RsaKey): Clave pública RSA con la que se quiere verificar.

Returns:
    True en el caso de que se verifique la firma; False en caso contrario.
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
