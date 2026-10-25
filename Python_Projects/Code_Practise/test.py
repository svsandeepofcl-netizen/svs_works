Input = [12, 35, 1, 10, 34, 1]
largest=float("-inf")
smallest=float("-inf")

for i in Input:
    if i > largest:
        smallest=largest
        largest=i
        print(largest, smallest)
    else:
        pass
        

        
print(largest, smallest)