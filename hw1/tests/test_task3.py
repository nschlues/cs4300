from task3 import check_number, is_prime, get_first_n_primes, sum_integers

def test_if():
    assert check_number(5) == 'positive'
    assert check_number(0) == 'zero'
    assert check_number(-100) == 'negative'


def test_for():
    assert get_first_n_primes(10) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


def test_while():
    assert sum_integers(100) == 5050
