# Buy at lowest day and sell at highest day in the coming days

nums=[7,6,2,3,6,4]
combo = set()

left=0
profit=0

for right in range(1,len(nums)):
    print(nums[left],nums[right], profit)
    if nums[right]<nums[left]:
        left=right
    else:
        inter_profit=nums[right]-nums[left]
        if inter_profit>profit:
            profit=inter_profit
            combo.clear()
            combo.add((nums[left],nums[right]))

            
print(combo)

