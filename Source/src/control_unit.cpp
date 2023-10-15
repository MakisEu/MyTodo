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
    fin.open("../MyTodo/Source/db/NextId.txt");
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
bool ControlUnit::EditTodo(std::string name,std::string start_date,std::string end_date,int id){
		return false;
}
bool ControlUnit::DeleteTodo(int id){return true;}
bool ControlUnit::UpdateTodoStatus(std::string status){return true;}



ControlUnit::~ControlUnit(){
        std::ofstream fout;
        std::string num=std::to_string(nextId);
        fout.open("../MyTodo/Source/db/NextId.txt",std::ios::trunc | std::ios::out);
        if (fout) {
            fout<<num;
        }
        fout.close();
}
