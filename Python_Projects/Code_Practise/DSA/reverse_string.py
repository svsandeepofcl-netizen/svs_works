name="Sandeep"

def reverse(name):
    reversed_txt=""

    for ch in name:
        reversed_txt=ch+reversed_txt
    
    return reversed_txt

print(reverse(name))