## Control Structures
## Nathan Schluessler
# If statement
def check_number(num):
    if num > 0:
        return 'positive'
    elif num < 0:
        return 'negative'
    else:
        return 'zero'

# For loop
def is_prime(number):
    if number < 2:
        return False
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False
    return True

def get_first_n_primes(n):
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes


print(get_first_n_primes(10))

# While loop
def sum_integers(end_value):
    sum = 0
    while (end_value > 0):
        sum += end_value
        end_value -= 1
    return sum


