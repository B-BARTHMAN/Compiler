import Grammar as G
from typing import Self

# Base Regex, represent a regex rule
class RegexExpression(G.NonTerminal):

    container: G.NonTerminal | None

    def __init__(self, value: str = "E", container: G.NonTerminal | None = None) -> None:
        super().__init__(value)
        self.container = container



# Concatenation C -> EE    E -> C
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
contact_regex_rule = G.Rule(RegexExpression(), G.String([ConcatExpression()]), lambda x: RegexExpression("E", x[0]))



# Augmentation A -> E*    E -> A        [, A -> E+, A -> E?]
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
augment_regex_rule = G.Rule(RegexExpression(), G.String([AugmentExpression()]), lambda x: RegexExpression("E", x[0]))



# Parantheses P -> (E)    E -> P
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
parentheses_regex_rule = G.Rule(RegexExpression(), G.String([ParenthesesExpression()]), lambda x: RegexExpression("E", x[0]))



# Choice K -> E|E    E -> K
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
choice_regex_rule = G.Rule(RegexExpression(), G.String([ChoiceExpression()]), lambda x: RegexExpression("E", x[0]))



# QuestionMark Q -> E?    E -> Q
class QuestionMarkExpression(RegexExpression):
    body: RegexExpression | None
    augment: G.Terminal | None

    def __init__(self, body: RegexExpression | None = None, augment: G.Terminal | None = None) -> None:
        super().__init__("Q")

        self.body = body
        self.augment = augment

def question_application(s: G.String) -> QuestionMarkExpression:
    assert len(s.symbols) == 2
    assert isinstance(s[1], G.Terminal)
    assert s[1] == G.Terminal("?")
    assert isinstance(s[0], RegexExpression)

    return QuestionMarkExpression(s[0], s[1])

question_application_rule = G.Rule(QuestionMarkExpression(), G.String([RegexExpression(), G.Terminal("?")]), question_application)
question_regex_rule = G.Rule(RegexExpression(), G.String([QuestionMarkExpression()]), lambda x: RegexExpression("E", x[0]))



# PlusExpression F -> E?    E -> F
class PlusExpression(RegexExpression):
    body: RegexExpression | None
    augment: G.Terminal | None

    def __init__(self, body: RegexExpression | None = None, augment: G.Terminal | None = None) -> None:
        super().__init__("F")

        self.body = body
        self.augment = augment

def plus_application(s: G.String) -> PlusExpression:
    assert len(s.symbols) == 2
    assert isinstance(s[1], G.Terminal)
    assert s[1] == G.Terminal("+")
    assert isinstance(s[0], RegexExpression)

    return PlusExpression(s[0], s[1])

plus_application_rule = G.Rule(QuestionMarkExpression(), G.String([RegexExpression(), G.Terminal("+")]), plus_application)
plus_regex_rule = G.Rule(RegexExpression(), G.String([PlusExpression()]), lambda x: RegexExpression("E", x[0]))



# Tokenize Z -> [c]    E -> Z
class TokenExpression(RegexExpression):
    token: str | None

    def __init__(self, token: str | None = None) -> None:
        super().__init__("Z")

        self.token = token

def token_application(s: G.String) -> TokenExpression:
    assert len(s.symbols) == 3
    assert isinstance(s[0], G.Terminal)
    assert isinstance(s[1], G.Terminal)
    assert isinstance(s[2], G.Terminal)
    assert s[0] == G.Terminal("[")
    assert s[2] == G.Terminal("]")

    return TokenExpression(s[1].value)

def token_application_rule(tokens: str) -> list[G.Rule]:
    rules = []
    for c in tokens:
        rules.append(G.Rule(TokenExpression(), G.String([G.Terminal("["), G.Terminal(c), G.Terminal("]")]), token_application))
    return rules
token_regex_rule = G.Rule(RegexExpression(), G.String([TokenExpression()]), lambda x: RegexExpression("E", x[0]))



# SpreadExpression O -> [[c]-[c]]    E -> O
class SpreadExpression(RegexExpression):
    token1: str | None
    token2: str | None
    
    def __init__(self, token1: str | None = None, token2: str | None = None) -> None:
        super().__init__("O")
        
        self.token1 = token1
        self.token2 = token2

def spread_application(s: G.String) -> SpreadExpression:
    assert len(s.symbols) == 5
    assert isinstance(s[0], G.Terminal)
    assert isinstance(s[1], TokenExpression)
    assert isinstance(s[2], G.Terminal)
    assert isinstance(s[3], TokenExpression)
    assert isinstance(s[4], G.Terminal)
    assert s[0] == G.Terminal("[")
    assert s[2] == G.Terminal("-")
    assert s[4] == G.Terminal("]")
    assert ord(s[1].token) < ord(s[3].token)
    
    return SpreadExpression(s[1].token, s[3].token)
spread_application_rule = G.Rule(SpreadExpression(), G.String([G.Terminal("["), TokenExpression(), G.Terminal("-"), TokenExpression(), G.Terminal("]")]), spread_application)
spread_regex_rule = G.Rule(RegexExpression(), G.String([SpreadExpression()]), lambda x: RegexExpression("E", x[0]))



# Start S -> E$
starting_rule = G.Rule(G.NonTerminal("S"), G.String([RegexExpression(), G.Terminal("EOL")]), lambda x: RegexExpression("E", x[0]))



def regex_grammar(tokens: str) -> G.Grammar:
    rules: list[G.Rule] = [
        starting_rule,
        token_regex_rule,
        *token_application_rule(tokens),
        spread_application_rule,
        spread_regex_rule,
        choice_regex_rule,
        choice_application_rule,
        parentheses_regex_rule,
        question_application_rule,
        question_regex_rule,
        plus_application_rule,
        plus_regex_rule,
        parentheses_rule,
        augment_rule,
        augment_regex_rule,
        contact_regex_rule,
        concat_rule
    ]
    return G.rules2grammar(rules, G.NonTerminal("S"))

grammar = regex_grammar("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_")

"""
for nt in grammar.nonterminals:
    for t in grammar.first(nt):
        print(nt, t)
"""