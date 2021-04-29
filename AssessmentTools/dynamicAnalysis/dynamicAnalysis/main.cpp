//
//  main.cpp
//  dynamicAnalysis
//
//  Created by Official on 26/03/21.
//

#include<iostream>
using namespace std;

void memleak(){
  int *i = new int[100];
  return;
}

void memoutofbound(){
  int *i = new int[100];
  i[100] = 100;
  cout<<i<<endl;
}

void uninitialisedVariables(){
  int i;
  if(i==100){
    cout << 100 << endl;
  }
  else{
    cout << i << endl;
  }
}

void illegalfree(){
  int *a;
  delete a;
  return;
}

void forloop(){
    for(int i=0;i<100000;i++){
        
    }
}



int main(int argc, const char * argv[]) {
    // insert code here...
    std::cout << "Hello, World!\n";
    memleak();
    memoutofbound();
    uninitialisedVariables();
    illegalfree();

    return 0;
}
