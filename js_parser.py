from js_lexer import Kind, from_str, from_kind

tkns: tuple[tuple[Kind, str]]
idx:  int

        
def find_with_kind(kind: Kind, idx_param: int = None, terminated: set[Kind] = set()):
    for i in range(idx if idx_param is None else idx_param):
        if tkns[i][0] == kind:       return i
        if kind[i][0] in terminated: break
    
    return -1


def build_skip_brace(break_cond):
    global tkns; global idxgi
    
    num_of_nested = 0
    once_enter = False
    
    while True:
        if once_enter and not num_of_nested:  
            if break_cond(tkns[idx][0]): break
        elif tkns[idx][0] == Kind.LeftBrace:  num_of_nested += 1; once_enter = True
        elif tkns[idx][0] == Kind.RightBrace: num_of_nested -= 1
        
        skip_val_any()


def skip_brace():
    build_skip_brace(lambda _: True)


def skip_brace(terminated: set[Kind] = set()):
    global idx
    
    build_skip_brace(lambda elem: (idx := (original := idx) + (elem in terminated)) - original)


def skip_val(kind: Kind):
    global tkns; global idx
    
    if tkns[idx][0] != kind: parse_error()
    else:                    idx += 1
 

def skip_val_if(kind: Kind):
    global tkns; global idx
    
    return bool((idx := idx + (tkns[original := idx][0] == kind)) - original)

    
def skip_val_any():
    global idx
    
    idx += 1
        

def parse_error():
    print('[ERR] Parse Error')
    exit(1)
    