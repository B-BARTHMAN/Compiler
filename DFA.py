import numpy as np
import pathlib
import RegexToFA as R2FA

class DFA:
    
    alphabet: str
    transitions: list[list[int]]
    accept: list[int]
    reject: list[int]
    
    def __init__(self, path: str, regex: str | None = None, alphabet: str | None = None) -> None:
        
        if pathlib.Path(path).is_file:
            
            with open(path, 'rb') as f:
                self.alphabet = np.load(f)
                self.transitions = np.load(f)
                self.accept = np.load(f)
                self.reject = np.load(f)
        
        else:
            self.alphabet = alphabet
            x = R2FA.regex2FA(regex, alphabet)
            self.transitions, self.accept, self.reject = R2FA.FA.fa2dfa(x, alphabet)
            
            # save to file
            with open(path, 'wb') as f:
                np.save(f, self.alphabet)
                np.save(f, self.transitions)
                np.save(f, self.accept)
                np.save(f, self.reject)