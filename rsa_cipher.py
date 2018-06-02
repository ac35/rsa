# RSA Cipher
# http://inventwithpython.com/hacking (BSD Licensed)

import sys

# IMPORTANT: The block size MUST be less than or equal to the key size!
# (Note: The block size is in bytes, the key size is in bits. There
# are 8 bits in 1 byte.)
DEFAULT_BLOCK_SIZE = 128  # 128 bytes
BYTE_SIZE = 256  # One byte has 256 different values.


def main():
    pass
    # # Runs a test that encrypts a message to a file or decrypts a message
    # # from a file.
    # filename = 'encrypted_file.txt' # the file to write to/read from
    # mode = 'encrypt' # set to 'encrypt' or 'decrypt'
    #
    # if mode == 'encrypt':
    #     message = '''"Journalists belong in the gutter because that is where the ruling classes throw their guilty secrets." -Gerald Priestland "The Founding Fathers gave the free press the protection it must have to bare the secrets of government and inform the people." -Hugo Black'''
    #     pubKeyFilename = 'al_sweigart_pubkey.txt'
    #     print('Encrypting and writing to %s...' % (filename))
    #     start = time.time()
    #     encryptedText = encryptAndWriteToFile(filename, pubKeyFilename, message)
    #     totalTime = time.time() - start
    #     print('Time to encrypt: %s' % (totalTime))
    #     print()
    #     print('Encrypted text:')
    #     print(encryptedText)
    #
    # elif mode == 'decrypt':
    #     privKeyFilename = 'al_sweigart_privkey.txt'
    #     print('Reading from %s and decrypting...' % (filename))
    #     start = time.time()
    #     decryptedText = readFromFileAndDecrypt(filename, privKeyFilename)
    #     totalTime = time.time() - start
    #     print('Time to decrypt: %s' % (totalTime))
    #
    #     print('Decrypted text:')
    #     print(decryptedText)


def get_blocks_from_text(message, block_size=DEFAULT_BLOCK_SIZE):
    # Converts a string message to a list of block integers. Each integer
    # represents 128 (or whatever blockSize is set to) string characters.

    # messageBytes = message.encode('ascii') # convert the string to bytes

    block_ints = []
    for block_start in range(0, len(message), block_size):
        # Calculate the block integer for this block of text
        block_int = 0
        for i in range(block_start, min(block_start + block_size, len(message))):
            block_int += ord(message[i]) * (BYTE_SIZE ** (i % block_size))
        block_ints.append(block_int)
    return block_ints


def get_text_from_blocks(block_ints, message_length, block_size=DEFAULT_BLOCK_SIZE):
    # Converts a list of block integers to the original message string.
    # The original message length is needed to properly convert the last
    # block integer.
    message = []
    for block_int in block_ints:
        block_message = []
        for i in range(block_size - 1, -1, -1):
            if len(message) + i < message_length:
                # Decode the message string for the 128 (or whatever
                # blockSize is set to) characters from this block integer.
                ascii_number = block_int // (BYTE_SIZE ** i)
                block_int = block_int % (BYTE_SIZE ** i)
                block_message.insert(0, chr(ascii_number))
        message.extend(block_message)
    return ''.join(message)


def encrypt_message(message, key, block_size=DEFAULT_BLOCK_SIZE):
    # Converts the message string into a list of block integers, and then
    # encrypts each block integer. Pass the PUBLIC key to encrypt.
    encrypted_blocks = []
    n, e_or_d = key
    for block in get_blocks_from_text(message, block_size):
        # ciphertext = plaintext ^ e mod n
        encrypted_blocks.append(pow(block, e_or_d, n))
    return encrypted_blocks


