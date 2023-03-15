class Node:

    def __init__(self, data):
        self.data = data
        self.next = self
        self.prev = self


class OrderedList:

    def __init__(self):
        self.dummy = Node(None)

    def is_empty(self):
        return self.dummy.next is self.dummy

    def add(self, item):
        n = Node(item)
        c = self.dummy
        if self.is_empty():
            self.dummy.next = n
            n.prev = self.dummy
            n.next = self.dummy
            self.dummy.prev = n
            return True
        elif n.data < self.dummy.next.data:
            temp = self.dummy.next
            self.dummy.next = n
            n.prev = self.dummy
            n.next = temp
            temp.prev = n
            return True
        else:
            c = c.next
            while c.next is not self.dummy:
                if c.data < n.data < c.next.data:
                    temp = c.next
                    c.next = n
                    n.prev = c
                    n.next = temp
                    temp.prev = n
                    return True
                c = c.next
            if c.data is not None and c.data < n.data and c.next == self.dummy:
                c.next = n
                n.prev = c
                n.next = self.dummy
                self.dummy.prev = n
                return True
            else:
                return False

    def remove(self, item):
        c = self.dummy.next
        while c.next is not self.dummy:
            if c.data == item:
                c.prev.next = c.next
                c.next.prev = c.prev
                return True
            c = c.next
        if c.next is self.dummy and c.data == item:
            c.prev.next = self.dummy
            self.dummy.prev = c.prev
            return True
        else:
            return False

    def index(self, item):
        idx = 0
        c = self.dummy.next
        while c.data is not None:
            if c.data == item:
                return idx
            idx += 1
            c = c.next
        return None

    def pop(self, index):
        if index < 0 or index >= self.size():
            raise IndexError
        else:
            c = self.dummy.next
            for i in range(index):
                c = c.next
            c.prev.next = c.next
            c.next.prev = c.prev
            return c.data

    def search(self, item):
        return self.search_helper(item, self.dummy)

    def search_helper(self, item, c):
        if (not c.data == item) and c.next == self.dummy:
            return False
        elif c.data == item:
            return True
        else:
            return self.search_helper(item, c.next)

    def python_list(self):
        c = self.dummy.next
        lst = []
        while c.data is not None:
            lst.append(c.data)
            c = c.next
        return lst

    def python_list_helper(self, lst):
        if len(lst) == 0:
            return []
        else:
            return [lst[-1]] + self.python_list_helper(lst[0:len(lst)-1])

    def python_list_reversed(self):
        return self.python_list_helper(self.python_list())

    def size(self):
        return self.size_helper(self.dummy.next)

    def size_helper(self, n):
        if n == self.dummy:
            return 0
        return 1 + self.size_helper(n.next)
