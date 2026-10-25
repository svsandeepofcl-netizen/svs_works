
#leetcode 347
#neetcode 
nums = [1,2,2,3,3,3]
k = 2


counter_data={}
for i in nums:
    counter_data[i]=counter_data.get(i, 0)+1
    
#bucketscreation
#we are creating extra bucket because if len of repeating characters is equal
#to lenght of repeating character we will have an issue
buckets=[[] for i in range(len(nums)+1)] 

for key, value in counter_data.items():
    buckets[value].append(key)

result = []
for i in range(len(buckets)-1, 0, -1):
    print(i)
    for v in buckets[i]:
        if len(result)!=k:
            result.append(v)
            
            
print(result)