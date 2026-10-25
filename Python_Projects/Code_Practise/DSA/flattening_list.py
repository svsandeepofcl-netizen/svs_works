data=[1,2,3,[4], [5,6,[7,8],9],10]
#data=[1,2,3,[4,5],6]


def func(data):
    output=[]
    for value in data:
        print(value, output)
        if isinstance(value,list):
            output.extend(func(value))
        else:
            output.append(value)
            print(output)
    
    print("Out of loop", output)
    return output

#print(func(data))
k=func(data)
print(k)
            