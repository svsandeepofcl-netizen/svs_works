# @async()
# def getting_details():
    
#     url="/get"
    
    
#     async_api=aysnc.get(url)
#     await(async_api)
    
#     async.gather(async_api)


# for key,value in dic.items():
#     if isinstance(value, dict):
#         for k,v in value.items():
#             if isinstance()

# Sort different datatypes
# lst = [1, 3, 5, 'red', 'black', 'yellow', 2.5, 1, 1, 'red']

# integers=[]
# floats=[]
# strings=[]


# for i in lst:
#     if isinstance(i, int):
#         integers.append(i)
#     elif isinstance(i, float):
#         floats.append(i)
#     elif isinstance(i, str):
#         strings.append(i)


# print(integers+floats+strings)



# Employee.models.get(Employee.salary.gt(20000))

# Employee.get(Employee.salary.gt(20000))

# print(new_lst)
#*************************************************************************
# Find the values for a specified key
dic = {
    "a": "Hello",
    "b": {
        "d": [
            {
                "a": "World"
            }
        ]
    },
    "c": [
        {
            "a": "EY"
        },
        {
            "b": "Athletica"
        }
    ]
}


new =[]

def get_key(dct, target):
    
    for k,v in dct.items():
        if k == target:
            new.append(v)
        elif isinstance(v,dict):
            get_key(v,target)
        elif isinstance(v, list):
            for i in v:
                get_key(i, target)

get_key(dic,'c')
print(new)

#*************************************************************************

    