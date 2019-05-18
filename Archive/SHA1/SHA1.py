import sys ; sys.path += ['.', '../..']
from bitstring import BitArray
import base64
import re

class SHA1():
    
    @staticmethod
    def createDigest(message, ml=None, h0=0x67452301, h1=0xEFCDAB89, h2=0x98BADCFE, h3=0x10325476, h4=0xC3D2E1F0, padding=True):
        """
        Creates a message digests for a bytes message.
        Output is in Base64
        """

        # Converts to binary
        messageBinary = BitArray(bytes=message).bin

        if ml is None:
            ml = len(messageBinary)

        # Adds padding to the value
        if padding: 
            messageBinary = SHA1.addPadding(messageBinary, ml)

        # Creates 512 bit chunks
        messageChunks = SHA1.splitStringIntoChunks(messageBinary, size=512)

        for chunk in messageChunks:

            # Split chunck into 32bit words
            # Should expect 16 chunks
            words = SHA1.splitStringIntoChunks(chunk, size=32)
            words += [0] * 64

            # Extends sixteen 32 bit values into eighty
            for i in range(16, 80):

                xor = int(words[i-3], 2) ^ int(words[i-8], 2) ^ \
                      int(words[i-14], 2) ^ int(words[i-16], 2)

                xor = SHA1.left_rotate(xor, shift=1)
                words[i] = format(xor, "032b")

           # Initialize hash value for this chunk:
            a = h0
            b = h1
            c = h2
            d = h3
            e = h4

            # Main loop
            for i in range(0, 80):
                if 0 <= i <= 19:
                    f = d ^ (b & (c ^ d))  
                    k = 0x5A827999

                elif 20 <= i <= 39:
                    f = b ^ c ^ d
                    k = 0x6ED9EBA1
                    
                elif 40 <= i <= 59:
                    f = (b & c) | (d & (b | c))
                    k = 0x8F1BBCDC

                else:
                    f = b ^ c ^ d
                    k = 0xCA62C1D6

                temp = SHA1.left_rotate(a, shift=5) + f + e + k + int(words[i], 2) & 0xffffffff
                e = d
                d = c
                c = SHA1.left_rotate(b, shift=30)
                b = a
                a = temp

            # Adds the result to the running hash
            h0 = (h0 + a) & 0xffffffff 
            h1 = (h1 + b) & 0xffffffff 
            h2 = (h2 + c) & 0xffffffff
            h3 = (h3 + d) & 0xffffffff
            h4 = (h4 + e) & 0xffffffff

        hexHash = '%08X%08X%08X%08X%08X' % (h0, h1, h2, h3, h4)
        return hexHash

    @staticmethod
    def addPadding(messageBinary, messageLength):
        """
        Adds padding defined in the SHA1 specification
        """

        if len(messageBinary) % 8 == 0:
            messageBinary += "1"

        # Adds zeros until padding is 64 bits away from 512
        while len(messageBinary) % 512 != 448:
            messageBinary += "0"

        # Add 64 bit integer of the length to make the message a multiple of 512
        lengthBin = format(messageLength, "064b")
        messageBinary += lengthBin
        
        return messageBinary

    @staticmethod
    def left_rotate(value, shift):
        """
        Shifts the bits a certain distance to the left
        """
        return ((value << shift) & 0xffffffff) | (value >> (32 - shift))

    @staticmethod
    def splitStringIntoChunks(string, size):
        """
        Splits a string into a set of characters
        """

        pattern = ".{" + str(size) + "}"

        return re.findall(pattern, string)


def loadPart(name):

    data = []
    with open(f"/home/main_user/GitHub/Cyber-Security-Individual-Project/Code/SHA1/SHAtteredSections/chunks/{name}", "rb") as file:
        data = file.read()

    return data


if __name__ == "__main__":
    
    sha = SHA1()

    prefix = loadPart("prefix")
    m1_1 = loadPart("m1_block1")
    m1_2 = loadPart("m1_block2")

    message1 = prefix + m1_1

    message2 = prefix + m1_2
    
    h1 = sha.createDigest(message1, padding=False)
    print(h1)

    h2 = sha.createDigest(message2, padding=False)
    print(h2)
