Input = [12, 35, 1, 10, 34,33, 1]
largest=float("-inf")
second=float("-inf")

for i in Input:
    if i > largest:
        second=largest
        largest=i
        
    elif second<i<largest:
        second=i

print(largest, second)
