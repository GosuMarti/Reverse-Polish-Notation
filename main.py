import matplotlib.pyplot as plt
import re


class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def __hash__(self):
        return hash(id(self))  # Unique hash based on object id

    def __eq__(self, other):
        return self is other  # Nodes are equal only if they are the same object


def infix_to_rpn(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    output = []
    operators = []
    tokens = re.findall(r'\d+(?:\.\d+)?|[+\-*/()]', expression)

    corrected_tokens = []
    for i, token in enumerate(tokens):
        if token == '-' and (i == 0 or tokens[i - 1] in {'+', '-', '*', '/', '('}):
            corrected_tokens.append(token + tokens[i + 1])
        elif i > 0 and tokens[i - 1] == '-' and (i == 1 or tokens[i - 2] in {'+', '-', '*', '/', '('}):
            continue
        else:
            corrected_tokens.append(token)

    tokens = corrected_tokens

    for token in tokens:
        if re.match(r'^-?\d+(?:\.\d+)?$', token):
            output.append(token)
        elif token == '(':
            operators.append(token)
        elif token == ')':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            operators.pop()
        else:
            while operators and operators[-1] != '(' and precedence[operators[-1]] >= precedence[token]:
                output.append(operators.pop())
            operators.append(token)

    while operators:
        output.append(operators.pop())

    return output


def infix_to_pn(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    output = []
    operators = []
    tokens = re.findall(r'\d+(?:\.\d+)?|[+\-*/()]', expression)

    corrected_tokens = []
    for i, token in enumerate(tokens):
        if token == '-' and (i == 0 or tokens[i - 1] in {'+', '-', '*', '/', '('}):
            corrected_tokens.append(token + tokens[i + 1])
        elif i > 0 and tokens[i - 1] == '-' and (i == 1 or tokens[i - 2] in {'+', '-', '*', '/', '('}):
            continue
        else:
            corrected_tokens.append(token)

    tokens = corrected_tokens[::-1]

    for i in range(len(tokens)):
        if tokens[i] == '(':
            tokens[i] = ')'
        elif tokens[i] == ')':
            tokens[i] = '('

    for token in tokens:
        if re.match(r'^-?\d+(?:\.\d+)?$', token):
            output.append(token)
        elif token == '(':
            operators.append(token)
        elif token == ')':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            operators.pop()
        else:
            while operators and operators[-1] != '(' and precedence[operators[-1]] > precedence[token]:
                output.append(operators.pop())
            operators.append(token)

    while operators:
        output.append(operators.pop())

    return output[::-1]


def build_tree(tokens, is_pn=False):
    stack = []
    steps = []

    if is_pn:
        tokens = tokens[::-1]  # Reverse for PN processing

    for token in tokens:
        if token in {'+', '-', '*', '/'}:
            node = TreeNode(token)
            if is_pn:  # Prefix notation (PN)
                node.left = stack.pop()
                node.right = stack.pop()
            else:  # Reverse Polish notation (RPN)
                node.right = stack.pop()
                node.left = stack.pop()
        else:
            node = TreeNode(token)

        stack.append(node)
        steps.append(stack[:])

    return stack[0], steps


def draw_tree(root, ax, pos=None, x=0, y=0, layer=1, spacing=1.5):
    if root is None:
        return {}

    if pos is None:
        pos = {}

    pos[root] = (x, y)

    if root.left:
        pos.update(draw_tree(root.left, ax, pos, x - spacing / layer, y - 1, layer + 1))
        ax.plot([x, x - spacing / layer], [y, y - 1], 'k-')

    if root.right:
        pos.update(draw_tree(root.right, ax, pos, x + spacing / layer, y - 1, layer + 1))
        ax.plot([x, x + spacing / layer], [y, y - 1], 'k-')

    return pos


def visualize_steps(steps, title="Expression Tree"):
    plt.ion()
    fig, ax = plt.subplots(figsize=(6, 5))

    for i, stack in enumerate(steps):
        ax.clear()
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_frame_on(False)

        if stack:
            tree_root = stack[-1]
            pos = draw_tree(tree_root, ax)
            for node, (x, y) in pos.items():
                ax.text(x, y, node.value, fontsize=12, ha='center', va='center',
                        bbox=dict(facecolor='white', edgecolor='black'))

        ax.set_title(f"{title} - Стъпка {i + 1}")
        plt.pause(1)

    plt.ioff()
    plt.show()


# Example usage
print("Въведете уравнение:")
expression = input().strip()
rpn_tokens = infix_to_rpn(expression)
pn_tokens = infix_to_pn(expression)

print("ОПЗ:", rpn_tokens)
print("ППЗ:", pn_tokens)

# Build trees
rpn_root, rpn_steps = build_tree(rpn_tokens)
pn_root, pn_steps = build_tree(pn_tokens, is_pn=True)

# Visualize trees
print("\nВизуализиране на ОПЗ...")
visualize_steps(rpn_steps, title="ОПЗ")

print("\nВизуализиране на ППЗ...")
visualize_steps(pn_steps, title="ППЗ")
