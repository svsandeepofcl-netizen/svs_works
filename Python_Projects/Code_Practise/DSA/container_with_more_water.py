# Container with more water storage
nums=[1,8,6,2,5,4,8,3,7]
left=0
right=len(nums)-1
max_area=0
while left < right:
    # print(left, right)
    # print(nums[left], nums[right])
    width=right-left
    Area=width*min(nums[right],nums[left])
    max_area=max(max_area, Area)
    print(max_area)
    if nums[left]<nums[right]:
        left+=1
    else:
        right-=1

print(max_area)