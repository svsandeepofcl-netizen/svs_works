# problem is we need to make sure all the non zeros at first and zeros at last
# expected output : [1, 3, 12, 0, 0]
nums = [0, 1, 0, 3, 12]

trans_pos=0

for i in range(len(nums)):
    if nums[i]!=0:
        nums[trans_pos]=nums[i]
        trans_pos+=1

print(nums)

while trans_pos<len(nums):
    nums[trans_pos]=0
    trans_pos+=1

print(nums)