#include "../headers/database.h"
#include "../headers/helper.h"
#include "../headers/todo.h"
#include "../headers/reminder.h"
#include <iostream>
#include <QtSql>
#include <vector>
#include <string>

QSqlDatabase DB;
/*
 * Opens an SQLite database from a file
*/
void openDB(){

    QString path = "currentTodos.db";
    DB = QSqlDatabase::addDatabase("QSQLITE");
    DB.setDatabaseName(path);
    DB.open();
}
/*
 * Closes the database
*/
void closeDB(){
    DB.close();
}
/*
 * Creates the Todo and Reminder tables
*/
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
    query.prepare("CREATE TABLE IF NOT EXISTS Reminders("
                  "TODOID         INT      NOT NULL, "
                  "MESSAGE        TEXT     NOT NULL, "
                  "TITLE          CHAR(50) NOT NULL, "
                  "DATE           CHAR(19) NOT NULL, "
                  "PRIMARY KEY (TODOID,DATE),        "
                  "FOREIGN KEY (TODOID) REFERENCES Todo(ID) ON DELETE CASCADE);");
    query.exec();
}
/*
 * Preps the todo values (to prevent sql injection), stores the todo and create reminders for the start date and end date of the todo
*/
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

    query.prepare("INSERT INTO Reminders (TODOID,MESSAGE,TITLE,DATE) VALUES (:id,:msg,:title,:date);");
    query.bindValue(":id",newTodo->getId());
    query.bindValue(":msg","The todo "+QString::fromStdString(name)+" has started.");
    query.bindValue(":title","Todo Has Started");
    query.bindValue(":date",QString::fromStdString(start_date));
    query.exec();


    query.prepare("INSERT INTO Reminders (TODOID,MESSAGE,TITLE,DATE) VALUES (:id,:msg,:title,:date);");
    query.bindValue(":id",newTodo->getId());
    query.bindValue(":msg","The todo "+QString::fromStdString(name)+" has expired.");
    query.bindValue(":title","Todo Has Expired");
    query.bindValue(":date",QString::fromStdString(end_date));
    query.exec();
}
/*
 * Returns all the todos in the database in a vector
*/
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
/*
 * Deletes the todo and the reminders associated with the todo
*/
void deleteTodo(int id){
    QSqlQuery query(DB);
    query.exec("PRAGMA foreign_keys = ON");
    query.prepare("DELETE FROM Todo WHERE ID ="+QString::fromStdString(std::to_string(id))+";");
    query.exec();
}
/*
 * Edits a todo and re-creates the reminders according to the new datetimes
*/
void editTodo(Todo *td){
    QSqlQuery query(DB);
    QString start,end;
    query.prepare("SELECT * FROM Todo WHERE ID;");
    query.exec();
    query.next();
    start=query.value(3).toString();
    end=query.value(4).toString();

    query.prepare("UPDATE Todo SET NAME=:name, START_DATE=:sd, END_DATE=:ed WHERE ID=:id;");
    query.bindValue(":name",QString::fromStdString(td->getName()));
    query.bindValue(":sd",QString::fromStdString(td->getStartDate()));
    query.bindValue(":ed",QString::fromStdString(td->getEndDate()));
    query.bindValue(":id",td->getId());
    query.exec();

    query.prepare("DELETE FROM Reminders WHERE TODOID=:id;");
    query.exec();

    query.prepare("INSERT INTO Reminders (TODOID,MESSAGE,TITLE,DATE) VALUES (:id,:msg,:title,:date);");
    query.bindValue(":id",td->getId());
    query.bindValue(":msg","The todo "+QString::fromStdString(td->getName())+" has started.");
    query.bindValue(":title","Todo Has Started");
    query.bindValue(":date",QString::fromStdString(td->getStartDate()));
    query.exec();


    query.prepare("INSERT INTO Reminders (TODOID,MESSAGE,TITLE,DATE) VALUES (:id,:msg,:title,:date);");
    query.bindValue(":id",td->getId());
    query.bindValue(":msg","The todo "+QString::fromStdString(td->getName())+" has expired.");
    query.bindValue(":title","Todo Has Expired");
    query.bindValue(":date",QString::fromStdString(td->getEndDate()));
    query.exec();
}
/*
 * Updates the status the of a todo with a specific id
*/
void updateStatus(int id,std::string s){
    QSqlQuery query(DB);
    query.prepare("UPDATE Todo SET STATUS=:status WHERE ID=:id;");
    query.bindValue(":status",QString::fromStdString(s));
    query.bindValue(":id",id);
    if (!query.exec()){
        int x=10;
    }
}
/*
 * Returns all the reminders with a specific datetime
*/
std::vector<Reminder*> getReminders(QString datetime){
    QSqlQuery query(DB);
    std::vector <Reminder*> vec;
    query.prepare("SELECT TODOID,MESSAGE,TITLE FROM Reminders WHERE DATE=:datetime ;");
    query.bindValue(":datetime",datetime);
    query.exec();
    Reminder *rm;

    while (query.next()){
        rm=new Reminder(query.value(0).toInt(),query.value(1).toString(),query.value(2).toString());
        vec.push_back(rm);
    }
    return vec;
}
/*
 * Deletes a reminder with a specific Todo id
*/
void deleteReminder(int id, QString datetime){
    QSqlQuery query(DB);
    query.prepare("DELETE FROM Reminders WHERE TODOID=:id AND DATE=:datetime ;");
    query.bindValue(":id",id);
    query.bindValue(":datetime",datetime);
    query.exec();
}


