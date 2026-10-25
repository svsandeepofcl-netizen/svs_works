# Problem is reverse an integer without converting that to string

num=9865237

rev=0
digit=0

while num%10>0:
    digit=num%10
    rev=rev*10+digit
    num=num//10


print(rev)


