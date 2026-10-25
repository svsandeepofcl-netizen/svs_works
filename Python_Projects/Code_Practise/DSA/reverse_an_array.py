#reverse an array without using slicing
arr = [1, 2, 3, 4, 5]


left=0
right=len(arr)-1

new=[]


while left<right:
    arr[left],arr[right]=arr[right], arr[left]
    left+=1
    right-=1

print(arr)