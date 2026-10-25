
# #1,1,2, op count 2
# #1,2,3 op count 3
# #1,2
# unique=set()


# def get_count(k):

#     for i in str(k):
#         unique.add(i)

# value= get_count(123)

# print(len(unique))


# k=[1,2,3,4,5,6]

# even=[ i*i for i in range(5) if i%2==0]

# # even = map(

# #     [lambda x:x*x for x in range(5)]
# # )

# # print(even)
# # print(sum(even))
# value = [x*x for x in k]

# even= filter(
# lambda x:x%2==0, value
# )

# print(list(even))

j=[1,2,3]
k =2

combo=[]

left=0
right=len(j)-1

while left<right:
    value=j[right]-j[left]
    print(value)

    if value==k:
        combo.append((j[left],j[right]))
        left+=1
    elif value<k:
        right-=1
    elif value>k:
        left+=1


print(combo)
#BOOK_TABLE
#BOOK
#AUTHOR

# select author, count(author) from BOOK_TABLE group by author having count(author) >10;




