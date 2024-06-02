import numpy as np
import pathlib
import RegexToFA as R2FA

class DFA:
    
    alphabet: str
    transitions: list[list[int]]
    accept: list[int]
    reject: list[int]
    
    def __init__(self, path: str, regex: str | None = None, alphabet: str | None = None) -> None:
        
        path = pathlib.Path(path)
        
        if path.is_file():
            
            with open(path, 'rb') as f:
                self.alphabet = np.load(f).tolist()
                self.transitions = np.load(f).tolist()
                self.accept = np.load(f).tolist()
                self.reject = np.load(f).tolist()
        
        else:
            self.alphabet = alphabet
            x = R2FA.regex2FA(regex, alphabet)
            self.transitions, self.accept, self.reject = R2FA.FA.fa2dfa(x, alphabet)
            
            # save to file
            with open(path, '+wb') as f:
                np.save(f, self.alphabet)
                np.save(f, self.transitions)
                np.save(f, self.accept)
                np.save(f, self.reject)
    
    def run(self, word: str) -> bool:
        
        state: int = 0
        for c in word:
            
            i: int = self.alphabet.find(c)
            
            if i == -1: return False
            state = self.transitions[state][i]
            if state in self.reject: return False
        
        return state in self.accept

identifier = DFA("dfa/identifier_dfa.npy", "(([[a]-[z]]|[[A]-[Z]]|[_])+)(([[a]-[z]]|[[A]-[Z]]|[[0]-[9]]|[_])*)", "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")
integer = DFA("dfa/integer.npy","(([-]|[+])?)((([0]([x]|[X]))((([_]?)([[0]-[9]]|[[a]-[f]]|[[A]-[F]]))+))|(([0]([b]|[B]))((([_]?)([0]|[1]))+))|(([0]([o]|[O]))((([_]?)([[0]-[7]]))+))|(([[1]-[9]]+)(([_]?)([[0]-[9]]))*))", "0123456789abcdefABCDEFxXoO_+-")

