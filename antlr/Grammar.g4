grammar Grammar;

complete_script
        :script EOF
        ;

script
        : stmt SEMI (stmt SEMI)*
        ;

stmt
        : KW_CONNECT KW_TO STRING
        | KW_LIST KW_ALL KW_GRAPHS
        | select_stmt
        | named_pattern_stmt
        ;

named_pattern_stmt
        : NT_NAME OP_EQ pattern
        ;

select_stmt
        : KW_SELECT obj_expr KW_FROM STRING KW_WHERE where_expr
        ;

obj_expr
        : vs_info
        | KW_COUNT vs_info
        | KW_EXISTS vs_info
        ;

vs_info
        : LBR IDENT COMMA IDENT RBR
        | IDENT
        ;

where_expr
        : LBR v_expr RBR
         OP_MINUS pattern OP_ARROW
         LBR v_expr RBR
         ;

v_expr
        : IDENT
        | UNDERSCORE
        | IDENT DOT KW_ID OP_EQ INT
        ;

pattern
        : alt_elem
        | alt_elem MID pattern
        ;

alt_elem
        : seq_elem+
        | LBR RBR
        ;

seq_elem
        : prim_pattern
        | prim_pattern OP_STAR
        | prim_pattern OP_PLUS
        | prim_pattern OP_Q
        ;

prim_pattern
        : IDENT
        | NT_NAME
        | LBR pattern RBR
        ;

LBR
    : '('
    ;

RBR
    : ')'
    ;

COMMA
    : ','
    ;

SEMI
    : ';'
    ;

MID
    : '|'
    ;

DOT
    : '.'
    ;

OP_STAR
    : '*'
    ;

OP_PLUS
    : '+'
    ;

OP_Q
    : '?'
    ;

OP_MINUS
    : '-'
    ;

OP_ARROW
    : '->'
    ;

OP_EQ
    : '='
    ;

UNDERSCORE
    : '_'
    ;

KW_ID
    : 'ID'
    ;

KW_COUNT
    : 'count'
    ;

KW_EXISTS
    : 'exists'
    ;

KW_FROM
    : 'from'
    ;

KW_WHERE
    : 'where'
    ;

KW_SELECT
    : 'select'
    ;

KW_LIST
    : 'list'
    ;

KW_ALL
    : 'all'
    ;

KW_GRAPHS
    : 'graphs'
    ;

KW_CONNECT
    : 'connect'
    ;

KW_TO
    : 'to'
    ;

IDENT
    : 'a'..'z'+
    ;

INT
    : '0'
    | '1'..'9' '0'..'9'*
    ;

NT_NAME
    : [A-Z] [a-z]*
    ;

STRING
    : '['([a-z] | [A-Z] | [0-9] | ('-' | '_' | '/' | '.'))* ']'
    ;

WS
    : [ \n\t\r]+ -> skip;