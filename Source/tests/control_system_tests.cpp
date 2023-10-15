#include <iostream>
#include "../headers/todo.h"
#include "../headers/control_unit.h"
#include <cassert>

using namespace std;

void Add_Todo_tests(){
		ControlUnit *cn=new ControlUnit();
		cn->AddTodo("JohnDoe","12/09/2020","11/4/2021","13/8/2020");
		cout<<"Size:"<<cn->getTodos().size()<<endl;
		cn->AddTodo("MaryDoe","02/11/2022","10/3/2021","13/8/2020");
		cout<<"Size:"<<cn->getTodos().size()<<endl;

}

int main(){
		Add_Todo_tests();
		return 0;
}
