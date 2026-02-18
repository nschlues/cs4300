## Functions and Duck Typeing
## Nathan Schluessler
def calculate_discount(price, discount):
    return (price - (price * (discount / 100)))

print (calculate_discount(100, 10))
print(calculate_discount(10.5, 1))
print(calculate_discount(100, 2.5))
