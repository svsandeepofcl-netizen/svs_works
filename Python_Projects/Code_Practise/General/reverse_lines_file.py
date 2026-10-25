path =r'D:\Sandeep\Python_Projects\Code_Practise\DSA\test_file.txt'

with open(path, "r") as file:
    content = file.read()
    print(content)