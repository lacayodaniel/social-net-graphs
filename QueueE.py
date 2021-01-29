class Queue: # FIFO
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.size() == 0

    def enqueue(self, item):
        # add the item to the end of the array
        self.items.append(item)

    def dequeue(self):
        if self.isEmpty():
            return None
        temp = self.items[0]
        # remove the item from the beginning of the array
        self.items.remove(self.items[0])
        return temp

    def size(self):
        return len(self.items)

    def clear(self):
        self.items.clear()

    def __str__(self):
        return "{}".format(self.items)

    def __contains__(self, item):
        return item in self.items
