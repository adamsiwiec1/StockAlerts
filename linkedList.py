# listList.py
# library for circular doubly linked list


# Node class for circular, doubly linked list with a sentinel
class Node:
    def __init__(self, data):
        self.data = data    # Node Instance Variables
        self.next = None
        self.prev = None

    # Return Node data
    def get_data(self):
        return self.data


class Sentinel_DLL:
    # Create the sentinel node, which is before the first node and after the last node
    def __init__(self):
        self.sentinel = Node(None)  # The sentinel is a null
        self.sentinel.next = self.sentinel
        self.sentinel.prev = self.sentinel

    # Return the first node in the list, if there is one. If empty, return None
    def first_node(self):
        if self.sentinel.next == self.sentinel:
            return None
        else:
            return self.sentinel.next

    # Insert a new node w/ data after node 'x'
    def insert_after(self, x, data):
        y = Node(data)  # New node object
        z = x.next      # y goes between x and z

        # Fix up links in the new node
        y.prev = x
        y.next = z

        # The new node 'y' follows node 'x'
        x.next = y

        # The previous node of the next node is the original node
        z.prev = y

    # Insert a new node at the end of the list
    def append(self, data):
        last_node = self.sentinel.prev
        self.insert_after(last_node, data)

    # Insert a new node at the start of the list.
    def prepend(self, data):
        self.insert_after(self.sentinel, data)

    # Delete node x
    def delete(self, x):
        # Splice out node 'x' by making its next and previous equal each other
        y = x.prev
        z = x.next
        y.next = z
        z.prev = y

    # Find a node containing data and return a reference to it. If no node contains 'data', returns none
    def find(self, data):       # This uses 'linear_search' but in a linked list
        # Trick: Store a copy of the data in the sentinel, so data is always found
        self.sentinel.data = data

        # Find data
        x = self.first_node()
        while x.data != data:
            x = x.next

        # Restore the sentinels data
        self.sentinel.data = None

        # Why did we drop out of the while-loop?
        # This is checking if it didn't find the sentinel by accident

        if x == self.sentinel:
            return None     # data wasn't really in the list
        else:
            return x        # we found it in x, in the list

    # ToString method for a circular, doubly linked list with a sentinel.
    # Returns a Python list
    def __str__(self):
        s = "["

        x = self.sentinel.next
        while x != self.sentinel:   # loop through each node in the list
            if type(x.data) == str:
                s += "'"
            s += str(x.data)        # concatenate this node's data
            if type(x.data) == str:
                s += "'"
            if x.next != self.sentinel:
                s += ", "   # if not the last node, add comma and space
            x = x.next

        s += "]"
        return s

