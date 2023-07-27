# javascript 코드는 정상 동작을 했다고 가정.
# regex literal은 코드에 반영 안 함. 해야 됨.
# semicolon도 필요한 곳에 모두 있다고 가정. syntax만 분석하는데 그렇게까지 고려해야 할까 싶기도 하고...
# TODO : 유니코드 이스케이프 시퀀스 렉싱 이상함. 중괄호 내에 6글자로 한정될 필요 없고 안에 있는 숫자가 0x10FFFF보다만 작으면 되는데 그게 좀 힘드네...


from enum import Enum

import re


elems_of_kind:    tuple[str] = (
    'Unknown'                  , 'EndOfToken'         , 'NullLiteral'      , 'UndefinedLiteral'   , 'TrueLiteral'      , 'FalseLiteral'      , 'NumberLiteral'    , 'BigIntLiteral'          , 
    'Import'                   , 'Export'             , 'Catch'            , 'Finally'            , 'Throw'            , 'Try'               , 'Const'            , 'Var'                    , 
    'Class'                    , 'Extends'            , 'Function'         , 'New'                , 'Return'           , 'Yield'             , 'Super'            , 'This'                   , 
    'Continue'                 , 'Break'              , 'Do'               , 'For'                , 'In'               , 'While'             , 'Case'             , 'Default'                , 
    'Else'                     , 'If'                 , 'Switch'           , 'Delete'             , 'InstanceOf'       , 'Typeof'            , 'Void'             , 'With'                   , 
    'Identifier'               , 'Await'              , 'Debugger'         , 'Enum'               , 'StringLiteral'    , 'Add'               , 'Subtract'         , 'Multiply'               , 
    'Power'                    , 'Divide'             , 'Modulo'           , 'Increase'           , 'Decrease'         , 'BitwiseAnd'        , 'BitwiseOr'        , 'BitwiseXor'             , 
    'BitwiseNot'               , 'LeftShift'          , 'SignedRightShift' , 'UnsignedRightShift' , 'CoalesceNullish'  , 'Dot'               , 'OptionalChaining' , 'Assign'                 , 
    'AssignAdd'                , 'AssignSubtract'     , 'AssignMultiply'   , 'AssignPower'        , 'AssignDivde'      , 'AssignModulo'      , 'AssignLeftShift'  , 'AssignSignedRightShift' , 
    'AssignUnsignedRightShift' , 'AssignBitwiseAnd'   , 'AssignBitwiseOr'  , 'AssignBitwiseXor'   , 'AssignTruthy'     , 'AssignFalsy'       , 'AssignNullish'    , 'Equal'                  , 
    'StrictEqual'              , 'NotEqual'           , 'StrictNotEqual'   , 'Less'               , 'Greater'          , 'LessEqual'         , 'GreaterEqual'     , 'LogicalAnd'             , 
    'LogicalOr'                , 'LogicalNot'         , 'QuestionMark'     , 'Colon'              , 'LeftRoundBracket' , 'RightRoundBracket' , 'LeftBrace'        , 'RightBrace'             , 
    'LeftSquareBracket'        , 'RightSquareBracket' , 'Comma'            , 'Backtick'           , 'BigQuote'         , 'SingleQuote'       , 'Arrow'            , 'Semicolon'              , 
    'TemplateHeadLiteral', 'TemplateMiddleLiteral', 'TemplateTailLiteral', 'TemplateLiteral',
)
operator_bracket: tuple[str] = (
    '+'  , '-'   , '*'   , '**'   , '/'   , '%'   , 
    '++' , '--'  , '&'   , '|'    , '^'   , '~'   , 
    '<<' , '>>'  , '>>>' , '??'   , '.'   , '?.'  , 
    '='  , '+='  , '-='  , '*='   , '**=' , '/='  , 
    '%=' , '<<=' , '>>=' , '>>>=' , '&='  , '|='  , 
    '^=' , '&&=' , '||=' , '??='  , '=='  , '===' , 
    '!=' , '!==' , '<'   , '>'    , '<='  , '>='  , 
    '&&' , '||'  , '!'   , '?'    , ':'   , '('   , 
    ')'  , '{'   , '}'   , '['    , ']'   , ','   , 
    '`'   , '"'   , "'"  , '=>'   , ';'   , 
)

idx_of_fst_oper: int             = elems_of_kind.index('Add')
Kind:            Enum            = Enum('Kind', elems_of_kind)
str_kind:        dict[str, Kind] = {
    **{
        x if not ((x := e.lower()) in {'unknown', 'endoftoken', 'identifier'} or x.endswith('literal')) else
        y if (y := x.removesuffix('literal')) in {'true', 'false', 'null', 'undefined'}                 else
        f'#{y}'
        : k for e, k in zip(elems_of_kind[:idx_of_fst_oper], Kind)
    },
    **{o: Kind[n] for o, n in zip(operator_bracket, elems_of_kind[idx_of_fst_oper:])},
}
kind_str:        dict[str, Kind] = {v: k for k, v in str_kind.items()}


def from_str(string: str) -> Kind: return str_kind.get(string, Kind.Unknown)


def from_kind(kind: Kind) -> str: return kind_str.get(kind, '')


