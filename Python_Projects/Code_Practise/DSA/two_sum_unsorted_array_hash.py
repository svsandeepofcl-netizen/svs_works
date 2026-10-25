arr=[7,3,5,4,2,8]

seen = {}

target = 9

combo=[]
for i, o in enumerate(arr):
    need = target-o
    if not need in seen:
        seen[o]=i

    else:
        print("seen")
        combo.append((seen[need], i))

print(combo)


    