from js_parser_util import Tockens
from js_lexer import Kind, analyze_lexeme


contexts = [[[], []]]


def estimate_source(tkns: Tockens):
    while True:
        tkns.skip_brace({Kind.Var, Kind.Const, Kind.Let, Kind.Class, Kind.Function})
        idx = tkns.idx
        
        if any((
            tkns.token_at(idx - 1)[0] != Kind.Semicolon,  
            tkns.token_at(idx + 1)[0] != Kind.Identifier,
        )):
            tkns.skip_val_any()
            continue
        
        # var function / const let class 저장할 공간이 다르고요
        # 함수같은 경우에는 함수 자체를 선언부터 할당(undefined를 할당을 안 함) -> function키워드가 있었던 index
        # var은 undefined
        
        if tkns.token_at(idx) in {Kind.Var, Kind.Function}:
            contexts[0][0].append((tkns.token_at(idx), tkns.token_at(idx + 1), ()))
        else:
            contexts[0][1].append((tkns.token_at(idx), tkns.token_at(idx + 1), None))
        
        print(f'{tkns.token_at(idx - 1)=}, {tkns.token_at(idx)=} {tkns.token_at(idx + 1)=}')
        input(' : ')
        

import sys
    
target_nm = sys.argv[1]

with open(target_nm, 'rt') as f:
    target = f.read()
    result = analyze_lexeme(target)
    estimate_source(Tockens(result))