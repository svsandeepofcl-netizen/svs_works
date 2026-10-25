nums=[2,3,1,2,4,3]
target=10
k=[]
sum=0
left=0

for right in range(len(nums)):
    sum+=nums[right]
    # print(sum)
    while sum >=target:
        k.append(right-left+1)
        sum-=nums[left]
        left += 1
print(k)
print(min(k))
   