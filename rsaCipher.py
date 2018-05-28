# RSA Cipher
# http://inventwithpython.com/hacking (BSD Licensed)

import sys, time

# IMPORTANT: The block size MUST be less than or equal to the key size!
# (Note: The block size is in bytes, the key size is in bits. There
# are 8 bits in 1 byte.)
DEFAULT_BLOCK_SIZE = 128 # 128 bytes
BYTE_SIZE = 256 # One byte has 256 different values.

def main():
    # Runs a test that encrypts a message to a file or decrypts a message
    # from a file.
    filename = 'encrypted_file.txt' # the file to write to/read from
    mode = 'encrypt' # set to 'encrypt' or 'decrypt'

    if mode == 'encrypt':
        message = '''"Journalists belong in the gutter because that is where the ruling classes throw their guilty secrets." -Gerald Priestland "The Founding Fathers gave the free press the protection it must have to bare the secrets of government and inform the people." -Hugo Black'''
        pubKeyFilename = 'al_sweigart_pubkey.txt'
        print('Encrypting and writing to %s...' % (filename))
        start = time.time()
        encryptedText = encryptAndWriteToFile(filename, pubKeyFilename, message)
        totalTime = time.time() - start
        print('Time to encrypt: %s' % (totalTime))
        print()
        print('Encrypted text:')
        print(encryptedText)

    elif mode == 'decrypt':
        privKeyFilename = 'al_sweigart_privkey.txt'
        print('Reading from %s and decrypting...' % (filename))
        start = time.time()
        decryptedText = readFromFileAndDecrypt(filename, privKeyFilename)
        totalTime = time.time() - start
        print('Time to decrypt: %s' % (totalTime))        

        print('Decrypted text:')
        print(decryptedText)


def getBlocksFromText(message, blockSize=DEFAULT_BLOCK_SIZE):
    # Converts a string message to a list of block integers. Each integer
    # represents 128 (or whatever blockSize is set to) string characters.

    # messageBytes = message.encode('ascii') # convert the string to bytes

    blockInts = []
    for blockStart in range(0, len(message), blockSize):
        # Calculate the block integer for this block of text
        blockInt = 0
        for i in range(blockStart, min(blockStart + blockSize, len(message))):
            blockInt += ord(message[i]) * (BYTE_SIZE ** (i % blockSize))
        blockInts.append(blockInt)
    return blockInts


def getTextFromBlocks(blockInts, messageLength, blockSize=DEFAULT_BLOCK_SIZE):
    # Converts a list of block integers to the original message string.
    # The original message length is needed to properly convert the last
    # block integer.
    message = []
    for blockInt in blockInts:
        blockMessage = []
        for i in range(blockSize - 1, -1, -1):
            if len(message) + i < messageLength:
                # Decode the message string for the 128 (or whatever
                # blockSize is set to) characters from this block integer.
                asciiNumber = blockInt // (BYTE_SIZE ** i)
                blockInt = blockInt % (BYTE_SIZE ** i)
                blockMessage.insert(0, chr(asciiNumber))
        message.extend(blockMessage)
    return ''.join(message)

'''
def encryptMessage(message, key, blockSize=DEFAULT_BLOCK_SIZE):
    # Converts the message string into a list of block integers, and then
    # encrypts each block integer. Pass the PUBLIC key to encrypt.
    encryptedBlocks = []
    n, e = key

    for block in getBlocksFromText(message, blockSize):
        # ciphertext = plaintext ^ e mod n
        encryptedBlocks.append(pow(block, e, n))
    return encryptedBlocks
'''

def encryptMessage(message, key, mode=None, blockSize=DEFAULT_BLOCK_SIZE):
    # Converts the message string into a list of block integers, and then
    # encrypts each block integer. Pass the PUBLIC key to encrypt.
    encryptedBlocks = []
    if mode == None:
        pass  
    elif mode.lower() == 'encrypt':
        n, e = key
        for block in getBlocksFromText(message, blockSize):
            # ciphertext = plaintext ^ e mod n
            encryptedBlocks.append(pow(block, e, n))
    elif mode.lower() == 'signature':
        n, d = key
        for block in getBlocksFromText(message, blockSize):
            encryptedBlocks.append(pow(block, d, n))
    return encryptedBlocks


