alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
modulo = 26


def char_to_num(c):
    return alphabet.index(c)


def num_to_char(num):
    return alphabet[num % modulo]


def inverse_matrix(matrix):
    det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    det_inv = None
    for i in range(modulo):
        if (det * i) % modulo == 1:
            det_inv = i
            break
    if det_inv == None:
        raise ValueError("The matrix is not invertible")

    adj = [[matrix[1][1], -matrix[0][1]], [-matrix[1][0], matrix[0][0]]]
    inv_matrix = [[(det_inv * adj[i][j]) % modulo for j in range(2)] for i in range(2)]
    return inv_matrix


def matrix_mul(m1, m2):
    r1, c1 = len(m1), len(m1[0])
    r2, c2 = len(m2), len(m2[0])

    if c1 != r2:
        raise ValueError("The matrices cannot be multiplied")

    result = [[0 for j in range(c2)] for i in range(r1)]
    for i in range(r1):
        for j in range(c2):
            for k in range(c1):
                result[i][j] += m1[i][k] * m2[k][j]
    result[i][j] %= modulo
    return result


def hill_encrypt(plaintext, key_matrix):
    plaintext = plaintext.upper().replace(" ", "")

    if len(plaintext) % 2 != 0:
        plaintext += "X"

    plain_nums = [char_to_num(c) for c in plaintext]
    ciphertext = ""

    for i in range(0, len(plain_nums), 2):
        plain_matrix = [[plain_nums[i]], [plain_nums[i + 1]]]
        cipher_matrix = matrix_mul(key_matrix, plain_matrix)
        ciphertext += num_to_char(cipher_matrix[0][0]) + num_to_char(cipher_matrix[1][0])

    return ciphertext


def hill_decrypt(ciphertext, key_matrix):
    ciphertext = ciphertext.upper().replace(" ", "")

    if len(ciphertext) % 2 != 0:
        raise ValueError("The ciphertext length must be even")

    cipher_nums = [char_to_num(c) for c in ciphertext]
    plaintext = ""

    for i in range(0, len(cipher_nums), 2):
        cipher_matrix = [[cipher_nums[i]], [cipher_nums[i + 1]]]
        plain_matrix = matrix_mul(inverse_matrix(key_matrix), cipher_matrix)
        plaintext += num_to_char(plain_matrix[0][0]) + num_to_char(plain_matrix[1][0])

    return plaintext.rstrip('X')  # Remove trailing 'X' characters


key_matrix = [[7, 8], [11, 11]]
plaintext = input("Enter your plaintext:")
ciphertext = hill_encrypt(plaintext, key_matrix)
print("Plaintext:", plaintext)
print("Ciphertext:", ciphertext)
print("Decrypted text:", hill_decrypt(ciphertext, key_matrix))
