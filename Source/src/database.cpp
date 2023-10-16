#include "../headers/database.h"
#include "../headers/helper.h"
#include "../headers/todo.h"
#include <iostream>
#include <QtSql>
#include <vector>
#include <string>

QSqlDatabase DB;
void openDB(){

    QString path = "../MyTodo/Source/db/currentTodos.db";
    DB = QSqlDatabase::addDatabase("QSQLITE");
    DB.setDatabaseName(path);
    DB.open();
}
void closeDB(){
    DB.close();
}

void createTables(){
    QSqlQuery query(DB);
    query.prepare("CREATE TABLE IF NOT EXISTS Todo("
                  "ID INT PRIMARY KEY      NOT NULL, "
                  "NAME           TEXT     NOT NULL, "
                  "STATUS         TEXT     NOT NULL, "
                  "START_DATE     CHAR(19) NOT NULL, "
                  "END_DATE       CHAR(19) NOT NULL, "
                  "DATE_CREATED   char(19) NOT NULL);");
    query.exec();
}

void addTodo(Todo* newTodo){
    std::string name,status,start_date,end_date,date_created;
    name=newTodo->getName();
    replace(name,"\'","\'\'");
    replace(name,"\"","\"\"");
    status=newTodo->getStatus();
    replace(status,"\'","\'\'");
    replace(status,"\"","\"\"");
    start_date=newTodo->getStartDate();
    replace(start_date,"\'","\'\'");
    replace(start_date,"\"","\"\"");
    end_date=newTodo->getEndDate();
    replace(end_date,"\'","\'\'");
    replace(end_date,"\"","\"\"");
    date_created=newTodo->getDateCreated();
    replace(date_created,"\'","\'\'");
    replace(date_created,"\"","\"\"");

    QSqlQuery query(DB);
    query.prepare("INSERT INTO Todo (ID,NAME,STATUS,START_DATE,END_DATE,DATE_CREATED) VALUES (:id,:name,:status,:start_date,:end_date,:date_created);");
    query.bindValue(":id",newTodo->getId());
    query.bindValue(":name",QString::fromStdString(name));
    query.bindValue(":status",QString::fromStdString(status));
    query.bindValue(":start_date",QString::fromStdString(start_date));
    query.bindValue(":end_date",QString::fromStdString(end_date));
    query.bindValue(":date_created",QString::fromStdString(date_created));
    query.exec();

}
std::vector<Todo*> getTodos(){
    QSqlQuery query(DB);
    query.prepare("SELECT * FROM Todo;");
    if (!query.exec()){
        //Error
    }
    std::vector <Todo*> v;
    std::string name,status,start_date,end_date,date_created;
    int id;
    Todo* td;
    while (query.next()){
        id=query.value(0).toInt();
        name=query.value(1).toString().toStdString();
        status=query.value(2).toString().toStdString();
        start_date=query.value(3).toString().toStdString();
        end_date=query.value(4).toString().toStdString();
        date_created=query.value(5).toString().toStdString();
        td=new Todo(name,start_date,end_date,date_created,id);
        td->updateStatus(status);
        v.push_back(td);
    }
    return v;
}
void deleteTodo(int id){
    QSqlQuery query(DB);
    query.prepare("DELETE FROM Todo WHERE ID ="+QString::fromStdString(std::to_string(id))+";");
    query.exec();
}
void editTodo(Todo *td){
    QSqlQuery query(DB);
    query.prepare("UPDATE Todo SET NAME=:name, START_DATE=:sd, END_DATE=:ed WHERE ID=:id;");
    query.bindValue(":name",QString::fromStdString(td->getName()));
    query.bindValue(":sd",QString::fromStdString(td->getStartDate()));
    query.bindValue(":ed",QString::fromStdString(td->getEndDate()));
    query.bindValue(":id",td->getId());
    query.exec();
}
void updateStatus(int id,std::string s){
    QSqlQuery query(DB);
    query.prepare("UPDATE TODO SET STATUS=:status WHERE ID=:id;");
    query.bindValue(":status",QString::fromStdString(s));
    query.exec();
}


Database::Database()
{

}
