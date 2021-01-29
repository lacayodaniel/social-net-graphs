class Stack:
    def __init__(self):
        self.data = []

    def insert(self, obj):
        self.data.append(obj)

    def peek(self):
        return self.data[-1]

    def pop(self):
        obj = self.peek()
        self.data.remove(obj)
        return obj

    def clear(self):
        self.data.clear()

    def size(self):
        return len(self.data)

    def isEmpty(self):
        return self.size() == 0

    def __str__(self):
        return "{}".format(self.data)

    def __contains__(self, item):
        return item in self.data