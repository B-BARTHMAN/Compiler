import RegexGrammar as RG
import Grammar as G
import copy

class Item:
    rule: G.Rule
    next_token: int
    look_ahead: set[G.Terminal]

    def __init__(self, rule: G.Rule, next_token: int = 0, look_ahead: set[G.Terminal] = []) -> None:
        self.rule = rule
        self.next_token = next_token
        self.look_ahead = look_ahead
    

    def is_final(self) -> bool:
        return self.rule.rhs[self.next_token] == G.Empty()
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Item): return False
        if self.rule != other.rule: return False
        if self.next_token != other.next_token: return False
        if self.look_ahead != other.look_ahead: return False
        return True
    
    def __str__(self) -> str:
        return str(self.rule.lhs) + "->" + str(self.rule.rhs)[:self.next_token] + "." + str(self.rule.rhs)[self.next_token:]

    def __hash__(self) -> int:
        s: int = hash(str(self))
        for t in self.look_ahead:
            s ^= hash(t)
        return s



class Node:
    items: set[Item]
    __grammar: G.Grammar

    def __init__(self, item: Item | set[Item], grammar: G.Grammar) -> None:
        if isinstance(item, Item):
            self.items = set([item])
        elif isinstance(item, set):
            self.items = item
        self.__grammar = grammar

        self.complete()
    
    def complete(self) -> None:
        while True:
            new_items: set[Item] = set()
            for item in self.items:

                C = item.rule.rhs[item.next_token]
                d = item.rule.rhs[item.next_token + 1]

                if isinstance(C, G.NonTerminal):
                    # compute lookahead set
                    look_ahead: set[G.Terminal] = set(self.__grammar.first(d))
                    # if d can derive empty or is empty, also include this items lookahead
                    if G.Empty() in look_ahead or d == G.Empty():
                        look_ahead.update(item.look_ahead)
                    
                    # add new item to node
                    for rule in self.__grammar.rules:
                        if rule.lhs == C:
                            new_items.add(Item(rule, 0, look_ahead))

            # break condition
            if new_items.issubset(self.items):
                self.items.update(new_items)
                break
            self.items.update(new_items)
    
    def next_symbol(self) -> set[G.Symbol]:
        symbols: set[G.Symbol] = set()
        for item in self.items:
            C: G.Symbol = item.rule.rhs[item.next_token]

            # this is a final item
            if C == G.Empty():
                continue
            symbols.add(C)
        return symbols
    
    def transition_items(self, symbol: G.Symbol) -> set[Item]:
        items: set[Item] = set()
        for item in self.items:
            if item.rule.rhs[item.next_token] == symbol:
                new_item: Item = copy.deepcopy(item)
                new_item.next_token += 1
                items.add(new_item)
        return items

                

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node): return False
        return self.items == other.items

class RegexParseException(Exception):
    pass

def regex_parse(s: str):

    starting_node: Node = Node(Item(RG.starting_rule), RG.grammar)

    stack: G.String = G.String([])
    consume: G.String = G.String([G.Terminal(x) for x in s] + [G.Terminal("EOL")])

    while True:

        current_node: Node = starting_node
        
        # setup phase
        for symbol in stack.symbols:
            if not symbol in current_node.next_symbol():
                raise RegexParseException
            new_items = current_node.transition_items(symbol)
            current_node = Node(new_items, RG.grammar)
        
        # shift
        while True:
            symbol = consume[0]
            if not symbol in current_node.next_symbol():
                # reduce after this
                break
            new_items = current_node.transition_items(symbol)
            current_node = Node(new_items, RG.grammar)
            stack.symbols.append(symbol)
            consume = G.String(consume.symbols[1:])
        
        # reduce
        reduced = False
        for item in current_node.items:

            # check if this is a final item
            if not item.is_final():
                continue

            # check if there are enough symbols on the stack
            rule_length: int = len(item.rule.rhs.symbols)
            if len(stack.symbols) < rule_length:
                continue

            # check if end of stack matches rule
            end_of_stack = G.String(stack.symbols[-rule_length:])
            if end_of_stack == item.rule.rhs:
                reduced = True
                new_symbol = item.rule.application(end_of_stack)
                stack = G.String(stack.symbols[:-rule_length] + [new_symbol])
                break
        
        if not reduced:
            raise RegexParseException


regex_parse("([a]|[b]|[c])*")


