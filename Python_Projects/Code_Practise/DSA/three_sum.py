k=[-4,-1,-1,0,1,2]

values=[]

for i in range(len(k)-1):
    left=i+1
    right=len(k)-1
    while left<right:
        total = k[i]+k[left]+k[right]
        print(k[i],k[left],k[right])
        
        if total==0:
            print(k[i],k[left],k[right])
            values.append((k[i],k[left],k[right]))
            left+=1
            right-=1

        elif total<0:
            left+=1
        elif total>0:
            right-=1


print(values)

