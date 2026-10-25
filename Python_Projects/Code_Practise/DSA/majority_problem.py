#We need to find the most repeated value in this

arr = [1, 1, 2, 1, 3, 5, 1]

candidate=-1
count=0

for i in arr:
    if count==0:
        candidate=i
        count+=1
    if i==candidate:
        count+=1
    else:
        count-=1

print(candidate, count)

if arr.count(candidate) > len(arr)//2:
    print(candidate)
else:
    print -1
