import random

length_required=int(input("Enter how many length of OTP is need:"))

max_limit=10**length_required
min_limit=10**(length_required-1)


random_generation=random.randint(min_limit,max_limit)
print(f"Random number that is generated {random_generation}")
