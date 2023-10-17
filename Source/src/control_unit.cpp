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
bool ControlUnit::AddTodo(std::string name,std::string start_date,std::string end_date,std::string date_created){
		Todo *todo=new Todo(name,start_date,end_date,date_created,nextId);
        addTodo(todo);
        nextId++;
        delete todo;
        return true;
}
bool ControlUnit::EditTodo(Todo *td){
        editTodo(td);
        return true;
}
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
bool ControlUnit::UpdateTodoStatus(Todo *td,std::string status){
        updateStatus(td->getId(),status);
        td->updateStatus(status);
        this->DeleteTodo(td);
        return true;
}

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


ControlUnit::~ControlUnit(){
        std::ofstream fout;
        std::string num=std::to_string(nextId);
        fout.open("NextId.txt",std::ios::trunc | std::ios::out);
        if (fout) {
            fout<<num;
        }
        fout.close();
}
