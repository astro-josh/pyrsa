from math import sqrt
#import tkinter import *
import tkinter as tk
from tkinter import ttk

class RSA(object):
    def __init__(self, n=None, e=None, d=None, pq=None):
        self.n = n
        self.e = e
        self.d = d
        self.pq = pq


    def crack(self, n, e):
        """
        Find private key (d) given public key values (n, e)
        """
        self.n = n
        self.e = e

        self.pq = RSA.find_prime_factor(n)
        self.d = RSA.extended_euclidean(e, (self.pq[0] - 1) * (self.pq[1] - 1))

        return (self.d, self.pq)


    def decrypt(self, c, n=None, e=None, d=None):
        """
        Wrapper function for decryption process.
        Input:
        c - ciphertext as a number
        n - (optional) public key value n
        e - (optional) public key value e
        d - (optional) private key value d
        """
        if self.d:
            print(f"d:{self.d}, n:{self.n}, e:{self.e}")
        elif all([n, e]):
            self.crack(n, e)
        else:
            print("Must call crack(n, e) function first or call decrypt() with"
                " n and e parameters.")
            return

        m = RSA.modular_exponentiation(c, self.d, self.n)

        print(f"p, q = {self.pq}")
        print(f"d = {self.d}")
        print(f"m = {m}")

        return RSA.convert_num_to_text(m)


    @staticmethod
    def extended_euclidean(e, pq):
        """
        Finds the modular inverse of a number given the number and the modulus.
        Finds d for RSA.
        """
        remainder = 1
        p = 0
        mod = pq

        A = [0, 1]
        Q = []

        while remainder != 0:
            remainder = pq % e
            quotient = pq // e
            Q.append(quotient)

            if p != 0 and p != 1:
                num = (A[p - 2] - (A[p - 1] * Q[p - 2])) % mod

                A.append(num)

            pq = e
            e = remainder
            p += 1

        num = (A[p - 2] - (A[p - 1] * Q[p - 2])) % mod

        A.append(num)

        return A[p]


    @staticmethod
    def find_prime_factor(num):
        """
        Finds two prime factors for a given number.
        i.e. two numbers whose product equals the given number.
        """
        prime_numbers = [2]

        # TODO: list comprehension
        for x in range(3, num, 2):
            if RSA.is_prime(x):
                prime_numbers.append(x)

        for x in reversed(prime_numbers):
            for y in reversed(prime_numbers):
                if x * y == num:
                    return [x, y]

        return None


    @staticmethod
    def modular_exponentiation(num, exp, mod):
        """
        Performs modular exponentiation by repeated squaring.
        """
        result = 1

        for x in range(exp):
            result = ((result * num) % mod)

        return result


    def convert_to_text(numbers):
        return [convert_num_to_text(x) for x in numbers]


    @staticmethod
    def convert_num_to_text(num):
        """
        Converts numbers back to letters by reversing the encryption a * 26^2 + b * 26 + c
        """
        # a = int(num % 26)
        # temp = (num - a) // 26
        # b = int(temp % 26)
        # c = int((temp - b) // 26)
        #
        # # +97 for 0 index
        # return str(chr(c + 97) + chr(b + 97) + chr(a + 97))
        return str(chr(num))


    @staticmethod
    def is_prime(num):
        """
        Checks if a number is prime, returns boolean
        """
        if num == 2 or num == 3:
            return True

        if num % 2 == 0 or num % 3 == 0:
            return False

        for x in range(3, int(sqrt(num)), 2):
            if num % x == 0:
                return False

        # no factors found,å number is prime
        return True


def click_decrypt():
    rsa = RSA()
    rsa.crack(187, 3)
    plaintext_str.set(rsa.decrypt(int(cyphertext_str.get())))
    button_one.config(text="Decrypted")


gui = tk.Tk()
gui.geometry('600x400+300+300')
gui.title("RSA Decrypter")

button_one = ttk.Button(gui, text="Decrypt", command=click_decrypt)
button_one.grid(column=0, row=0, sticky='W')

button_two = ttk.Button(gui, text="Click 2")
button_two.grid(column=0, row=1, sticky='W')

cyphertext_label = ttk.Label(gui, text="Cyphertext")
cyphertext_label.grid(column=0, row=2, columnspan=3)

cyphertext_str = tk.StringVar(value='183')
cyphertext_entry = ttk.Entry(gui, width=50, textvariable=cyphertext_str)
cyphertext_entry.grid(column=0, row=3, columnspan=3)

plaintext_label = ttk.Label(gui, text="Plaintext")
plaintext_label.grid(column=0, row=4, columnspan=3)

plaintext_str = tk.StringVar()
plaintext_entry = ttk.Entry(gui, width=50, textvariable=plaintext_str)
plaintext_entry.grid(column=0, row=5, columnspan=3)

gui.mainloop()