def decrypt_message(encrypted_blocks, message_length, key, block_size=DEFAULT_BLOCK_SIZE):
    # Decrypts a list of encrypted block ints into the original message
    # string. The original message length is required to properly decrypt
    # the last block. Be sure to pass the PRIVATE key to decrypt.
    decrypted_blocks = []
    n, e_or_d = key
    for block in encrypted_blocks:
        decrypted_blocks.append(pow(block, e_or_d, n))
    return get_text_from_blocks(decrypted_blocks, message_length, block_size)


def read_key_file(key_file):
    # Given the filename of a file that contains a public or private key,
    # return the key as a (n,e) or (n,d) tuple value.
    fo = open(key_file)
    content = fo.read()
    fo.close()
    key_size, n, e_or_d = content.split(',')
    return int(key_size), int(n), int(e_or_d)


def encrypt(key, message, block_size=DEFAULT_BLOCK_SIZE):
    # Enkripsi message
    # Using a key from a key file, encrypt the message and save it to a
    # file. Returns the encrypted message string.

    key_size, n, e_or_d = key  # bongkar key

    # Check that key size is greater than block size.
    if key_size < block_size * 8:  # * 8 to convert bytes to bits
        sys.exit('ERROR: Block size is %s bits and key size is %s bits. The RSA cipher requires the block size '
                 'to be equal to or greater than the key size. Either decrease the block size or use different keys.' %
                 (block_size * 8, key_size))

    # Encrypt the message
    encrypted_blocks = encrypt_message(message=message, key=(n, e_or_d), block_size=block_size)

    # Convert the large int values to one string value.
    # for i in range(len(encrypted_blocks)):
    #     encrypted_blocks[i] = str(encrypted_blocks[i])
    #
    # encrypted_content = ''
    # # jika isi blok di dlm encryptedBlocks lebih dari 1
    # if len(encrypted_blocks) > 1:
    #     # bikin encryptedContent dengan memecah blok-blok menggunakan ','
    #     encrypted_content += ','.join(encrypted_blocks)
    # # tapi jika blok isinya hanya 1, tidak pakai ','
    # encrypted_content += encrypted_blocks[0]
    #
    # Write out the encrypted string to the output file.
    # output = '%s_%s_%s' % (len(message), block_size, encrypted_content)

    for i in range(len(encrypted_blocks)):
        encrypted_blocks[i] = str(encrypted_blocks[i])
    encrypted_content = ','.join(encrypted_blocks)

    # Write out the encrypted string to the output file.
    output = '%s_%s_%s' % (len(message), block_size, encrypted_content)

    return output


digital_signature = encrypt


def decrypt(key, message):
    # Using a key from a key file, read an encrypted message from a file
    # and then decrypt it. Returns the decrypted message string.
    key_size, n, e_or_d = key

    # Read in the message length and the encrypted message from the file.
    message_length, block_size, encrypted_message = message.split('_')
    message_length = int(message_length)
    block_size = int(block_size)

    # Check that key size is greater than block size.
    if key_size < block_size * 8:  # * 8 to convert bytes to bits
        sys.exit('ERROR: Block size is %s bits and key size is %s bits. The RSA cipher requires the block size '
                 'to be equal to or greater than the key size. Did you specify the correct key file and '
                 'encrypted file?' % (block_size * 8, key_size))

    # Convert the encrypted message into large int values.
    encrypted_blocks = []

    '''
    # jika isi blok di dlm encryptedMessage lebih dari 1 (> 1)
    if len(encrypted_message) > 1:
        # ambil blok-blok dengan memisahkannya dari tanda ','
        for block in encrypted_message.split(','):
            encrypted_blocks.append(int(block))
    # isi blok kurang dari 1, langsung aja isi
    encrypted_blocks.append(int(block)) ######################################################### FIX THIS
    '''

    for block in encrypted_message.split(','):
        encrypted_blocks.append(int(block))

    # Decrypt the large int values.
    return decrypt_message(encrypted_blocks=encrypted_blocks,
                           message_length=message_length, key=(n, e_or_d), block_size=block_size)


decrypt_signature = decrypt


if __name__ == '__main__':
    main()
