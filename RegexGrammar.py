import Grammar as G
from typing import Self

class RegexSymbol(G.Terminal):
    symbol: str

    def __init__(self, value: str) -> None:
        super().__init__("[" + value + "]")
        self.symbol = value
    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, RegexSymbol): return False
        return self.symbol == other.symbol



# Base Regex, represent a regex rule
class RegexExpression(G.NonTerminal):
    def __init__(self, value: str = "E") -> None:
        super().__init__(value)



# Concatenation C -> EE
class ConcatExpression(RegexExpression):
    lhs: RegexExpression | None
    rhs: RegexExpression | None

    def __init__(self, lhs: RegexExpression | None = None, rhs: RegexExpression | None = None) -> None:
        super().__init__("C")

        self.lhs = lhs
        self.rhs = rhs

def concat_application(s: G.String) -> ConcatExpression:
    assert len(s.symbols) == 2
    assert isinstance(s[0], RegexExpression)
    assert isinstance(s[1], RegexExpression)

    return ConcatExpression(s[0], s[1])

concat_rule = G.Rule(ConcatExpression(), G.String([RegexExpression(), RegexExpression()]), concat_application)
contact_regex_rule = G.Rule(RegexExpression(), G.String([ConcatExpression()]), lambda x: x[0])



# Augmentation A -> E*        [, A -> E+, A -> E?]
class AugmentExpression(RegexExpression):
    body: RegexExpression | None
    augment: G.Terminal | None

    def __init__(self, body: RegexExpression | None = None, augment: G.Terminal | None = None) -> None:
        super().__init__("A")

        self.body = body
        self.augment = augment

def augment_application(s: G.String) -> AugmentExpression:
    assert len(s.symbols) == 2
    assert isinstance(s[1], G.Terminal)
    assert s[1] == G.Terminal("*")
    assert isinstance(s[0], RegexExpression)

    return AugmentExpression(s[0], s[1])

augment_rule = G.Rule(AugmentExpression(), G.String([RegexExpression(), G.Terminal("*")]), augment_application)
augment_regex_rule = G.Rule(RegexExpression(), G.String([AugmentExpression()]), lambda x: x[0])



# Parantheses P -> (E)
class ParenthesesExpression(RegexExpression):
    body: RegexExpression | None

    def __init__(self, body: RegexExpression | None = None) -> None:
        super().__init__("P")

        self.body = body

def parentheses_application(s: G.String) -> ParenthesesExpression:
    assert len(s.symbols) == 3
    assert isinstance(s[0], G.Terminal)
    assert isinstance(s[2], G.Terminal)
    assert s[0] == G.Terminal("(")
    assert s[2] == G.Terminal(")")
    assert isinstance(s[1], RegexExpression)

    return ParenthesesExpression(s[1])

parentheses_rule = G.Rule(ParenthesesExpression(), G.String([G.Terminal("("), RegexExpression(), G.Terminal(")")]), parentheses_application)
parentheses_regex_rule = G.Rule(RegexExpression(), G.String([ParenthesesExpression()]), lambda x: x[0])



# Choice K -> E|E
class ChoiceExpression(RegexExpression):
    lhs: RegexExpression | None
    rhs: RegexExpression | None

    def __init__(self, lhs: RegexExpression | None = None, rhs: RegexExpression | None = None) -> None:
        super().__init__("K")

        self.lhs = lhs
        self.rhs = rhs

def choice_application(s: G.String) -> ChoiceExpression:
    assert len(s.symbols) == 3
    assert isinstance(s[1], G.Terminal)
    assert s[1] == G.Terminal("|")
    assert isinstance(s[0], RegexExpression)
    assert isinstance(s[2], RegexExpression)

    return ChoiceExpression(s[0], s[2])

choice_application_rule = G.Rule(ChoiceExpression(), G.String([RegexExpression(), G.Terminal("|"), RegexExpression()]), choice_application)
choice_regex_rule = G.Rule(RegexExpression(), G.String([ChoiceExpression()]), lambda x: x[0])