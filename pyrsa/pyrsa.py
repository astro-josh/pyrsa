import argparse
from os import environ
from math import sqrt
import tkinter as tk
from tkinter import ttk

__all__ = ['RSA']

class RSA(object):
    def __init__(self, n=None, e=None, d=None, pq=None):
        self.n = n
        self.e = e
        self.d = d
        self.pq = pq


    def decrypt(self, c, n=None, e=None, d=None):
        """
        Wrapper function for decryption process.
        Input:
        c - ciphertext: space serperated list of numbers, int or string
        n - (optional) public key value n
        e - (optional) public key value e
        d - (optional) private key value d
        """
        if isinstance(c, str):
            c = c.split(" ")
        elif isinstance(c, int):
            c = [c]

        if d:
            seld.d = d

        if all([n, e]):
            self.n = n
            self.e = e

        if self.d:
            print(f"d:{self.d}, n:{self.n}, e:{self.e}")
        elif all([self.n, self.e]):
            self.d, self.pq = RSA.crack(self.n, self.e)
        else:
            print("Error: n and/or e value(s) not given in construction or method call.")
            return

        numbers = [RSA.modular_exponentiation(int(x), self.d, self.n) for x in c]

        print(f"p, q = {self.pq}")
        print(f"d = {self.d}")

        return RSA.convert_nums_to_text(numbers)


    @staticmethod
    def crack(n, e):
        """
        Find private key (d) given public key values (n, e)
        """

        pq = RSA.find_prime_factor(n)
        d = RSA.extended_euclidean(e, (pq[0] - 1) * (pq[1] - 1))

        return (d, pq)


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
        i.e. two prime numbers whose product equals the given number.
        """
        if num % 2 == 0:
            return None

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


    def convert_nums_to_text(numbers):
        return " ".join([RSA.convert_num_to_text(x) for x in numbers])


    @staticmethod
    def convert_num_to_text(num):
        """
        Converts numbers back to letters by reversing the encryption
        a * 26^2 + b * 26 + c
        """
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

        # no factors found, number is prime
        return True


def get_input():
    """
    Get input from user, return dictionary of input.
    """
    n = int(input('Enter n value: '))
    e = int(input('Enter e value: '))
    c = input('Enter cyphertext (space seperated ints): ')

    return {'n':n, 'e':e, 'c':c}


def click_decrypt():
    """
    Decrypt button click function.
    Gets n, e, and cypher text values from gui entries,
    then decrypts and adds resulting plaintext to entry field.
    """
    rsa = RSA()
    rsa.crack(int(n_str.get()), int(e_str.get()))
    plaintext_str.set(rsa.decrypt(cyphertext_str.get()))


def start_gui():
    global n_str
    global e_str
    global plaintext_str
    global cyphertext_str

    gui = tk.Tk()
    gui.geometry('600x400+300+300')
    gui.title("RSA Decrypter")

    n_label = ttk.Label(gui, text="n")
    n_label.grid(column=0, row=0, sticky='E')

    n_str = tk.StringVar(value='187')
    n_entry = ttk.Entry(gui, textvariable=n_str)
    n_entry.grid(column=1, row=0, sticky='W', columnspan=2)

    e_label = ttk.Label(gui, text="e")
    e_label.grid(column=0, row=1, sticky='E')

    e_str = tk.StringVar(value='3')
    e_entry = ttk.Entry(gui, textvariable=e_str)
    e_entry.grid(column=1, row=1, stick='W', columnspan=2)

    button_one = ttk.Button(gui, text="Decrypt", command=click_decrypt)
    button_one.grid(column=1, row=2, columnspan=3)

    cyphertext_label = ttk.Label(gui, text="Cyphertext")
    cyphertext_label.grid(column=1, row=3, columnspan=3)

    cyphertext_str = tk.StringVar(value='183')
    cyphertext_entry = ttk.Entry(gui, textvariable=cyphertext_str)
    cyphertext_entry.grid(column=1, row=4)

    plaintext_label = ttk.Label(gui, text="Plaintext")
    plaintext_label.grid(column=1, row=5, columnspan=3)

    plaintext_str = tk.StringVar()
    plaintext_entry = ttk.Entry(gui, textvariable=plaintext_str)
    plaintext_entry.grid(column=1, row=6, columnspan=3)

    gui.mainloop()


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--gui', '-g', action="store_true", dest='gui',
                            help='Start GUI.', required=False)

    args = parser.parse_args()

    if args.gui and environ["DISPLAY"] != "":
        start_gui()
    else:
        user_input = get_input()
        rsa = RSA(n=user_input['n'], e=user_input['e'])
        print(rsa.decrypt(user_input['c']))


if (__name__ == '__main__'):
    main()
