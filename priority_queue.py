# Queue node
class QueueNode(object):
    def __init__(self, key, value=None): 
        self.key   = key 
        self.value = value
        self.next  = None
        self.prev  = None 

# Double linked priority queue
class PriorityQueue(object):

    def __init__(self):
        self.first = None
        self.last  = None
        self.length = 0


    # len() definition
    def __len__(self):
        return self.length


    # Push from a starting node to right
    def push(self, new_node, starting_node=None):

        # Set the first node as the default starting node
        if starting_node is None:
            current_node = self.first
        else:
            current_node = starting_node

        # Case 0 - New node is the first node
        if self.length == 0:
            self.first = new_node
            self.last  = new_node
            self.length += 1
            return new_node

        # Find the corresponding next node for the new node
        while current_node is not None and new_node.key > current_node.key:
            current_node = current_node.next

        # Case 1 - New node is placed at rightmost position
        if current_node is None:
            new_node.prev = self.last
            new_node.next = None
            self.last.next = new_node
            self.last = new_node

        # Case 2 - New node is placed at leftmost position
        elif current_node.prev is None:
            new_node.prev = None
            new_node.next = current_node
            current_node.prev = new_node
            self.first = new_node

        # case 3 - New node is placed somewhere in the middle
        else:
            previous_node = current_node.prev
            previous_node.next = new_node
            new_node.prev = previous_node
            new_node.next = current_node
            current_node.prev = new_node
            
        self.length += 1
        return new_node


    # Pop rightmost node
    def right_pop(self):

        if self.length > 0:
            last_node = self.last
            self.last = last_node.prev
            self.length -= 1

            if self.length == 0:
                self.last  = None
                self.first = None

            return last_node

        else:
            raise Exception("Can't pop nodes from an empty queue")


    # Pop leftmost node
    def left_pop(self):

        if self.length > 0:
            first_node = self.first
            self.first = first_node.next
            if self.first is not None:
                self.first.prev = None
            self.length -= 1

            if self.length == 0:
                self.last  = None
                self.first = None

            return first_node

        else:
            raise Exception("Can't pop nodes from an empty queue")


    # Random access pop
    def random_pop(self, node):

        next_node = node.next
        prev_node = node.prev

        if self.length > 0:

            if prev_node is None:
                self.first = next_node
            else:
                prev_node.next = next_node

            if next_node is None:
                self.last = prev_node
            else:
                next_node.prev = prev_node
            
            self.length -= 1
            if self.length == 0:
                self.last  = None
                self.first = None
            
            return node

        else:
            raise Exception("Can't pop nodes from an empty queue")


    # Add one to the node's key
    def fast_increment(self, node):

        self.random_pop(node)
        node.key += 1
        self.push(node)

        return node


    # Debug method to check internal consistence
    def check_consistence(self):

        counter = 0
        current_node = self.first
        while current_node is not None:
            counter += 1
            current_node = current_node.next

        if counter != self.length:
            raise Exception("Inconsistent queue")