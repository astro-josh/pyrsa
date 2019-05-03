import logging
import argparse
from os import environ
from math import sqrt
import tkinter as tk
from tkinter import ttk

__all__ = ['RSA']

logger = logging.getLogger('pyrsa')
def init_logger():
    """
    Initialize logger.
    """
    logger.setLevel(logging.INFO)
    logging.basicConfig()
    logging.captureWarnings(True)


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
            logger.info(f"d:{self.d}, n:{self.n}, e:{self.e}")
        elif all([self.n, self.e]):
            self.d, self.pq = RSA.crack(self.n, self.e)
        else:
            logger.error("Error: n and/or e value(s) not given in construction or method call.")
            return

        numbers = [RSA.modular_exponentiation(int(x), self.d, self.n) for x in c]

        logger.info(f"p, q = {self.pq}")
        logger.info(f"d = {self.d}")

        return RSA.convert_nums_to_text(numbers)


    @staticmethod
    def crack(n, e):
        """
        Find private key (d) given public key values (n, e)
        """

        pq = RSA.find_prime_factors(n)
        if pq:
            d = RSA.extended_euclidean(e, (pq[0] - 1) * (pq[1] - 1))
            return (d, pq)
        else:
            logger.error(f"No prime factors found for {n}")
            exit(0)


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
    def find_prime_factors(num):
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
        """
        Converts list of asci char numbers to text.
        """
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


def click_decrypt():
    """
    Decrypt button click function.
    Gets n, e, and cypher text values from gui entries,
    then decrypts and adds resulting plaintext to entry field.
    """
    rsa = RSA(int(n_str.get()), int(e_str.get()))
    plaintext_str.set(rsa.decrypt(cyphertext_str.get()))


def start_gui():
    """
    Starts a tkinter GUI.
    """
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


def get_valid_input(prompt, type_ = None, min = None, max = None):
    """
    Input validation helper function
    """
    if min is not None and max is not None and max < min:
        raise ValueError("Min must be less than or equal to max.")
    while True:
        user_input = input(prompt)
        if type_ is not None:
            try:
                user_input = type_(user_input)
            except ValueError:
                logger.error("Input type must be {0}.".format(type_.__name__))
                continue
        if max is not None and user_input > max:
            logger.error("Input must be less than or equal to {0}.".format(max))
        elif min is not None and user_input < min:
            logger.error("Input must be greater than or equal to {0}.".format(min))
        else:
            return user_input


def get_input():
    """
    Get input from user, return dictionary of input.
    """
    n = get_valid_input("Enter n value: ", type_=int)
    e = get_valid_input("Enter e value: ", type_=int)
    c = get_valid_input("Enter cyphertext (space seperated ints): ", type_=str)

    return {'n':n, 'e':e, 'c':c}


def main():
    init_logger()
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
