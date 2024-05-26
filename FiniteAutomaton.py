from typing import Self

class Node:

    id: int
    transitions: list[tuple[str, int]]

    def __init__(self, id: int, transitions: list[tuple[str, int]] = []) -> None:
        self.id = id
        self.transitions = []# transitions

class FiniteAutomaton:

    nodes: list[Node] = []
    start: int | None = None
    end: list[int] = []

    is_dfa: bool = False

    def __init__(self) -> None:
        self.nodes = []
        self.start = None
        self.end = []
        self.is_dfa = False

    def add_node(self) -> None:
        x = len(self.nodes)
        self.nodes.append(Node(x))
    def add_transition(self, source: int, target: int, char: str) -> None:
        self.nodes[source].transitions.append((char, target))
    def define_start(self, id: int) -> None:
        self.start = id
    def define_end(self, id: int) -> None:
        self.end.append(id)
    
    def run(self, value: str) -> bool:
        if not self.is_dfa: raise Exception

        current: int = self.start
        for c in value:
            # no such transition
            if not c in [x[0] for x in self.nodes[current].transitions]: return False
            for t, id in self.nodes[current].transitions:
                if t == c:
                    current = id
                    break
        return current in self.end



def char_accepter(char: str) -> FiniteAutomaton:
    fa = FiniteAutomaton()
    fa.add_node()
    fa.add_node()
    fa.add_transition(0, 1, char)
    fa.define_start(0)
    fa.define_end(1)

    return fa

def concat_accepter(fa0: FiniteAutomaton, fa1: FiniteAutomaton) -> FiniteAutomaton:
    # create new empty fa
    fa = FiniteAutomaton()

    # add all nodes to fa
    for i in range(len(fa0.nodes) + len(fa1.nodes)):
        fa.add_node()
    
    # add all old transitions to fa
    for n in fa0.nodes:
        for c, id in n.transitions:
            fa.add_transition(n.id, id, c)
    for n in fa1.nodes:
        for c, id in n.transitions:
            fa.add_transition(n.id + len(fa0.nodes), id + len(fa0.nodes), c)
    
    # define the same start
    fa.define_start(fa0.start)

    # add epsilon transition to next start state
    for id in fa0.end:
        fa.add_transition(id, fa1.start + len(fa0.nodes), "")
    
    # define ends
    for id in fa1.end:
        fa.define_end(len(fa0.nodes) + id)
    
    return fa



def choice_accepter(fa0: FiniteAutomaton, fa1: FiniteAutomaton) -> FiniteAutomaton:
    # create new empty fa
    fa = FiniteAutomaton()

    # add all nodes to fa
    for i in range(len(fa0.nodes) + len(fa1.nodes)):
        fa.add_node()
    
    # add all old transitions to fa
    for n in fa0.nodes:
        for c, id in n.transitions:
            fa.add_transition(n.id, id, c)
    for n in fa1.nodes:
        for c, id in n.transitions:
            fa.add_transition(n.id + len(fa0.nodes), id + len(fa0.nodes), c)
    
    # define new start and add epsilon transitions
    fa.add_node()
    fa.define_start(len(fa0.nodes) + len(fa1.nodes))
    fa.add_transition(len(fa0.nodes) + len(fa1.nodes), fa0.start, "")
    fa.add_transition(len(fa0.nodes) + len(fa1.nodes), fa1.start + len(fa0.nodes), "")

    #define ends
    for id in fa0.end:
        fa.define_end(id)
    for id in fa1.end:
        fa.define_end(id + len(fa0.nodes))
    
    return fa



def augment_accepter(fa0: FiniteAutomaton) -> FiniteAutomaton:
    # create new empty fa
    fa = FiniteAutomaton()

    # add all nodes to fa
    for i in range(len(fa0.nodes)):
        fa.add_node()
    
    # add all old transitions to fa
    for n in fa0.nodes:
        for c, id in n.transitions:
            fa.add_transition(n.id, id, c)
    
    # define the same start
    fa.define_start(fa0.start)

    # add epsilon transitions from start to end nodes
    for id in fa0.end:
        fa.define_end(id)
        fa.add_transition(fa.start, id, "")
        fa.add_transition(id, fa.start, "")
    
    return fa

# useless:
"""
def make_nfa(fa0: FiniteAutomaton) -> FiniteAutomaton:
    # create new empty fa
    fa = FiniteAutomaton()

    # add all nodes to fa
    for i in range(len(fa0.nodes)):
        fa.add_node()
    
    # add all old transitions to fa
    for n in fa0.nodes:
        for c, id in n.transitions:
            fa.add_transition(n.id, id, c)
    
    # define the same start
    fa.define_start(fa0.start)

    # add the same ends
    for id in fa0.end:
        fa.define_end(id)
    
    repeat = True
    while repeat:
        repeat = False

        for n in fa.nodes:

            new_transitions: list[tuple[str, int]] = []
            for c, id in n.transitions:

                # skip non epsilon transitions
                if c != "":
                    new_transitions.append((c, id))
                    continue

                repeat = True

                for x, id2 in fa.nodes[id].transitions:
                    if (not (x, id2) in new_transitions) and (id != id2):
                        new_transitions.append((x, id2))
            
            n.transitions = new_transitions
    
    return fa
"""