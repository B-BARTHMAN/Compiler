import RegexParser as RP
import FiniteAutomaton as FA
import RegexGrammar as G

def __regex2FArec(e: G.RegexExpression) -> FA.FiniteAutomaton:
    if isinstance(e, G.ConcatExpression):
        return FA.concat_accepter(__regex2FArec(e.lhs), __regex2FArec(e.rhs))
    elif isinstance(e, G.ChoiceExpression):
        return FA.choice_accepter(__regex2FArec(e.lhs), __regex2FArec(e.rhs))
    elif isinstance(e, G.AugmentExpression):
        return FA.augment_accepter(__regex2FArec(e.body))
    elif isinstance(e, G.QuestionMarkExpression):
        return FA.question_accepter(__regex2FArec(e.body))
    elif isinstance(e, G.PlusExpression):
        return FA.plus_accepter(__regex2FArec(e.body))
    elif isinstance(e, G.ParenthesesExpression):
        return __regex2FArec(e.body)
    elif isinstance(e, G.TokenExpression):
        return FA.char_accepter(e.token)
    elif isinstance(e, G.SpreadExpression):
        return FA.spread_accepter(e.token1, e.token2)
    elif isinstance(e, G.RegexExpression):
        return __regex2FArec(e.container)

def regex2FA(value: str, tokens: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_") -> FA.FiniteAutomaton:
    parsed: G.RegexExpression = RP.regex_parse(value, tokens)
    return __regex2FArec(parsed)


