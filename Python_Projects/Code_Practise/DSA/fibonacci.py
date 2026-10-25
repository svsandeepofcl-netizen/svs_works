a=0
b=1

list =[]
while a<10:
    list.append(str(a))
    a,b=b,a+b


# print(list)


for i in list:
    print(i, end=" ")

print(' '.join(list))


print(*list)