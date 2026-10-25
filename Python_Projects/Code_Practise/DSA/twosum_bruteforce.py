arr=[7,3,5,4,2,8]

target=9
combo=[]

for i in arr:
    minus=target-i
    if minus in arr:        
        idx1=arr.index(i)
        idx2=arr.index(minus)
        # We are getting indx value because to avoid duplicates like 0,4 and 4,0 
        if idx1<idx2:
            combo.append((idx1, idx2))

print(combo)
        