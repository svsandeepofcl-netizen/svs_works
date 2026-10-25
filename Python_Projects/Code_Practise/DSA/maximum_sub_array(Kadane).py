nums= [2, 3, -8, 7, -1, 2, 3]


max_sum=nums[0]
curr_sum=0


for i in nums:
    if curr_sum<0:
        curr_sum=0 # if the sum is negative we are restting the value check neet code youtube video for this
    
    curr_sum+=i
    max_sum=max(max_sum,curr_sum)

print(max_sum)