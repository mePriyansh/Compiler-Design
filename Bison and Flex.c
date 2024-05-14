/*
1) Create the calc.yacc file
2) Create the calc.lex file
3) Run the following commands:
yacc -d calc.yacc
lex -d calc.lex
cc y.tab.c lex.yy.c
./a.out
  */

%{
#include <stdio.h>

int regs[26];  // Array to store values of variables 'a' to 'z'
int base;      // To determine the base of the number (octal or decimal)
%}

%start list
%union { int a; }

%token DIGIT LETTER
%left '|' '&'
%left '+' '-'
%left '*' '/' '%'
%left UMINUS /* Precedence for unary minus */

%%

/* Rules Section */
list: 
      /* Empty */
    | list stat '\n'
    | list error '\n' { yyerrok; }
    ;

stat: expr { printf("%d\n", $1.a); }
    | LETTER '=' expr { regs[$1.a] = $3.a; }
    ;

expr: '(' expr ')' { $$ = $2; }
    | expr '*' expr { $$.a = $1.a * $3.a; }
    | expr '/' expr { $$.a = $1.a / $3.a; }
    | expr '%' expr { $$.a = $1.a % $3.a; }
    | expr '+' expr { $$.a = $1.a + $3.a; }
    | expr '-' expr { $$.a = $1.a - $3.a; }
    | expr '&' expr { $$.a = $1.a & $3.a; }
    | expr '|' expr { $$.a = $1.a | $3.a; }
    | '-' expr %prec UMINUS { $$.a = -$2.a; }
    | LETTER { $$.a = regs[$1.a]; }
    | number
    ;

number: DIGIT { $$.a = $1.a; base = ($1.a == 0) ? 8 : 10; }
      | number DIGIT { $$.a = base * $1.a + $2.a; }
      ;

%%

/* Auxiliary C code section */
int main() {
    return yyparse();
}

void yyerror(const char *s) {
    fprintf(stderr, "%s\n", s);
}

int yywrap() {
    return 1;
}



// LEX FILE

%{
#include <stdio.h>
#include "y.tab.h"

int c;  // Global variable to hold the character value
%}

%%

" " ;    // Ignore whitespace

[a-z] {
    c = yytext[0];  // Get the character
    yylval.a = c - 'a';  // Calculate the index for the variable
    return LETTER;  // Return the token type LETTER
}

[0-9] {
    c = yytext[0];  // Get the character
    yylval.a = c - '0';  // Convert the character to an integer value
    return DIGIT;  // Return the token type DIGIT
}

[^a-z0-9\b] {
    c = yytext[0];  // Get the character
    return c;  // Return the character as its ASCII value (operators and other symbols)
}

%%

int yywrap() {
    return 1;  // Indicate end of input
}
