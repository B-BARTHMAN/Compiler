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
    elif isinstance(e, G.ParenthesesExpression):
        return __regex2FArec(e.body)
    elif isinstance(e, G.TokenExpression):
        return FA.char_accepter(e.token)
    elif isinstance(e, G.RegexExpression):
        return __regex2FArec(e.container)

def regex2FA(value: str, tokens: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_") -> FA.FiniteAutomaton:
    parsed: G.RegexExpression = RP.regex_parse(value, tokens)
    return __regex2FArec(parsed)


id_reg = "([a]|[b]|[c]|[d]|[e]|[f]|[g]|[h]|[i]|[j]|[k]|[l]|[m]|[n]|[o]|[p]|[q]|[r]|[s]|[t]|[u]|[v]|[w]|[x]|[y]|[z]|[A]|[B]|[C]|[D]|[E]|[F]|[G]|[H]|[I]|[J]|[K]|[L]|[M]|[N]|[O]|[P]|[Q]|[R]|[S]|[T]|[U]|[V]|[W]|[X]|[Y]|[Z]|[_])(([a]|[b]|[c]|[d]|[e]|[f]|[g]|[h]|[i]|[j]|[k]|[l]|[m]|[n]|[o]|[p]|[q]|[r]|[s]|[t]|[u]|[v]|[w]|[x]|[y]|[z]|[A]|[B]|[C]|[D]|[E]|[F]|[G]|[H]|[I]|[J]|[K]|[L]|[M]|[N]|[O]|[P]|[Q]|[R]|[S]|[T]|[U]|[V]|[W]|[X]|[Y]|[Z]|[_]|[0]|[1]|[2]|[3]|[4]|[5]|[6]|[7]|[8]|[9])*)"
id_regs = "([a]|[b])(([a]|[b]|[0]|[1])*)"

x = regex2FA(id_regs, "ab01")
print("DONE")