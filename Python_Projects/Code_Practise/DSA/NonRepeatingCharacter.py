Input="leetcode"
count={}


for i in Input:
    if i in count.keys():
        count[i]+=1
    else:
        count[i]=1

print(count)

for k,v in count.items():
    if v==1:
        print("First Non Repeating", k)
        break