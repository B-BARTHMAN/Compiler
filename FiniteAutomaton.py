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
    
    def closure(self, start: int | set[int]) -> set[int]:

        if isinstance(start, int):
            result = set([start])
        else:
            result = set(start)

        while True:
            n = set(result)
            for i in result:
                for c, x in self.nodes[i].transitions:
                    if c == "":
                        n.add(x)
            if n.issubset(result):
                return result
            result.update(n)
    
    def next_state(self, start: set[int], token: str) -> set[int]:

        result = set()
        
        for i in start:
            for c, x in self.nodes[i].transitions:
                if c == token:
                    result.add(x)
        return self.closure(result)

    def accepts(self, value: set[int]) -> bool:
        for s in value:
            if s in self.end:
                return True
        return False
            



def char_accepter(char: str) -> FiniteAutomaton:
    fa = FiniteAutomaton()
    fa.add_node()
    fa.add_node()
    fa.add_transition(0, 1, char)
    fa.define_start(0)
    fa.define_end(1)

    return fa

def spread_accepter(char1: str, char2: str) -> FiniteAutomaton:
    fa = FiniteAutomaton()
    fa.add_node()
    fa.add_node()
    i = ord(char1)
    while i <= ord(char2):
        fa.add_transition(0, 1, chr(i))
        i += 1
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



def question_accepter(fa0: FiniteAutomaton) -> FiniteAutomaton:
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
    
    return fa



def plus_accepter(fa0: FiniteAutomaton) -> FiniteAutomaton:
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
        fa.add_transition(id, fa.start, "")
    
    return fa



def __fa2dfarec(fa: FiniteAutomaton, alphabet: str, states: dict[int, set[int]], transitions: list[list[int]], accept: list[int], lookat: int) -> None:

    state = states[lookat]

    if fa.accepts(state):
        accept.append(lookat)

    for c in alphabet:

        # calculate next state
        next_state = fa.next_state(state, c)
        # next state already exists
        if next_state in states.values():
            key = list(states.values()).index(next_state)
            assert states[key] == next_state
            transitions[lookat][alphabet.index(c)] = key
            continue

        # add new state to the list
        new_id = len(states)
        states[new_id] = next_state
        transitions.append([-1 for x in alphabet])
        transitions[lookat][alphabet.index(c)] = new_id

        # recursive
        __fa2dfarec(fa, alphabet, states, transitions, accept, new_id)

def __reaches_accept(transitions: list[list[int]], visited: list[int], accepts: list[int], lookat: int) -> bool:
    
    visited.append(lookat)

    if lookat in accepts: return True

    for t in transitions[lookat]:
        if t in visited: continue
        if __reaches_accept(transitions, visited, accepts, t): return True
    
    return False



def fa2dfa(fa: FiniteAutomaton, alphabet: str):

    states: dict[int, set[int]] = {}
    transitions: list[list[int]] = [[-1 for x in alphabet]]
    states[0] = fa.closure(fa.start)
    accept: list[int] = []

    __fa2dfarec(fa, alphabet, states, transitions, accept, 0)
    
    reject: list[int] = []

    for start in range(len(states)):
        if not __reaches_accept(transitions, [], accept, start): reject.append(start)

    return transitions, accept, reject

