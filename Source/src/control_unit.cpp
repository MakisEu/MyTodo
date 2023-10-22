#include "../headers/control_unit.h"
#include "../headers/todo.h"
#include "../headers/database.h"
#include <vector>
#include <string>
#include <fstream>
#include <iostream>
#include <filesystem>
#include <QtSql>
#include <fstream>


/*
 * Opens a file containing the next id and reads it. If the file does not exist, it defaults to 0.
*/
ControlUnit::ControlUnit(){
    std::ifstream fin;
    fin.open("NextId.txt");
    nextId=0;
    std::string num;
    if (fin){
        getline(fin, num);
        nextId=QString::fromStdString(num).toInt();
    }
    fin.close();

}
/*
 * Creates the todo, Calls the addTodo function of the database.h  and increments the next id
*/
bool ControlUnit::AddTodo(std::string name,std::string start_date,std::string end_date,std::string date_created){
		Todo *todo=new Todo(name,start_date,end_date,date_created,nextId);
        addTodo(todo);
        nextId++;
        delete todo;
        return true;
}
/*
 * Calls the editTodo function of the database.h
*/
bool ControlUnit::EditTodo(Todo *td){
        editTodo(td);
        return true;
}
/*
 * Deletes the todo, sets the status of it to deleted and writes it into the history file
*/
bool ControlUnit::DeleteTodo(Todo *td){
        deleteTodo(td->getId());

        std::ofstream fout;
        fout.open("History.txt",std::ios_base::app);
        if (fout) {
            if (td->getStatus()!="Completed"){
                td->updateStatus("Deleted");
            }
            fout<<td->toString()+"\n";
        }
        fout.close();
        return true;
}
/*
 * Updates the status of the todo. If the todo is completed, it deletes it
*/
bool ControlUnit::UpdateTodoStatus(Todo *td,std::string status){
        updateStatus(td->getId(),status);
        td->updateStatus(status);
        if (status=="Completed"){
            this->DeleteTodo(td);
        }
        return true;
}
/*
 * Callsthe the getTodos function of database.h and iterates over the returned vector and converts the todos into string.
 * Returns a vector of the todos into string
*/
std::vector<std::string> ControlUnit::getStringTodos(){
        std::vector<Todo*> v=getTodos();
        std::vector<std::string> strings;

        std::vector<Todo*>::iterator it;
        for(it = v.begin() ;it != v.end() ;++it)
        {
        strings.push_back((*it)->toString());
            delete (*it);
        }
        return strings;
}
/*
 * Opens the history file that contains past todos and returns all the past todos as a vector of strings
*/
std::vector<std::string> ControlUnit::getPastHistory(){
        std::ifstream file;
        std::vector<std::string> strings;

        file.open("History.txt");
        if (file.is_open()) {
        std::string line;
        while (getline(file, line)) {
            // using printf() in all tests for consistency
            strings.push_back(line);
        }
        file.close();
        }
        return strings;
}

/*
 * Opens the file containing the next id and writes into it the next id
*/
ControlUnit::~ControlUnit(){
        std::ofstream fout;
        std::string num=std::to_string(nextId);
        fout.open("NextId.txt",std::ios::trunc | std::ios::out);
        if (fout) {
            fout<<num;
        }
        fout.close();
}
