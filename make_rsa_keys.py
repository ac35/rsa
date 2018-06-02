# RSA Key Generator
# http://inventwithpython.com/hacking (BSD Licensed)

import random
import sys
import os
import prime_number
import rsa_math


def main():
    pass


def generate_key(keysize=1024, silent=False):
    # Creates a public/private key pair with keys that are keySize bits in
    # size. This function may take a while to run.

    # Step 1: Create two prime numbers, p and q. Calculate n = p * q.
    # print('Generating p prime...')
    if not silent:
        print('Buat bilangan prima (p)...')
    p = prime_number.generate_large_prime(keysize)
    # print('Generating q prime...')
    if not silent:
        print('Buat bilangan prima (q)...')
    q = prime_number.generate_large_prime(keysize)
    n = p * q

    # Step 2: Create a number e that is relatively prime to (p-1)*(q-1).
    # print('Generating e that is relatively prime to (p-1)*(q-1)...')
    if not silent:
        print('Buat bilangan e yang relatif prima dengan (p-1)*(q-1)...')
    while True:
        # Keep trying random numbers for e until one is valid.
        e = random.randrange(2 ** (keysize - 1), 2 ** keysize)
        if rsa_math.gcd(e, (p - 1) * (q - 1)) == 1:
            break

    # Step 3: Calculate d, the mod inverse of e.
    # print('Calculating d that is mod inverse of e...')
    if not silent:
        print('Hitung d yaitu inverse dari e modulo (p-1)*(q-1)...')
    d = rsa_math.find_mod_inverse(e, (p - 1) * (q - 1))

    public_key = (n, e)
    private_key = (n, d)

    return public_key, private_key


def make_key_files(name, keysize=1024):
    # Creates two files 'x_pubkey.txt' and 'x_privkey.txt' (where x is the
    # value in name) with the the n,e and d,e integers written in them,
    # delimited by a comma.

    # Our safety check will prevent us from overwriting our old key files:
    if os.path.exists('%s_pubkey.txt' % name) or os.path.exists('%s_privkey.txt' % name):
        sys.exit('WARNING: The file %s_pubkey.txt or %s_privkey.txt already exists! Use a different name '
                 'or delete these files and re-run this program.' % (name, name))
    # start = time.time() # time start
    public_key, private_key = generate_key(keysize)
    # totalTime = time.time() - start
    # print('Time required to generate public and private key: %s\n' % (totalTime))
    print('The public key is a %s and a %s digit number.' % (len(str(public_key[0])), len(str(public_key[1]))))
    print('Writing public key to file %s_pubkey.txt...' % name)
    fo = open('%s_pubkey.txt' % name, 'w')
    fo.write('%s,%s,%s' % (keysize, public_key[0], public_key[1]))
    # fo.write('%s,%s,%s' % (hex(keysize), hex(public_key[0]), hex(public_key[1])))  # ganti jadi dlm bentuk heksadesimal
    fo.close()
    print()
    print('The private key is a %s and a %s digit number.' % (len(str(private_key[0])), len(str(private_key[1]))))
    print('Writing private key to file %s_privkey.txt...' % name)
    fo = open('%s_privkey.txt' % name, 'w')
    fo.write('%s,%s,%s' % (keysize, private_key[0], private_key[1]))
    # fo.write('%s,%s,%s' % (hex(keysize), hex(private_key[0]), hex(private_key[1])))
    fo.close()


'''
def makeKeyFiles(username, keySize):
    userDir = os.getcwd() + '\data\%s\keys\\' % username
    publicKey, privateKey = generateKey(keySize)

    fo = open(userDir + '%s_pubkey.txt' % username, 'w')
    fo.write('%s,%s,%s' % (keySize, publicKey[0], publicKey[1]))
    fo.close()

    fo = open(userDir + '%s_privkey.txt' % username, 'w')
    fo.write('%s,%s,%s' % (keySize, privateKey[0], privateKey[1]))
    fo.close()
'''


# If makeRsaKeys.py is run (instead of imported as a module) call
# the main() function.
if __name__ == '__main__':
    main()
