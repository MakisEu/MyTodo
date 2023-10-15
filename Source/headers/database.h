#ifndef DATABASE_H
#define DATABASE_H

#include <QtSql>
#include <string>
#include "todo.h"

extern QSqlDatabase DB;

void openDB();
void closeDB();
void createTables();
void addTodo(Todo* newTodo);
std::vector<Todo*> getTodos();
class Database
{
public:
    Database();
};

#endif // DATABASE_H
