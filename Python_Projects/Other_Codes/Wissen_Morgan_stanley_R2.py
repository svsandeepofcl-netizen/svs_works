users={'Sandeep':'amazon', 'SV':'flipkart','SV':'amazon','Ravi':'Ola','Sandeep':'flipkart'}


count={}

users_data=set()

def get_users(user):
    users_data.add(user)
    if user in count:
    
        count[user]+=1
    else:
        count[user]=1


get_users('Sandeep')
get_users('Sandeep')
get_users('Ravi')
get_users('Ravi1')
get_users('Ravi2')
get_users('Ravi4')
get_users('Ravi11')
get_users('Ravi')
print(count)



# for k,v in count.items():

# print(users_data)

for user1 in users_data:
    if count[user1]>=2:
        print(user1)

# /get/topusers
# /customer/toplist/allusers
# /customer/toplist/allusers

    



