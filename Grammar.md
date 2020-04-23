В этом файле описывается язык запросов.
Скрипт должен соответствовать лексике, описанной ниже. Исходно он выглядит как 
````<script>````, ```eps``` - это пустая строка.
```
script: eps
            | <statement>; <script>

statement: connect to [<dir_name>]
            | list all graphs
            | select <obj> from [<file_name>] where <where_expr>
            | <NT_NAME> = <pattern>

obj: <vertices>
    | count <vertices>
    | exists <vertices>

vertices: ( <ID> , <ID> )
            | <ID>

where_expr: ( <v_expr> ) - <regexp> -> ( <v_expr> )

v_expr: <ID>
        | _ 
        | <ID>.ID = INT

regexp: <seq_elem>
        | <seq_elem> | <regexp>                   - второй '|' это символ

seq_elem: <seq>
        | ()

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

dir_name - абсолютный путь к директории

file_name - абсолютный путь к файлу
``` 

Пример:
```
connect to [/home/user/graph];
S = a S b S | () ;
select count u from [/hime/user/g1.txt] where (v.ID = 10) - S -> (u);
```
Или:
```
connect to [/home/user/graph];
S = a S b;
select exists (a , b) from [/home/user/g1] where (_) - S -> (a);
```
