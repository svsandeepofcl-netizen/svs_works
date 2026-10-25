data = { "user": { "id": 101, "profile": { "name": "Alice", "skills": ["python", "aws"] } }, "active": True }

final_outpt={}
def call_func(data,final_outpt, parent_key=''):
    # print("Parent Key", parent_key)
  
    for key, value in data.items():
        if isinstance(value, dict):
            if parent_key:
                key = parent_key+'.'+key
            
            call_func(value, final_outpt, parent_key=key)
        
        elif isinstance(value, list):
            
            for index, i  in enumerate(value):
                final_outpt[parent_key+'.'+key+'.'+str(index)]=i
       
        else:
            # print(">>>", key, parent_key)
            if parent_key:
                final_outpt[parent_key+'.'+key]=value
            else:
                final_outpt[key]=value

    return final_outpt


print(call_func(data, final_outpt))