## Control Structures
## Nathan Schluessler
# If statement

# For loop
def print_primes(num_primes):
    for i in range(2, int(num_primes ** 0.5) + 1):
        if num_primes % i != 0:
            print(i)

print(print_primes(5))

# While loop
def sum_integers(end_value):
    sum = 0
    while (end_value > 0):
        sum += end_value
        end_value -= 1
    return sum

print (sum_integers(100))

