import pytest

from pyrsa import RSA

class TestRSA(object):
    def test_rsa_init(self):
        """
        Test of the RSA constructor
        """
        n = 187
        e = 3
        d = 107
        rsa = RSA(n=n, e=e)

        assert rsa.n == n
        assert rsa.e == e


    def test_decrypt(self):
        """
        Test of decryption function
        Expected: returns string of space seperated decrypted characters
        """
        n = 187
        e = 3
        expected_d = 107
        expected_single = "H"
        expected_multiple = "H E"

        rsa = RSA()
        rsa_vars = RSA(n, e)

        # decrypt with given n and e
        assert rsa.decrypt(183, n, e) == expected_single
        assert rsa.decrypt("183", n, e) == expected_single
        assert rsa.decrypt("183 137", n, e) == expected_multiple
        assert rsa.decrypt([183, 137], n , e) == expected_multiple

        assert rsa.d == expected_d
        assert rsa.n == n
        assert rsa.e == e
        assert rsa.pq == [17, 11]

        # decrypt with n and e given in constructor
        assert rsa_vars.decrypt(183) == expected_single
        assert rsa_vars.decrypt("183") == expected_single
        assert rsa_vars.decrypt("183 137") == expected_multiple
        assert rsa_vars.decrypt([183, 137]) == expected_multiple

        assert rsa_vars.d == expected_d
        assert rsa_vars.n == n
        assert rsa_vars.e == e
        assert rsa_vars.pq == [17, 11]


    def test_euclidean(self):
        """
        Test of extended euclidean function
        Expected: returns d value (mod inverse)
        """
        rsa = RSA()

        e = 3
        pq = 160
        expected = 107

        assert RSA.extended_euclidean(e, pq) == expected


    def test_find_prime_factors(self):
        """
        Test of prime factors fucntion
        Expected: returns two prime factors or None if given number isn't prime
        """
        expected = [23, 5]
        num = expected[0] * expected[1]

        assert RSA.find_prime_factor(num) == expected
        assert RSA.find_prime_factor(200) == None


    def test_modular_exponentiation(self):
        """
        Test of extended euclidean function
        Expected: returns modular exponentiation of number, exponent, and modulus
        """
        num = 7
        exp = 256
        mod = 13
        expected = 9

        assert RSA.modular_exponentiation(num, exp, mod) == expected


    def test_convert_nums_to_text(self):
        """
        Test of convert numbers to text function.
        Exepected: returns string of space seperated characters
        """
        numbers = [116, 69, 115, 84]
        expected = "t E s T"

        assert RSA.convert_nums_to_text(numbers) == expected


    def test_is_primt(self):
        """
        Test of is prime function.
        Exepected: returns true if given number is prime, false otherwise
        """
        num_result = {359:True, 271:True, 300:False, 409:True, 4409:True, 505:False}

        for num, result in num_result.items():
            assert RSA.is_prime(num) == result
