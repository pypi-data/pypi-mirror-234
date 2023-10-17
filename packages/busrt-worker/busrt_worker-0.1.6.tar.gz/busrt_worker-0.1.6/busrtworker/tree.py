class RadixTreeNode(object):
    def __init__(self, path=None, handler=None, methods=None):
        self.path = path
        self.methods = {}
        self.children = []
        self.indices = str()
        self.size = 0

        self.add_methods(methods, handler)

    def __repr__(self):
        return ('<RadixTreeNode path: {}, methods: {}, indices: {}, children: '
                '{}>'.format(self.path, self.methods, self.indices,
                             self.children))

    def add_methods(self, methods, handler):
        if not methods:
            return

        if not isinstance(methods, (list, tuple, set)):
            methods = [methods]

        for method in methods:
            if method in self.methods and self.methods[method] != handler:
                raise KeyError(
                    '{} conflicts with existed handler '
                    '{}'.format(handler, self.methods[method]))

            self.methods[method] = handler

    def bisect(self, target):
        low, high = 0, self.size
        while low < high:
            mid = low + high >> 1
            if self.indices[mid] < target:
                low = mid + 1
            else:
                high = mid
        return low

    def insert_child(self, index, child):
        pos = self.bisect(index)
        self.indices = self.indices[:pos] + index + self.indices[pos:]
        self.children.insert(pos, child)
        self.size += 1

        return child

    def get_child(self, index):
        for i, char in enumerate(self.indices):
            if char == index:
                return self.children[i]


class RadixTree(object):
    def __init__(self):
        self.root = RadixTreeNode()

    def __repr__(self):
        return repr(self.root)

    def insert(self, key, handler, methods):
        i, n, root = 0, len(key), self.root

        def get_position(i):
            return n if i == -1 else i

        while i < n:
            conflict, num = [], (key[i] == ':') + (root.indices == ':')

            if (root.indices == '*' or
                    key[i] == '*' and root.indices or
                    num == 1 or
                    num == 2 and key[i + 1:get_position(
                        key.find('/', i))] != root.get_child(':').path):
                conflict = [key[:i] + p for p in self.traverse(root)]

            if conflict:
                raise Exception('"{}" conflicts with {}'.format(key, conflict))

            child = root.get_child(key[i])

            if child is None:
                pos = get_position(key.find(':', i))
                if pos == n:
                    pos = get_position(key.find('*', i))
                    if pos == n:
                        root.insert_child(
                            key[i], RadixTreeNode(key[i:], handler, methods))
                        return

                    root = root.insert_child(key[i], RadixTreeNode(key[i:pos]))
                    root.insert_child(
                        '*', RadixTreeNode(key[pos + 1:], handler, methods))
                    return

                root = root.insert_child(key[i], RadixTreeNode(key[i:pos]))
                i = get_position(key.find('/', pos))
                root = root.insert_child(':', RadixTreeNode(key[pos + 1:i]))

                if i == n:
                    root.add_methods(methods, handler)
            else:
                root = child
                if key[i] == ':':
                    i += len(root.path) + 1
                    if i == n:
                        root.add_methods(methods, handler)
                else:
                    j, m = 0, len(root.path)
                    while i < n and j < m and key[i] == root.path[j]:
                        i += 1
                        j += 1

                    if j < m:
                        child = RadixTreeNode(root.path[j:])
                        child.methods = root.methods
                        child.children = root.children
                        child.indices = root.indices
                        child.size = root.size

                        root.path = root.path[:j]
                        root.methods = {}
                        root.children = [child]
                        root.indices = child.path[0]
                        root.size = 1

                    if i == n:
                        root.add_methods(methods, handler)

    def get(self, key, method):
        i, n, root, params = 0, len(key), self.root, {}
        while i < n:
            if root.indices == ':':
                root, pos = root.children[0], key.find('/', i)
                if pos == -1:
                    pos = n
                params[root.path], i = key[i:pos], pos
            elif root.indices == '*':
                root = root.children[0]
                params[root.path] = key[i:]
                break
            else:
                root = root.get_child(key[i])
                if root is None:
                    return False, None, {}

                pos = i + len(root.path)
                if key[i:pos] != root.path:
                    return False, None, {}
                i = pos

        return True, root.methods.get(method, None), params

    def traverse(self, root):
        r = []
        for i, char in enumerate(root.indices):
            child = root.children[i]
            path = '{}{}'.format(
                char if char in [':', '*'] else '', child.path)

            if child.methods and child.indices:
                r.append([path])

            r.append([path + p for p in self.traverse(child) or ['']])
        return sum(r, [])
