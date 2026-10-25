
# S - Seperate responsible principal
# we have added two seperates class for each User and Email Address which is independent of each other
# class User:
    
#     def __init__(self, user: str):
#         self.user = user

# class EmailAddress(User):
#     def add_email_address(self, user:User, email:str):
#         print(f"Email address of user {user.user} is {email}")



# user1=User("Sandeep")
# emailObj=EmailAddress("KK")
# emailObj.add_email_address(user1,"hello@gmail.com")

# O - Open Extension/ Closed Modification
# here we have added place value my inheriting EmailAddress class so that anyone using EmailAddress already will not break 

# class User:    
#     def __init__(self, name: str):
#         self.name = name

# class EmailAddress():
#     def add_email_address(self, user:User, email:str):
#         print(f"Email address of user {user.name} is {email}")

# class ModifyDetails(EmailAddress):
#     def add_place(self, user:User, email:str,place:str):
#         print(f"Email address of user {user.name} is {email} and from {place}")

# user1=User("Sandeep")
# emailObj=ModifyDetails()
# emailObj.add_place(user1,"hello@gmail.com", "Jap")

# oldEmailObj=EmailAddress()
# oldEmailObj.add_email_address(user1,"hello@gmail.com")


# L - Liskov Seperation Principal

# When we replace Parent with its Child everything should work fine without any issue


# class Bird:
#     pass
# class FlyingBird(Bird):
#     def fly(self):
#         print("Its a flying Bird")
# class NonFlyingBird(Bird):
#     def eat(self):
#         print("Its a Nonflying Bird")


# penguin=NonFlyingBird()
# penguin.eat()

# parrot=FlyingBird()
# parrot.fly()