nums=[2,1,5,1,3,2]
k=3

total_sum=0
max_sum=0
left=0 
# right=k
# window=[]

for right in range(len(nums)):
    total_sum+=nums[right]
    if right >=k-1:
        max_sum=max(max_sum, total_sum)
        total_sum-=nums[left]
        left+=1

print(max_sum)