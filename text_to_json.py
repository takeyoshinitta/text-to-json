import json

class Node:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.frequency = 1

    def add_child(self, node):
        if node not in self.children:
            self.children.append(node)

    def increment_frequency(self):
        self.frequency += 1

    def __repr__(self):
        return f"{self.name} ({self.frequency})"


def convert_node_to_dict(node):
    node_dict = {"name": node.name, "size": node.frequency}
    if node.children:
        children = []
        for child in node.children:
            child_dict = convert_node_to_dict(child)
            children.append(child_dict)
        node_dict["children"] = children
    return node_dict


def build_node_tree(file_path):
    node_dict = {}
    with open(file_path) as f:
        lines = f.readlines()
        for i in range(len(lines) - 1):
            parent_word = lines[i].strip()
            child_word = lines[i+1].strip()

            parent_node = node_dict.get(parent_word, None)
            if not parent_node:
                parent_node = Node(parent_word)
                node_dict[parent_word] = parent_node
            else:
                parent_node.increment_frequency()

            child_node = node_dict.get(child_word, None)
            if not child_node:
                child_node = Node(child_word)
                node_dict[child_word] = child_node
            else:
                child_node.increment_frequency()

            parent_node.add_child(child_node)

    root_node = node_dict[lines[0].strip()]
    return root_node

def convert_node_to_dict_iter(node):
    node_stack = [(node, None)]
    result = {"name": node.name, "size": node.frequency, "children": []}

    while node_stack:
        curr_node, parent_dict = node_stack.pop()
        curr_dict = {"name": curr_node.name, "size": curr_node.frequency, "children": []}
        if parent_dict is None:
            parent_dict = result
        parent_dict["children"].append(curr_dict)

        for child_node in curr_node.children:
            child_dict = {"name": child_node.name, "size": child_node.frequency, "children": []}
            curr_dict["children"].append(child_dict)
            node_stack.append((child_node, child_dict))

    return result

root_node = build_node_tree("input.txt")
json_dict = convert_node_to_dict_iter(root_node)
json_str = json.dumps(json_dict, indent=2)
print(json_str)

