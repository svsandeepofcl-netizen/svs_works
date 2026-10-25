nums=[2,1,5,1,3,2]
k=3

total_sum=0
max_sum=0
left=0 
right=k
window=[]

while right<=len(nums):
    window=nums[left:right]
    print(window)
    total_sum=sum(window)

    if total_sum>max_sum:
        max_sum = total_sum

    left+=1
    right+=1


print(max_sum)