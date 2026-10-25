# def convert_to_roman(num):

#     values = {
#         "M": 1000,
#         "CM": 900,
#         "D": 500,
#         "CD": 400,
#         "C": 100,
#         "XC": 90,
#         "L": 50,
#         "XL": 40,
#         "X": 10,
#         "IX": 9,
#         "V": 5,
#         "IV": 4,
#         "I": 1
#     }

#     roman_values = {
#     "I": 1,
#     "V": 5,
#     "X": 10,
#     "L": 50,
#     "C": 100,
#     "D": 500,
#     "M": 1000
# }
#     res=""

#     for key, value in values.items():
#         while num >=value:
#             res+=key
#             num-=value
#     # print(res)

#     # res = ''.join(sorted(res, key= lambda x: values[x]))

  
#     # res = ''.join(sorted(res, key= lambda x: roman_values[x]))
#     print(''.join(sorted(res))) # if asked to sort by alphabets

#     return res


def rearranage(n, arr):

    values = {
        "M": 1000,
        "CM": 900,
        "D": 500,
        "CD": 400,
        "C": 100,
        "XC": 90,
        "L": 50,
        "XL": 40,
        "X": 10,
        "IX": 9,
        "V": 5,
        "IV": 4,
        "I": 1
    }
    print(n ,arr)


rearranage(7, [1,2,3,21,20])



