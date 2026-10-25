# problem is to maintain order by removing duplicates
nums=[3, 1, 2, 1, 3, 4]

seen = set() # This is because set uses hash table and its TC is O(1)

output=[]
for i in nums:
    if i not in seen:
        seen.add(i)
        output.append(i)

print(output)
        
