//
//  main.c
//  assessmentTool
//
//  Created by Official on 25/03/21.
//

#include <stdio.h>


void outofbound(){
  int a[10];
  a[10] = 0;
}

int unexecutedCode(){
  int a = 5;
  printf("First Executed %d\n",a);
  return 1;
  int b = 4;
    printf("Unexecuted %d\n",b);
}

void divbyzero(){
  int x = 1/0;
}

void nullptrDereference(){
  int *p=NULL;
//  *p=4;
}
void typemismatch(){
  int a,*aptr;
  float b , *bptr;
  b = 5.5;
  a = 4;
  aptr = &a;
  bptr = aptr;
}

int strreturn(){
    float a;
    int b;
    a = 5.5;
    return "123";
}

void uninitialisedVariables(){
  int i;
  if(i==100){
      printf("100\n");
  }
  else{
      printf("not 100\n");
  }
}

void intoverflow(){
  int a = 10000000;
  a = a*a*a*a;
}


int main(int argc, const char * argv[]) {
    // insert code here...
    int a=5;
    printf("Hello, World!\n");
    return 0;
}
