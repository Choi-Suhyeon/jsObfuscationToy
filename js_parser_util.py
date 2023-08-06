from js_lexer import Kind, from_str, from_kind


class Tockens:
    def __init__(self, tkns: tuple[tuple[Kind, str]]):
        self.__tkns: tuple[tuple[Kind, str]] = tkns
        self.__idx:  int                     = 0

        
    def find_idx_with_kinds(self, kinds: set[Kind], idx: int = None, terminated: set[Kind] = set()):
        i = self.__idx if idx is None else idx
        
        try:
            while True:
                if self.__tkns[i][0] in kinds:      return i
                if self.__tkns[i][0] in terminated: break
                
                i += 1
        except IndexError: pass
        
        return -1


    def skip_brace(self):
        once_enter    = False
        num_of_nested = 0
        
        while True:
            if once_enter and not num_of_nested:                break
            elif self.__tkns[self.__idx][0] == Kind.LeftBrace:  num_of_nested += 1; once_enter = True
            elif self.__tkns[self.__idx][0] == Kind.RightBrace: num_of_nested -= 1
            
            self.skip_val_any()


    def skip_brace(self, terminated: set[Kind]):
        once_enter    = False
        num_of_nested = 0
        
        while True:
            is_time_to_break = self.__tkns[self.__idx][0] in terminated
            
            if once_enter and not num_of_nested and is_time_to_break: break
            elif not once_enter and is_time_to_break:                 break
            elif self.__tkns[self.__idx][0] == Kind.LeftBrace:        num_of_nested += 1; once_enter = True
            elif self.__tkns[self.__idx][0] == Kind.RightBrace:       num_of_nested -= 1
            
            self.skip_val_any()

 
    def skip_val(self, kind: Kind):
        if self.__tkns[self.__idx][0] != kind: self.__parse_error()
        else:                                  self.__idx += 1
 

    def skip_val_if(self, kind: Kind):
        self.__idx = self.__idx + (self.__tkns[original := self.__idx][0] == kind)
        
        return bool(self.__idx - original)


    def skip_val_any(self, step: int = 1):
        self.__idx += step
        

    def __parse_error(self):
        print('[ERR] Parse Error')
        exit(1)
        

    def token_at(self, idx: int | None = None):
        return self.__tkns[self.__idx if idx is None else idx]
        
    
    @property
    def idx(self):
        return self.__idx
    