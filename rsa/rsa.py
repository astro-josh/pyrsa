from math import sqrt

class RSA():

    @staticmethod
    def decrypt(c, n, e):
        pq = RSA.find_prime_factor(n)
        print(f"pq = {pq}")
        d = RSA.extended_euclidean(e, (pq[0] - 1) * (pq[1] - 1))
        print(f"d = {d}")
        m = RSA.modular_exponentiation(c, d, n)
        print(m)
        return RSA.num_to_text(m)

    @staticmethod
    def extended_euclidean(e, pq):
        print(f"pq in ee = {pq}")
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
            print("quotient = ", quotient)
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
        result = 1

        for x in range(exp):
            result = ((result * num) % mod)

        return result

    @staticmethod
    def num_to_text(num):
        """
        Converts numbers back to letters by reversing the encryption a * 26^2 + b * 26 + c
        """
        a = int(num % 26)
        temp = (num - a) // 26
        b = int(temp % 26)
        c = int((temp - b) // 26)

        # +97 for 0 index
        return str(chr(c + 97) + chr(b + 97) + chr(a + 97))

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


rsa = RSA()
print(rsa.decrypt(1394, 3127, 3))
