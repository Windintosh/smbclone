
level = 0
def indent():
    global level
    level += 1

def unindent():
    global level
    level -= 1

def print_indent():
    for i in range(level):
        print("    ", end='')


class BehaviorTree: #behavior tree를 실행한다는 것은 곧 루트 노드를 실행하는 것
    FAIL, RUNNING, SUCCESS = -1, 0, 1

    def __init__(self, root_node):
        self.root = root_node

    def run(self):
        self.root.run()

    def print(self):
        self.root.print()


class Node:
    def add_child(self, child):
        self.children.append(child)
    def add_children(self, *children): # * : 개수 가변, tuple로 넘겨줌
        for child in children:
            self.children.append(child)


class SelectorNode(Node): #자식 노드를 왼쪽부터 실행, 하나라도 성공하면 성공. 미션을 수행함에 있어 여러개의 대안을 자식노드로 붙여둠.
    def __init__(self, name):
        self.children = []
        self.name = name
        self.prev_running_pos = 0 # 앞선 실행에서, RUNNING으로 리턴한 자식 노드 위치를 저장

    def run(self):
        for pos in range(self.prev_running_pos, len(self.children)):
            result = self.children[pos].run()
            if BehaviorTree.RUNNING == result:
                self.prev_running_pos = pos
                return BehaviorTree.RUNNING
            elif BehaviorTree.SUCCESS == result:
                self.prev_running_pos = 0
                return BehaviorTree.SUCCESS
        self.prev_running_pos = 0
        return BehaviorTree.FAIL

    def print(self):
        print_indent()
        print("SELECTOR NODE: " + self.name)
        indent()
        for child in self.children:
            child.print()
        unindent()

class SequenceNode(Node): # 하위 노드들이 모두 SUCCESS여야 SUCCESS를 리턴. 미션을 수행하기 위해 미션을 여러가지 단위 작업으로 분리하고 각각의 단위 작업이 모두 성공해야 완성
    def __init__(self, name):
        self.children = []
        self.name = name
        self.prev_running_pos = 0

    def run(self):
        for pos in range(self.prev_running_pos, len(self.children)):
            result = self.children[pos].run()
            if BehaviorTree.RUNNING == result:
                self.prev_running_pos = pos
                return BehaviorTree.RUNNING
            elif BehaviorTree.FAIL == result:
                self.prev_running_pos = 0
                return BehaviorTree.FAIL
        self.prev_running_pos = 0
        return BehaviorTree.SUCCESS

    def print(self):
        print_indent()
        print("SEQUENCE NODE: " + self.name)
        indent()
        for child in self.children:
            child.print()
        unindent()


class LeafNode(Node): #함수의 이름과 기능을 함수로서 갖고 있고, 이것을 실행했을 때 노드에 연결된 함수를 호출한다.
    def __init__(self, name, func):
        self.name = name
        self.func = func

    def add_child(self, child):
        print("ERROR: you cannot add child node to leaf node")

    def add_children(self, *children):
        print("ERROR: you cannot add children node to leaf node")

    def run(self):
        return self.func()

    def print(self):
        print_indent()
        print("LEAF NODE: " + self.name)



