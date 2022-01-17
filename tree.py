class Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.left = None
        self.right = None

    def set(self, key, val):
        if key < self.key:
            if self.left:
                self.left.set(key, val)
            else:
                self.left = Node(key, val)
        elif key == self.key:
            self.val = val
        else:
            if self.right:
                self.right.set(key, val)
            else:
                self.right = Node(key, val)

    def get(self, key):
        if key < self.key:
            if not self.left:
                raise KeyError
            return self.left.get(key)
        elif key == self.key:
            return self.val
        else:
            if not self.right:
                raise KeyError
            return self.right.get(key)

    def walk(self):
        if self.left:
            yield from self.left.walk()
        yield self.key, self.val
        if self.right:
            yield from self.right.walk()


class Tree:
    def __init__(self):
        self.head = None

    def set(self, key, val):
        if self.head:
            self.head.set(key, val)
        else:
            self.head = Node(key, val)

    def get(self, key):
        if not self.head:
            raise KeyError
        return self.head.get(key)

    def walk(self):
        if self.head:
            yield from self.head.walk()
