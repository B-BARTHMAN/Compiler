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


id_reg = "([a]|[b]|[c]|[d]|[e]|[f]|[g]|[h]|[i]|[j]|[k]|[l]|[m]|[n]|[o]|[p]|[q]|[r]|[s]|[t]|[u]|[v]|[w]|[x]|[y]|[z]|[A]|[B]|[C]|[D]|[E]|[F]|[G]|[H]|[I]|[J]|[K]|[L]|[M]|[N]|[O]|[P]|[Q]|[R]|[S]|[T]|[U]|[V]|[W]|[X]|[Y]|[Z]|[_])(([a]|[b]|[c]|[d]|[e]|[f]|[g]|[h]|[i]|[j]|[k]|[l]|[m]|[n]|[o]|[p]|[q]|[r]|[s]|[t]|[u]|[v]|[w]|[x]|[y]|[z]|[A]|[B]|[C]|[D]|[E]|[F]|[G]|[H]|[I]|[J]|[K]|[L]|[M]|[N]|[O]|[P]|[Q]|[R]|[S]|[T]|[U]|[V]|[W]|[X]|[Y]|[Z]|[_]|[0]|[1]|[2]|[3]|[4]|[5]|[6]|[7]|[8]|[9])*)"
numval = "([0][x](([0]|[1]|[2]|[3]|[4]|[5]|[6]|[7]|[8]|[9]|[a]|[b]|[c]|[d]|[e]|[f]|[A]|[B]|[C]|[D]|[E]|[F]|[_])([0]|[1]|[2]|[3]|[4]|[5]|[6]|[7]|[8]|[9]|[a]|[b]|[c]|[d]|[e]|[f]|[A]|[B]|[C]|[D]|[E]|[F]|[_])*))|(([0]|[1]|[2]|[3]|[4]|[5]|[6]|[7]|[8]|[9]|[_])([0]|[1]|[2]|[3]|[4]|[5]|[6]|[7]|[8]|[9]|[_])*)|([0][b](([0]|[1]|[_])([0]|[1]|[_])*))"
alphabetforthingabove = "0123456789abcdefABCDEFx_"
test = "((([[a]-[z]])|([[A]-[Z]])|[_])+)((([[a]-[z]])|([[A]-[Z]])|([[0]-[9]])|[_])*)"

x = regex2FA(test, "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789")
transitions, accept, reject = FA.fa2dfa(x, "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789")

print("node_count:", len(transitions))
print("accepting nodes:", accept)
print("rejecting nodes:", reject, "\n")
for i, v in enumerate(transitions):
    print("node", i, ":", v)
    for k, j in enumerate("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789"):
        print(j, ":", v[k])
    print("\n")

