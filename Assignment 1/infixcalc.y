/* Infix notation calculator. */

%{
  #include <math.h>
  #include <stdio.h>
  #include<stdlib.h>
  #include<ctype.h>
  int yylex (void);
  void yyerror (char const *);
  int founderror = 0;
  char op;
%}


/* Bison declarations. */
%define api.value.type {double}
%token NUMBER
%token ADD
%token SUBTRACT
%token DIVIDE
%token MULTIPLY
%token EXPONENTIAL
%token NL
%token OB
%token CB
%token ID

%left ADD SUBTRACT
%left MULTIPLY DIVIDE
%right EXPONENTIAL        /* exponentiation */

%% /* The grammar follows. */
input:
  %empty
| input line
;

line:
  NL {printf("Enter Valid expression\n");}
| exp NL  { if(!founderror){printf ("Value = %.10g\n", $1);} return 0; }
;

exp:
  NUMBER
| exp ADD exp             { $$ = $1 + $3;}
| exp SUBTRACT exp        { $$ = $1 - $3;}
| exp MULTIPLY exp        { $$ = $1 * $3;}
| exp DIVIDE exp          { if($3==0){
                              yyerror("Division by zero");
                              return 0;
                            }
                            $$ = $1 / $3;}
| exp EXPONENTIAL exp     { $$ = pow ($1, $3);}
| OB exp CB             { $$ = $2;}
;
%%

int
main (void)
{
  printf("************************************  Welcome To Calculator Builded Using \"LEX\" and \"BISON\"  ************************************\n");
  while(1){
    founderror=0;
    printf(" ************  Enter The Expression : ************\n");
    yyparse ();
  }
  printf("****END***");
  return 0;
}


/* Called by yyparse on error. */
/*
void
yyerror (char const *s)
{
  fprintf (stderr, "%s\n", s);
  founderror = 1;
}
*/
