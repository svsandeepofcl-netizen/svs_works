from abc import ABC, abstractmethod


class abs_class(ABC):

   @abstractmethod
   def pay(self, amount):
      pass
   

class CreditCard(abs_class):
   pass




print("Hello running here")