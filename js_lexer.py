# javascript 코드는 정상 동작을 했다고 가정.
# regex literal은 코드에 반영 안 함. 해야 됨.


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
    deci_int     = r'0|[1-9][\d_]*|(0[89]|0[0-7]+[89])+\d*'
    deci_digits  = r'\d[\d_]*'
    decimal      = rf'({deci_int}|.{deci_digits}|{deci_int}.({deci_digits})?)([Ee][+-]?({deci_digits}))?' 
    bigint       = r'(0|[1-9]\d*|[1-9][\d_]*)n'
    non_deci_int = r'0(?i:b[01][01_]*|o[0-7][0-7_]*|x[a-f0-9][a-f0-9_]*)n?'
    leg_oct_int  = r'0[0-7]+'
    
    dbl_str_chars = r'([^"\\\r\n]|\\(?i:[^ux\d]|0\D|0[89]|[1-7][^0-7]|[0-3][0-7][^0-7]|[4-7][0-7]|[0-3][0-7]{2}|x[a-f0-9]{2}|u[a-f0-9]{4}|u\{[a-f0-9]{0,6}\}|\r\n))*' # MEMO : LS PS는 뭔지 모르겠음
    sgl_str_chars = r"([^'\\\r\n]|\\(?i:[^ux\d]|0\D|0[89]|[1-7][^0-7]|[0-3][0-7][^0-7]|[4-7][0-7]|[0-3][0-7]{2}|x[a-f0-9]{2}|u[a-f0-9]{4}|u\{[a-f0-9]{0,6}\}|\r\n))*" 
    
    re_white_space = re.compile(r'\s+')
    re_num_literal = re.compile(rf'{decimal}|{bigint}|{non_deci_int}|{leg_oct_int}')
    re_str_literal = re.compile(rf'"{dbl_str_chars}"' + rf"'{sgl_str_chars}'")
    
    def analyze_lexeme_inner(code: str, result: tuple[tuple[Kind, str]]) -> tuple[tuple[Kind, str]]:
        if not code: return result
    
        if matched := re_white_space.match(code): return analyze_lexeme_inner(code[matched.end():], result)
        if matched := re_num_literal.match(code): return analyze_lexeme_inner(code[matched.end():], result + ((Kind.NumberLiteral, matched.string),))
        if matched := re_str_literal.match(code): return analyze_lexeme_inner(code[matched.end():], result + ((Kind.StringLiteral, matched.string),))
    
    return analyze_lexeme_inner(code, ())
