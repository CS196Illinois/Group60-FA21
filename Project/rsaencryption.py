# pip install pycryptodome

import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random

random_generator = Random.new().read
key = RSA.generate(2048, random_generator) #generate public and private keys

public_key = key.publickey # pub key export for exchange

encrypted = public_key.encrypt('encrypt this message', 32)
#message to encrypt is in the above line 'encrypt this message'

print('encrypted message: ' + encrypted) #ciphertext

f = open ('encryption.txt', 'w')
f.write(str(encrypted)) #write ciphertext to file
f.close()

#decrypted code below

f = open ('encryption.txt', 'r')
message = f.read()

decrypted = key.decrypt(message)

print('decrypted: ' + decrypted)

f = open ('encryption.txt', 'w')
f.write(str(message))
f.write(str(decrypted))
f.close()

"""helpful reading: https://www.pythonpool.com/rsa-encryption-python/, 
https://pycryptodome.readthedocs.io/en/latest/src/public_key/rsa.html
https://pycryptodome.readthedocs.io/en/latest/src/public_key/rsa.html
implementation: https://stackoverflow.com/questions/rsa-encryption-and-decryption-in-python"""
