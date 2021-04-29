%{
#include<math.h>
#include "infixcalc.tab.h"
extern int founderror;
void
yyerror (char const *s);
%}
digit [0-9]
number {digit}+(\.{digit}*)?
add "+"
sub "-"
mul "*"
div "/"
exp "^"
ws [ \t]
nl [\n]
ob "("
cb ")"
characters [a-zA-Z]
id {characters}+

%%
{ws}+ {;}
{ob} {return(OB);}
{cb} {return(CB);}
{number} {yylval=atof(yytext); return(NUMBER);}
{add} { return(ADD);}
{sub} { return(SUBTRACT);}
{mul} { return(MULTIPLY);}
{div} { return(DIVIDE);}
{exp} { return(EXPONENTIAL);}
{nl} {return NL;}
{id} {return ID;}
%%


int yywrap(){
  return 0;
}

void
yyerror (char const *s)
{
  fprintf (stderr, "Error - %s\n", s);
  founderror = 1;
}
