#leetcode 146
class Node:
    def __init__(self, key, value):
        self.key= key
        self.value=value
        self.prev= None
        self.next= None

class LRUCache:
    def __init__(self, capacity):
        self.capacity=capacity
        self.cache = {}

        #Intial head and tail
        self.left=Node(0,0)
        self.right=Node(0,0)

        #Linking Head and Tail
        self.left.next=self.right
        self.right.prev=self.left
        
    def remove(self, node):
        # here we are delinking node so we are getting its previous and
        #  next values so that we can assign previous value as a prev value to next and vice versa
        prev=node.prev
        nxt=node.next

        prev.next=nxt
        nxt.prev=prev

    def insert(self, node):

        prev=self.right.prev
        nxt=self.right

        #Here we are trying to add node at last before tail(self.right)
        prev.next=node
        node.prev=prev
        node.next=nxt
        nxt.prev=node


    def get(self, key):
        if key in self.cache:
            self.remove(self.cache[key])
            self.insert(self.cache[key])        
            return self.cache[key].value
        return -1
    

    def put(self, key, value):
        if key in self.cache:
            self.remove(self.cache[key])
        
        self.cache[key]=Node(key, value)
        self.insert(self.cache[key])

        if len(self.cache)>self.capacity:
            lru= self.left.next
            self.remove(lru)
            del self.cache[lru.key]