/*How to run:
  1)Create a file using vim - vi file1.l
  2) Make it lex- lex file1.l
  3) Use Gcc - gcc file1.c
  4) Run using ./a.out*/
  

%{

%}


%%
int {printf("%s KEYWORD\n", yytext);}
float {printf("%s is a keyword",yytext);}

double {printf("%s is a keyword",yytext);}

char {printf("%s is a keyword",yytext);}

if {printf("%s is a keyword",yytext);}

else {printf("%s is a keyword",yytext);}

while {printf("%s is a keyword",yytext);}

do {printf("%s is a keyword",yytext);}

return {printf("%s is a keyword",yytext);}

break {printf("%s is a keyword",yytext);}

continue {printf("%s is a keyword",yytext);}

void {printf("%s is a keyword",yytext);}

switch {printf("%s is keyword",yytext);}

for {printf("%s is a keyword",yytext);}

typedef {printf("%s is a keyword",yytext);}

struct {printf("%s is a keyword",yytext);}

goto {printf("%s is a keyword",yytext);}

[a-z] {printf("%s IDENTIFIER\n", yytext);}
[0-9] {printf("%s IDENTIFIER\n", yytext);}
[+] {printf("%s OPERATOR\n", yytext);}
[-] {printf("%s OPERATOR\n", yytext);}
[*] {printf("%s OPERATOR\n", yytext);}
\n {return 0;}
%%


int yywrap(){}
int main(){


yylex();
return 0;
}


/* I/p:a123
  O/p: a IDENTIFIER
       1 IDENTIFIER
       2 IDENTIFIER
       3 IDENTIFIER
  */
