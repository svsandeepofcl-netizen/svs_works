
#leetcode 443
chars=["a","a","b","b","c","c","c"]

left =0
write=0


while left<len(chars):

    right=left

    while right < len(chars) and chars[left]==chars[right]: # loop until we find new element
        right+=1

    count=right-left 
    chars[write]=chars[left]
    write+=1

    if count>1:
        for i in str(count):
            chars[write]=i
            write+=1

    left = right

print(chars)



