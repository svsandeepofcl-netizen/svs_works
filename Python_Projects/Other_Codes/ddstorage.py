#You are tasked with designing and implementing a production-ready, thread-safe Least Recently Used (LRU) Cache library intended for use in high-throughput backend systems.

#The cache stores key-value pairs and automatically evicts the least recently used entries when memory capacity is reached.



"""
Design LRU Cache
concureency
"""

from threading import Lock

class Node:
    def __init__(self, key, value):
        self.key = key
        self.val = value
        self.next = None
        self.prev = None


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        head = Node(-1,-1)
        tail = Node(-1,-1)
        head.next = tail
        tail.prev = head

        self.cache = {}
        self.lock = Lock()


    def _add(self, node):
        head_next = self.head.next
        node.next = head_next
        head_next.prev = node
        node.prev = self.head


    def _delete(self, node):
        next_node = node.next
        prev_node = node.prev
        prev_node.next = next_node
        next_node.prev = prev_node


    def get(self, key):
        with self.lock:
            if key in self.cache:
                # move that node to front
                # return the value

                node = self.cache[key]
                self._delete(node)
                self._add(node)

                return self.cache[key]

            return -1

    def post(self, key, value):
        with self.lock:
            if key in self.cache:
            
                self._delete(self.cache[key])
                # self._add(new_node)

            new_node = Node(key,value)
            self._add(new_node)
            self.cache[key] = new_node

            if self.capacity > len(self.cache):
                self._delete(self.tail.prev)
                del self.cache[key]