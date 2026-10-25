arr=[7,3,5,4,2,8]

target=9

arr.sort()
combo=[]

def two_sum(arr, target):

    left = 0
    right = len(arr)-1

    while left < right:
        sum=arr[left]+arr[right]
        if sum == target:
            combo.append((left,right))
            left+=1
        elif sum > target:
            right-=1
        elif sum < target:
            left+=1
        #print(left, right)
        
two_sum(arr,target)
print(combo)
