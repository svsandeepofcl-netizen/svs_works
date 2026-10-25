

# def convert_to_integer(s):

#     mapped_values= {
#         'I':1,
#         'V':5,
#         'X':10,
#         'L':50,
#         'C':100,
#         'D':500,
#         'M':1000,
#     }

#     total=0
#     # for i in range(len(s)):
#     i=0
#     while i<len(s):
#         print(i)

#         if i+1<len(s) and mapped_values[s[i]]<mapped_values[s[i+1]]:
#             total-=mapped_values[s[i]]
#         else:
#             total+=mapped_values[s[i]]
#         i+=1
    
#     return total


# print(convert_to_integer("XLVIII"))


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
    
    roman_pairs=[]
    
    for num in arr:
        res=""
        inter_Value=num
        for key, value in values.items():
            while num >=value:
                res+=key
                num-=value
        
        roman_pairs.append((res, inter_Value))
                           

    roman_pairs.sort()
    print(roman_pairs)        

    for k, v in roman_pairs:
        print(v)
        5

def main():
    n=int(input())
    S=input().split()
    arr=[]
    for i in range(n):
        arr.append(int(S[i]))

    rearranage(7, arr)

main()