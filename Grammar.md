В этом файле описывается язык запросов.
Скрипт может быть пустым, или состоять из строчек вида:
```
<statement>;
```
Вот как могут выглядеть выражения в языке:
```
statement: CONNECT TO [<file_name>]
            | LIST ALL GRAPHS
            | SELECT <obj> FROM [<file_name>] WHERE <where_expr>
            | <NT_NAME> = <pattern>

obj: <vertices>
    | COUNT <vertices>
    | EXISTS <vertices>

vertices: ( <ID> , <ID> )
            | <ID>

where_expr: ( <v_expr> ) - <regexp> -> ( <v_expr> )

v_expr: <ID>
        | _ 
        | <ID>.ID = INT

regexp: <seq>
        | ()
        | <seq> | <regexp>
        | () | <regexp>

seq: <elem>
      | <elem> seq

elem: <prim_pattern>
        | <prim_pattern> *
        | <prim_pattern> +
        | <prim_pattern> ?

prim_pattern: <ID>
               | NT_NAME
               | ( <regexp> )

ID: [a-z][a-z]*

NT_NAME: [A_Z][a-z]*
``` 

Пример:
```
CONNECT TO [/home/user/graph];
S = a S b S | () ;
SELECT COUNT u FROM [/hime/user/g1.txt] WHERE (v.ID = 10) - S -> (u)
```
Или:
```
CONNECT TO [/home/user/graph];
S = a S b;
SELECT EXISTS (a , b) FROM [/home/user/g1] WHERE (_) - S -> (a)
```
