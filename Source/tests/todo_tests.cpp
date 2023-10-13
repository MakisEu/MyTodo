#include <iostream>
#include <cassert>
#include "../headers/todo.h"

using namespace std;



void testConstructor() {
    Todo todo("Task", "2022-01-01", "2022-01-05", "2021-12-31", 1);

    assert(todo.getName() == "Task");
    assert(todo.getStartDate() == "2022-01-01");
    assert(todo.getEndDate() == "2022-01-05");
    assert(todo.getDateCreated() == "2021-12-31");
    assert(todo.getId() == 1);
}

void testEditTodo() {
    Todo todo("Task", "2022-01-01", "2022-01-05", "2021-12-31", 1);
    todo.editTodo("New Task", "2022-02-01", "2022-02-05", "2022-01-31");

    assert(todo.getName() == "New Task");
    assert(todo.getStartDate() == "2022-02-01");
    assert(todo.getEndDate() == "2022-02-05");
    assert(todo.getDateCreated() == "2022-01-31");
}

void testUpdateStatus() {
    Todo todo("Task", "2022-01-01", "2022-01-05", "2021-12-31", 1);
    todo.updateStatus("Completed");

    assert(todo.getStatus() == "Completed");
}

void testDestructor() {
    Todo* todo = new Todo("Task", "2022-01-01", "2022-01-05", "2021-12-31", 1);
    delete todo;
}

void testEverything(){
		Todo todo("task", "01/01/2022", "01/10/2022", "12/31/2021", 1);

		/*cout << "Name: " << todo.getName() << endl;
		cout << "Start Date: " << todo.getStartDate() << endl;
		cout << "End Date: " << todo.getEndDate() << endl;
		cout << "Date Created: " << todo.getDateCreated() << endl;
		cout << "ID: " << todo.getId() << endl;*/
		

		assert(todo.getName()=="task"); 
		assert(todo.getStatus()=="In Progress"); 
		assert(todo.getDateCreated()=="12/31/2021");
		assert(todo.getStartDate()=="01/01/2022");
		assert(todo.getEndDate()=="01/10/2022");
		assert(todo.getId()==1);
		todo.editTodo("new task", "02/01/2022", "02/10/2022", "01/31/2022");

		/*cout << "Name (after edit): " << todo.getName() << endl;
		cout << "Start Date (after edit): " << todo.getStartDate() << endl;
		cout << "End Date (after edit): " << todo.getEndDate() << endl;
		cout << "Date Created (after edit): " << todo.getDateCreated() << endl;*/



		assert(todo.getName()=="new task");
		assert(todo.getStatus()=="Completed");
		assert(todo.getDateCreated()=="01/31/2022");
		assert(todo.getStartDate()=="02/01/2022");
		assert(todo.getEndDate()=="02/10/2022");
		assert(todo.getId()==1);
}



int main() { // Test the Todo class
		testConstructor();
		testEditTodo();
		testUpdateStatus();
		testDestructor();
		testEverything();
		return 0; 
}

