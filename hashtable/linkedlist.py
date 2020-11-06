class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def __str__(self):
        r = ""
        cur = self.head

        while cur is not None:
            r += f'({cur.value})'
            if cur.next is not None:
                r += ' -> '
            cur = cur.next
        return r

    def insert_at_head(self, node):
        node.next = self.head
        self.head = node
