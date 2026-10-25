#longest sequence

nums=[100,4,1,2,200,3,5,4]
seen=set(nums)
longest = 0

for num in nums:

    if num-1 not in nums:
        length=1
        
        while num+length in nums:
            length+=1
            
    max_length=max(max_length, length)

print(max_length)