def analyze_lexeme(code: str) -> tuple[tuple[Kind, str]]:
    re_special_chars = str.maketrans({
        '.': r'\.', '^': r'\^', '$': r'\$', '*': r'\*', '+': r'\+', '?': r'\?', '|': r'\|', '\\': r'\\',
        '(': r'\(', ')': r'\)', '{': r'\{', '}': r'\}', '[': r'\[', ']': r'\]', '-': r'\-',
    })
    
    deci_int     = r'0|[1-9][\d_]*|(0[89]|0[0-7]+[89])+\d*'
    deci_digits  = r'\d[\d_]*'
    decimal      = rf'({deci_int}|.{deci_digits}|{deci_int}.({deci_digits})?)([Ee][+-]?({deci_digits}))?' 
    bigint       = r'(0|[1-9]\d*|[1-9][\d_]*)n'
    non_deci_int = r'0(?i:b[01][01_]*|o[0-7][0-7_]*|x[a-f0-9][a-f0-9_]*)n?'
    leg_oct_int  = r'0[0-7]+'
    
    dbl_str_chars = r'([^"\\\r\n]|\\(?i:[^ux\d]|0\D|0[89]|[1-7][^0-7]|[0-3][0-7][^0-7]|[4-7][0-7]|[0-3][0-7]{2}|x[a-f0-9]{2}|u[a-f0-9]{4}|u\{[a-f0-9]{0,6}\}|\r\n))*' # MEMO : LS PS는 뭔지 모르겠음
    sgl_str_chars = r"([^'\\\r\n]|\\(?i:[^ux\d]|0\D|0[89]|[1-7][^0-7]|[0-3][0-7][^0-7]|[4-7][0-7]|[0-3][0-7]{2}|x[a-f0-9]{2}|u[a-f0-9]{4}|u\{[a-f0-9]{0,6}\}|\r\n))*" 
    
    template_chars  = r'([^`\\\$]|\$[^\{]|\\([^ux\d]|[1-9]|x[a-f0-9]{2}|u[a-f0-9]{4}|u\{[a-f0-9]{0,6}\}|\r\n))*'
    
    re_white_space         = re.compile(r'\s+')
    re_num_literal         = re.compile(rf'{decimal}|{bigint}|{non_deci_int}|{leg_oct_int}')
    re_str_literal         = re.compile(rf'"{dbl_str_chars}"' + rf"'{sgl_str_chars}'")
    re_tmplt_head_literal  = re.compile(r'`('  + template_chars + r')?\$\{')
    re_tmplt_mid_literal   = re.compile(r'\}(' + template_chars + r')?\$\{')
    re_tmplt_tail_literal  = re.compile(r'\}(' + template_chars + r')?')
    re_tmplt_literal       = re.compile(rf'`{template_chars}`')
    re_identifier_kyword   = re.compile(r'[#_\$a-zA-Z][\$\w]*') # 원래 이렇게 두면 안 됨. class 안에 있을 때만 허용해야 됨.
    re_operator_bracket    = re.compile('|'.join(i.translate(re_special_chars) for i in sorted(operator_bracket, key=len, reverse=True)))
    
    
    def analyze_lexeme_inner(code: str, context: dict[str: bool], result: tuple[tuple[Kind, str]]) -> tuple[tuple[Kind, str]]:
        if not code: return result
    
        if matched := re_white_space.match(code): return analyze_lexeme_inner(code[matched.end():], context, result)
        if matched := re_num_literal.match(code): return analyze_lexeme_inner(code[matched.end():], context, result + ((Kind.NumberLiteral, matched.group()),))
        if matched := re_str_literal.match(code): return analyze_lexeme_inner(code[matched.end():], context, result + ((Kind.StringLiteral, matched.group()),))
        if matched := re_tmplt_literal.match(code): return analyze_lexeme_inner(code[matched.end():], context, result + ((Kind.TemplateLiteral, matched.group()),))
        if (matched := re_tmplt_head_literal.match(code)) and not context['in_tmplt']: return analyze_lexeme_inner(code[matched.end():], context | {'in_tmplt': True}, result + ((Kind.TemplateHeadLiteral, matched.group()),))
        if (matched := re_tmplt_mid_literal.match(code)) and context['in_tmplt']: return analyze_lexeme_inner(code[matched.end():], context, result + ((Kind.TemplateMiddleLiteral, matched.group())))
        if (matched := re_tmplt_tail_literal.match(code)) and context['in_tmplt']: return analyze_lexeme_inner(code[matched.end():], context | {'in_tmplt': False}, result + ((Kind.TemplateTailLiteral, matched.group())))
        if matched := re_identifier_kyword.match(code): 
            # print(matched.group())
            return analyze_lexeme_inner(code[matched.end():], context, result + ((str_kind.get(matched.group(), Kind.Identifier), matched.group()),))
        if matched := re_operator_bracket.match(code): return analyze_lexeme_inner(code[matched.end():], context, result + ((str_kind[matched.group()], matched.group()),))
        
        print('UNKOWN: ', code[:40])
        exit(1)
            
    
    return analyze_lexeme_inner(code, {'in_tmplt': False}, ())
