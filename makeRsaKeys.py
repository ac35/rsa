# RSA Key Generator
# http://inventwithpython.com/hacking (BSD Licensed)

import random, sys, os, rabinMiller, cryptomath, time

def main():
    pass
    '''
    create a public/private keypair with 1024 bit keys
    print('Making key files...')
    makeKeyFiles('alvin', 1024)
    print('Key files made.')
    '''

'''    
def format_keys(keySize, publicKey, privateKey):
    # konversi ke str kemudian concat
    # lebih baik simpan dalam bentuk file ke suatu lokasi (yg aman?)
    publicKey = str(keySize) + ',' + str(publicKey[0]) + ',' + str(publicKey[1])
    privateKey = str(keySize) + ',' + str(privateKey[0]) + ',' + str(privateKey[1])
    return (publicKey, privateKey)
'''

def generateKey(keySize=1024):
    # Creates a public/private key pair with keys that are keySize bits in
    # size. This function may take a while to run.

    # Step 1: Create two prime numbers, p and q. Calculate n = p * q.
    print('Generating p prime...')
    p = rabinMiller.generateLargePrime(keySize)
    print('Generating q prime...')
    q = rabinMiller.generateLargePrime(keySize)
    n = p * q

    # Step 2: Create a number e that is relatively prime to (p-1)*(q-1).
    print('Generating e that is relatively prime to (p-1)*(q-1)...')
    while True:
        # Keep trying random numbers for e until one is valid.
        e = random.randrange(2 ** (keySize - 1), 2 ** (keySize))
        if cryptomath.gcd(e, (p - 1) * (q - 1)) == 1:
            break

    # Step 3: Calculate d, the mod inverse of e.
    print('Calculating d that is mod inverse of e...')
    d = cryptomath.findModInverse(e, (p - 1) * (q - 1))

    publicKey = (n, e)
    privateKey = (n, d)

    return (publicKey, privateKey)


def makeKeyFiles(name, keySize):
    # Creates two files 'x_pubkey.txt' and 'x_privkey.txt' (where x is the
    # value in name) with the the n,e and d,e integers written in them,
    # delimited by a comma.

    # Our safety check will prevent us from overwriting our old key files:
    if os.path.exists('%s_pubkey.txt' % (name)) or os.path.exists('%s_privkey.txt' % (name)):
        sys.exit('WARNING: The file %s_pubkey.txt or %s_privkey.txt already exists! Use a different name or delete these files and re-run this program.' % (name, name))
    # start = time.time() # time start
    publicKey, privateKey = generateKey(keySize)
    # totalTime = time.time() - start
    # print('Time required to generate public and private key: %s\n' % (totalTime))
    print('The public key is a %s and a %s digit number.' % (len(str(publicKey[0])), len(str(publicKey[1]))))
    print('Writing public key to file %s_pubkey.txt...' % (name))
    fo = open('%s_pubkey.txt' % (name), 'w')
    fo.write('%s,%s,%s' % (keySize, publicKey[0], publicKey[1]))
    fo.close()

    print()
    print('The private key is a %s and a %s digit number.' % (len(str(privateKey[0])), len(str(privateKey[1]))))
    print('Writing private key to file %s_privkey.txt...' % (name))
    fo = open('%s_privkey.txt' % (name), 'w')
    fo.write('%s,%s,%s' % (keySize, privateKey[0], privateKey[1]))
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