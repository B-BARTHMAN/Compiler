import RegexGrammar as RG
import Grammar as G

class Item:
    rule: G.Rule
    next_token: int
    look_ahead: set[G.Terminal]

    def __init__(self, rule: G.Rule, next_token: int = 0, look_ahead: set[G.Terminal] = []) -> None:
        self.rule = rule
        self.next_token = next_token
        self.look_ahead = look_ahead
    
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

    def __init__(self, item: Item, grammar: G.Grammar) -> None:
        self.items = set([item])
        self.__grammar = grammar

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node): return False
        return self.items == other.items


class LR1Parser:
    pass