def decryptMessage(encryptedBlocks, messageLength, key, mode=None, blockSize=DEFAULT_BLOCK_SIZE):
    # Decrypts a list of encrypted block ints into the original message
    # string. The original message length is required to properly decrypt
    # the last block. Be sure to pass the PRIVATE key to decrypt.
    decryptedBlocks = []
    if mode.lower() == 'decrypt':
        n, d = key
        for block in encryptedBlocks:
            # plaintext = ciphertext ^ d mod n
            decryptedBlocks.append(pow(block, d, n))
    elif mode.lower() == 'signature':
        n, e = key
        for block in encryptedBlocks:
            # plaintext = ciphertext ^ d mod n
            decryptedBlocks.append(pow(block, e, n))        
    return getTextFromBlocks(decryptedBlocks, messageLength, blockSize)


def readKeyFile(keyFile):
    # Given the filename of a file that contains a public or private key,
    # return the key as a (n,e) or (n,d) tuple value.
    fo = open(keyFile)
    content = fo.read()
    fo.close()
    keySize, n, EorD = content.split(',')
    return (int(keySize), int(n), int(EorD))

def signing():
    pass


def encrypt(public_key, message, blockSize=DEFAULT_BLOCK_SIZE):
    # Using a key from a key file, encrypt the message and save it to a
    # file. Returns the encrypted message string.
    keySize, n, e = public_key

    # Check that key size is greater than block size.
    if keySize < blockSize * 8: # * 8 to convert bytes to bits
        sys.exit('ERROR: Block size is %s bits and key size is %s bits. The RSA cipher requires the block size to be equal to or greater than the key size. Either decrease the block size or use different keys.' % (blockSize * 8, keySize))

    # Encrypt the message
    encryptedBlocks = encryptMessage(message=message, key=(n, e), mode='encrypt', blockSize=blockSize)

    # Convert the large int values to one string value.
    for i in range(len(encryptedBlocks)):
        encryptedBlocks[i] = str(encryptedBlocks[i])

    # jika isi blok di dlm encryptedBlocks lebih dari 1 (> 1)
    if len(encryptedBlocks) > 1:
        # bikin encryptedContent dengan memecah blok-blok menggunakan ','
        encryptedContent = ','.join(encryptedBlocks)
    # tapi jika blok isinya hanya 1, tidak pakai ','
    encryptedContent = encryptedBlocks[0] 

    # Write out the encrypted string to the output file.
    encryptedContent = '%s_%s_%s' % (len(message), blockSize, encryptedContent)

    return encryptedContent


def signature(private_key, message, blockSize=DEFAULT_BLOCK_SIZE):
    # Using a key from a key file, encrypt the message and save it to a
    # file. Returns the encrypted message string.
    keySize, n, d = private_key # baca private key pengirim

    # Check that key size is greater than block size.
    if keySize < blockSize * 8: # * 8 to convert bytes to bits
        sys.exit('ERROR: Block size is %s bits and key size is %s bits. The RSA cipher requires the block size to be equal to or greater than the key size. Either decrease the block size or use different keys.' % (blockSize * 8, keySize))

    # Encrypt the message
    encryptedBlocks = encryptMessage(message=message, key=(n, d), mode='encrypt', blockSize=blockSize)

    # Convert the large int values to one string value.
    for i in range(len(encryptedBlocks)):
        encryptedBlocks[i] = str(encryptedBlocks[i])

    # jika isi blok di dlm encryptedBlocks lebih dari 1 (> 1)
    if len(encryptedBlocks) > 1:
        # bikin encryptedContent dengan memecah blok-blok menggunakan ','
        encryptedContent = ','.join(encryptedBlocks)
    # tapi jika blok isinya hanya 1, tidak pakai ','
    encryptedContent = encryptedBlocks[0] 

    # Write out the encrypted string to the output file.
    encryptedContent = '%s_%s_%s' % (len(message), blockSize, encryptedContent)

    return encryptedContent



