from typing import Self
from typing import Callable
import copy

# Base Symbol used in Grammars
class Symbol:
    value: str
    def __init__(self, value: str) -> None:
        self.value = value
    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, Symbol): return False
        return self.value == other.value
    def __str__(self) -> str:
        return self.value

class Terminal(Symbol):
    def __init__(self, value: str) -> None:
        super().__init__(value)
    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, Terminal): return False
        return self.value == other.value
    def __hash__(self) -> int:
        return hash("T_" + str(self))

class Empty(Terminal):
    def __init__(self) -> None:
        super().__init__("")

class NonTerminal(Symbol):
    def __init__(self, value: str) -> None:
        super().__init__(value)
    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, NonTerminal): return False
        return self.value == other.value
    def __hash__(self) -> int:
        return hash("N_" + str(self))

class String:

    symbols : list[Symbol]

    __iter : int

    def __init__(self, symbols : list[Symbol]) -> None:
        self.symbols = symbols
    
    def __getitem__(self, key:int) -> Symbol:
        if key < 0 or key >= len(self.symbols): return Empty()
        return self.symbols[key]
    
    def patched(self) -> Self:
        return String([copy.deepcopy(x) for x in self.symbols if x != Empty()])

    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, String): return False
        x : String = self.patched()
        y : String = other.patched()
        for i in range(max(len(x.symbols), len(y.symbols))):
            if x[i] != y[i]: return False
        return True
    
    def __str__(self) -> str:
        result: str = ""
        for symbol in self:
            result += str(symbol)
        return result

    def __iter__(self) -> Self:
        x: Self = copy.deepcopy(self)
        x.__iter = 0
        return x

    def __next__(self) -> Symbol:
        if self.__iter >= len(self.symbols): raise StopIteration
        x : Symbol = self[self.__iter]
        self.__iter += 1
        return x

    

# type Rule = tuple[NonTerminal, String]
class Rule:

    lhs: NonTerminal
    rhs: String

    application: Callable[[String],NonTerminal] | None

    def __init__(self, lhs: NonTerminal, rhs: String, application: Callable[[String],NonTerminal] | None = None) -> None:
        self.lhs = lhs
        self.rhs = rhs
        self.application = application



def str2rule(v: str, application: Callable[[String],NonTerminal] | None = None) -> Rule:
    assert isinstance(v, str)
    assert len(v) >= 3
    assert v[0].isupper()
    assert v[1:3] == "->"

    lhs = NonTerminal(v[0])
    rhs: list[Symbol] = []

    if len(v) == 3:
        rhs.append(Empty())
    
    for s in v[3:]:
        if s.isupper():
            rhs.append(NonTerminal(s))
        else:
            rhs.append(Terminal(s))
        
    return Rule(lhs, String(rhs), application)

class Grammar:

    terminals : list[Terminal]
    nonterminals : list[NonTerminal]
    start : NonTerminal
    rules : list[Rule]

    __first : dict[Symbol, list[Terminal]] = {}

    def __init__(self, terminals: list[Terminal], nonterminals: list[NonTerminal], start: NonTerminal, rules : list[Rule]) -> None:
        self.terminals = terminals
        self.nonterminals = nonterminals
        self.start = start
        self.rules = rules

        if not Empty() in self.terminals:
            self.terminals.append(Empty())

        self.__init_first()
    
    def __init_first(self) -> None:
        
        # initalize terminals
        for symbol in self.terminals:
            self.__first[symbol] = [symbol]
        
        # initalize nonterminals
        for symbol in self.nonterminals:
            self.__first[symbol] = []
        
        repeat: bool = True
        while repeat:
            repeat = False
            for rule in self.rules:
                lhs, rhs = rule.lhs, rule.rhs
                counter: int = 0
                for symbol in rhs:

                    result: set[Terminal] = set(self.__first[symbol])

                    if not result.issubset(self.__first[lhs]):
                        self.__first[lhs] = list(set.union(set(self.__first[lhs]), result)) # compute union
                        repeat = True

                    if not Empty() in result:
                        break

                    # if we reach this point the string may derive the empty word
                    if counter < len(rhs.symbols) - 1 and lhs != symbol:
                        self.__first[lhs].remove(Empty())
                    counter += 1

    
    def first(self, string: String | Symbol) -> list[Terminal]:

        if isinstance(string, Symbol):
            return self.__first[string]
        
        elif isinstance(string, String):

            accumulated: list[NonTerminal] = []

            for symbol in string:

                result: list[Terminal] = self.first(symbol)
                accumulated += result

                # symbol can derive empty word, we also need to consider next token
                if Empty() in result:
                    continue

            return list(set(accumulated))

def rules2grammar(rules: list[Rule], start: NonTerminal) -> Grammar:

    terminals: set[Terminal] = set()
    nonterminals: set[NonTerminal] = set()

    for rule in rules:
        lhs, rhs = rule.lhs, rule.rhs
        nonterminals.add(lhs)
        for symbol in rhs:
            if isinstance(symbol, Terminal):
                terminals.add(symbol)
            elif isinstance(symbol, NonTerminal):
                nonterminals.add(symbol)
            else:
                raise ValueError
    
    return Grammar(list(terminals), list(nonterminals), start, rules)

"""
rules : list[Rule] = [
    str2rule("S->R$"),
    str2rule("R->RR"), # concatenation
    str2rule("R->(R)"), 
    str2rule("R->RM"), # modifier
    str2rule("M->+"),
    str2rule("M->?"),
    str2rule("M->*"),
    str2rule("R->[C]"),
    str2rule("R->R|R"),
    str2rule("C->a")
    ]

grammar = rules2grammar(rules, NonTerminal("S"))
print(*grammar.first(NonTerminal("R")))
"""