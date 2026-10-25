class Robot:
    def __new__(cls,name):
        print("Class getting declared")
        # Creation of instance
        instance=super().__new__(cls)
        return instance
    def __init__(self, name):
        print(f"Initialization started for object {name}")
        # self.name=name


robj=Robot("Sandeep")

# print(r)
