# javascript 코드는 정상 동작을 했다고 가정.


from enum import Enum, auto


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
'`'   , '"'   , "'"    , '=>'  , ';'  , 
)

Kind:     Enum            = Enum('Kind', elems_of_kind)
str_kind: dict[str, Kind] = {
    **{
        x if not ((x := e.lower()) in {'unknown', 'endoftoken', 'identifier'} or x.endswith('literal')) else
        y if (y := x.removesuffix('literal')) in {'true', 'false', 'null', 'undefined'}                 else
        f'#{y}'
        : k for e, k in zip(elems_of_kind[:elems_of_kind.index('Add')], Kind)
    },
    **{o: Kind[n] for o, n in zip(operator_bracket, elems_of_kind[elems_of_kind.index('Add'):])},
}
kind_str: dict[str, Kind] = {v: k for k, v in str_kind.items()}


def from_str(string: str) -> Kind: return str_kind.get(string, Kind.Unknown)


def from_kind(kind: Kind) -> str: return kind_str.get(kind, '')
