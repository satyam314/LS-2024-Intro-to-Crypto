# !pip install pycryptodome
import numpy as np

def keyMatrix(key):
    if len(key) != 9:
        print("Key should be of length 9")
        return np.identity(3, dtype=int)
    
    if not all('A' <= ch <= 'Z' for ch in key):
        print("Key should be from A to Z")
        return np.identity(3, dtype=int)
    
    keyMatrix = np.zeros((3, 3), dtype=int)
    for i in range(3):
        for j in range(3):
            keyMatrix[i][j] = (ord(key[3*i + j]) - ord('A')) % 26
    return keyMatrix

def encrypt(message, key):
    message = message.upper()
    keyMat = keyMatrix(key)
    
    n = len(message)
    if n % 3 != 0:
        message += 'X' * (3 - n % 3)
    
    cipher = ""
    for i in range(0, len(message), 3):
        messageVec = np.array([ord(message[i+j]) - ord('A') for j in range(3)]).reshape(3, 1)
        cipherVec = np.dot(keyMat, messageVec) % 26
        cipher += ''.join(chr(cipherVec[j][0] + ord('A')) for j in range(3))
    return cipher

def AdotBinv(A, B):
    adjoint = np.zeros((3, 3), dtype=int)
    for i in range(3):
        for j in range(3):
            adjoint[i][j] = (B[(j+1)%3][(i+1)%3] * B[(j+2)%3][(i+2)%3] - B[(j+1)%3][(i+2)%3] * B[(j+2)%3][(i+1)%3]) % 26
    
    det_B = int(np.round(np.linalg.det(B))) % 26
    det_inv = pow(det_B, -1, 26)
    
    ans = np.dot(A, adjoint) % 26
    ans = (ans * det_inv) % 26
    return ans

def key_discovery(cipher, message):
    message = message.upper()
    cipher = cipher.upper()
    
    if len(message) < 9:
        print("Key can't be resolved")
        return "AAAAAAAAA"
    
    msgMat = np.array([ord(message[3*i+j]) - ord('A') for i in range(3) for j in range(3)]).reshape(3, 3).T
    det = int(np.round(np.linalg.det(msgMat))) % 26
    
    if np.gcd(det, 26) != 1:
        return key_discovery(cipher[3:], message[3:])
    
    cipherMat = np.array([ord(cipher[3*i+j]) - ord('A') for i in range(3) for j in range(3)]).reshape(3, 3).T
    keyMat = AdotBinv(cipherMat, msgMat)
    
    key = ''.join(chr(keyMat[i//3][i%3] + ord('A')) for i in range(9))
    return key

# Testing the improved functions
if __name__ == "__main__":
    print(keyMatrix("GYBNQKURP"))
    print(encrypt("ACT", "GYBNQKURP"))
    print(encrypt("THISISYOU", "GYBNQKURP"))

    msgtext = "WHATAREYOUDOINGTHESEDAYSIAMWORKINGONHILLCIPHER"
    key = "HILLISEZY"
    cipher = encrypt(msgtext, key)
    print("cipher", cipher)

    discovered_key = key_discovery(cipher, msgtext)
    print("discovered_key", discovered_key)

    cipher_checked = encrypt(msgtext, discovered_key)
    print("cipher_checked", cipher_checked)

    if cipher == cipher_checked and key == discovered_key:
        print("Key found!!")
