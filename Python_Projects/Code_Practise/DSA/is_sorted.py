#checking fi the array is sorted in ascending order or not
arr=[1,2,3,5,4]

for i in range(len(arr)-1):

    if arr[i]>arr[i+1]:
        print(False)
        break

else:
    print(True)

# check sorting in descending order
arr=[31,25,20,17,13]

for i in range(len(arr)-1):

    if arr[i]<arr[i+1]:
        print(False)
        break

else:
    print(True)

