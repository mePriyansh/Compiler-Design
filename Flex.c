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
