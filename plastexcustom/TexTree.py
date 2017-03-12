class Tree:
    def __init__(self, name, children, height):
        self.name = name
        self.children = children
        self.width = len(name)
        self.height = height
        if self.children:
            self.maxwidth = sum([child.maxwidth for child in self.children])
        else:
            self.maxwidth = len(name)

    def __repr__(self):
        repr = []
        rows = self.get_tree_rows()
        for r in reversed(rows):
            repr.append(" ".join(r).center(self.maxwidth))
        return "\n".join(repr)

    def get_tree_rows(self, rows=None):
        if not rows:
            rows = [[] for i in range(self.height)]
            starting_point = True
        else:
            starting_point = False
        rows[self.height - 1].append(self.name)
        if self.children:
            for c in self.children:
                Tree.get_tree_rows(c, rows)

        if starting_point:
            return rows


def walk_tree(node):
    if node.hasChildNodes():
        children = [walk_tree(child) for child in node.childNodes]
        height = max((c.height for c in children)) + 1
    else:
        children = None
        height = 1

    return Tree(node.nodeName, children, height)
