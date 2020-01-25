import heapq
import priority_queue as pq
'''
Example:
fercuencies = { 'Luis'   : (value = { 'frecuency' : 1, 'node' : QueueNode_1, ... "secondary definitions" ... }),
                'Matias' : (value = { 'frecuency' : 1, 'node' : None       , ... "secondary definitions" ... }),
                'Martin' : (value = { 'frecuency' : 2, 'node' : QueueNode_2, ... "secondary definitions" ... }),
                'Daniel' : (value = { 'frecuency' : 3, 'node' : QueueNode_3, ... "secondary definitions" ... })
}
k_most_frequent = (QueueNode_1 <-> QueueNode_2 <-> QueueNode_3)
'''
# Collection that counts the occurrences of each element and keeps track of the most frequent ones.
class CounterCollection(object):

    def __init__(self, k_most_max_amount=0, k_most_fixed_amount=True):

        self.frequencies         = {} # Records the primaries fields and its respectivly frequency.
        self.k_most_frequent     = pq.PriorityQueue() # It keeps track of the most frequent primaries and its frequency.
        self.k_most_max_amount   = k_most_max_amount
        self.k_most_fixed_amount = k_most_fixed_amount


    def put(self, primary, sec_fields=[], secondary_def=[]):

        # Increase frecuency.
        if primary in self.frequencies.keys():
            self.frequencies[primary]['frequency'] += 1

        # Record new item.
        else:
            value = {
                'frequency' : 1,
                'node' : None
            }
            self.frequencies[primary] = value

            for sec, sf in zip(secondary_def, sec_fields):
                self.update_item(primary, sf, sec)
 
        # Update k-most frequent.
        if not (self.k_most_fixed_amount == True and self.k_most_max_amount == 0):

            current_frequency = self.frequencies[primary]['frequency']
            node = self.frequencies[primary]['node']

            # Already in queue.
            if node is not None:
                self.k_most_frequent.fast_increment(node)

            # Queue at max length.
            elif self.k_most_fixed_amount == True and self.k_most_max_amount == len(self.k_most_frequent):

                first_node = self.k_most_frequent.left_pop()
                least_frequency = first_node.key

                # If the new value its bigger push it, otherwise restore queue.
                if least_frequency < current_frequency:
                    new_node = pq.QueueNode(current_frequency, primary)
                    self.k_most_frequent.push(new_node)
                    self.frequencies[primary]['node'] = new_node
                    self.frequencies[first_node.value]['node'] = None
                else:
                    self.k_most_frequent.push(first_node)

            # Not in queue and with availible space.
            else:
                new_node = pq.QueueNode(current_frequency, primary)
                self.k_most_frequent.push(new_node)
                self.frequencies[primary]['node'] = new_node


    # Return the values of the most frequent keys.
    def most_frequent(self, ascending_order=False):

        while(len(self.k_most_frequent) != 0):
            if ascending_order:
                biggest = self.k_most_frequent.left_pop()
            else:
                biggest = self.k_most_frequent.right_pop()

            yield biggest.value

    # Return all keys.
    def get_primaries(self):
          
          for key in self.frequencies.keys():
              yield key

    # Define or update secondary values.
    def update_item(self, primary, sec_name, secondary):

        try:
            key = self.frequencies[primary]
        except KeyError:
             print("Non defined primary")
        
        if sec_name not in ['frequecy', 'node']:
            key = self.frequencies[primary]
            key[sec_name] = secondary
        else:
            raise Exception("Can't modify a reserved field")

    # Return ocurrences of the passed key.
    def frequency_of(self, primary):

        value = self.frequencies[primary]
        return value['frequency']

    # [key] implementation
    def __getitem__(self, primary):

        try:
            key = self.frequencies[primary]
        except KeyError:
             print("Key", key, "doesn't exist")
            
        item = dict(key)
        del item['frequency']
        del item['node']
        
        return item