def decrypt(private_key, message):
    # Using a key from a key file, read an encrypted message from a file
    # and then decrypt it. Returns the decrypted message string.
    keySize, n, d = private_key


    # Read in the message length and the encrypted message from the file.
    messageLength, blockSize, encryptedMessage = message.split('_')
    messageLength = int(messageLength)
    blockSize = int(blockSize)

    # Check that key size is greater than block size.
    if keySize < blockSize * 8: # * 8 to convert bytes to bits
        sys.exit('ERROR: Block size is %s bits and key size is %s bits. The RSA cipher requires the block size to be equal to or greater than the key size. Did you specify the correct key file and encrypted file?' % (blockSize * 8, keySize))

    # Convert the encrypted message into large int values.

    encryptedBlocks = []

    # jika isi blok di dlm encryptedMessage lebih dari 1 (> 1)
    if len(encryptedMessage) > 1:
        # ambil blok-blok dengan memisahkannya dari tanda ','
        for block in encryptedMessage.split(','):
            encryptedBlocks.append(int(block))
    # isi blok kurang dari 1, langsung aja isi
    encryptedBlocks.append(int(block))

    # Decrypt the large int values.
    return decryptMessage(encryptedBlocks=encryptedBlocks,
        messageLength=messageLength, key=(n, d), mode="decrypt" ,blockSize=blockSize)


# def verify_signature(public_key, message):
def decrypt_signature(public_key, message):
    # Using a key from a key file, read an encrypted message from a file
    # and then decrypt it. Returns the decrypted message string.
    keySize, n, e = public_key


    # Read in the message length and the encrypted message from the file.
    messageLength, blockSize, encryptedMessage = message.split('_')
    messageLength = int(messageLength)
    blockSize = int(blockSize)

    # Check that key size is greater than block size.
    if keySize < blockSize * 8: # * 8 to convert bytes to bits
        sys.exit('ERROR: Block size is %s bits and key size is %s bits. The RSA cipher requires the block size to be equal to or greater than the key size. Did you specify the correct key file and encrypted file?' % (blockSize * 8, keySize))

    # Convert the encrypted message into large int values.

    encryptedBlocks = []

    # jika isi blok di dlm encryptedMessage lebih dari 1 (> 1)
    if len(encryptedMessage) > 1:
        # ambil blok-blok dengan memisahkannya dari tanda ','
        for block in encryptedMessage.split(','):
            encryptedBlocks.append(int(block))
    # isi blok kurang dari 1, langsung aja isi
    encryptedBlocks.append(int(block))

    # Decrypt the large int values.
    return decryptMessage(encryptedBlocks=encryptedBlocks, 
        messageLength=messageLength, key=(n, e), mode="signature", blockSize=blockSize)



'''
def readKeyFile(user, pubKey=False, privKey=False):
    # Given the filename of a file that contains a public or private key,
    # return the key as a (n,e) or (n,d) tuple value.
    # user adalah objek (instance) dari kelas User
    username = user.username    
    userkeysDir = os.getcwd() + '\\data\\%s\\keys\\' % username
    
    if pubKey == True:
        KeyFilename = user.publicKey
    elif privKey == True:
        keyFilename = user.privateKey
    elif pubkey == True and privKey == True:
        return None    

    keyLocation = os.path.join(userKeysDir, keyFilename) 

    # baca key
    f = open(keyLocation)
    content = f.read()
    f.close()
    keySize, n, EorD = content.split(',')
    return (int(keySize), int(n), int(EorD))


def encrypt(user, message, mode='' ,blockSize=DEFAULT_BLOCK_SIZE):
    # Using a key from a key file, encrypt the message and save it to a
    # file. Returns the encrypted message string.
    if mode == 'ds' or mode == 'signing':
        # digital signature, pake private key
        keySize, n, d = readKeyFile(user, privKey=True)
        if keySize < blockSize * 8:
            return None
        encryptedBlocks = encryptMessage(message, (n, d), blockSize)    
    # encrypt biasa, pake public key    
    keySize, n, e = readKeyFile(user, pubKey=True)

    # Check that key size is greater than block size.
    if keySize < blockSize * 8: # * 8 to convert bytes to bits
        # sys.exit('ERROR: Block size is %s bits and key size is %s bits. The RSA cipher requires the block size to be equal to or greater than the key size. Either decrease the block size or use different keys.' % (blockSize * 8, keySize))
        return None

    # Encrypt the message
    encryptedBlocks = encryptMessage(message, (n, e), blockSize)

    # Convert the large int values to one string value.
    for i in range(len(encryptedBlocks)):
        encryptedBlocks[i] = str(encryptedBlocks[i])
    encryptedContent = ','.join(encryptedBlocks)

    encryptedContent = '%s_%s_%s' % (len(message), blockSize, encryptedContent)

    # return the encrypted string.
    return encryptedContent
'''




# If rsaCipher.py is run (instead of imported as a module) call
# the main() function.
if __name__ == '__main__':
    main()