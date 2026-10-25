import os


path=r"D:\Sandeep\Reading_Materials"
destination="D:\\Sandeep\\Reading_Materials\\new"


dir_list = os.listdir(path)
print("Files and directories in '", path, "' :")
# prints all files
# print(dir_list)

for file in dir_list:
    #remove file extension and (1) and (2) which were in files
    actual_name = file.split(' ')[0]
    if not actual_name.endswith('.pdf'):
        #whole path
        old_path = os.path.join(path, file)
        new_path= os.path.join(path, actual_name)
        os.rename(old_path, new_path)