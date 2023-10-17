#ifndef DATABASE_H
#define DATABASE_H

#include <QtSql>
#include <string>
#include "todo.h"
#include "reminder.h"
extern QSqlDatabase DB;

void openDB();
void closeDB();
void createTables();
void addTodo(Todo* newTodo);
std::vector<Todo*> getTodos();
void deleteTodo(int id);
void editTodo(Todo *td);
void updateStatus(int id,std::string s);
std::vector<Reminder*> getReminders(QString datetime);
void deleteReminder(int id, QString datetime);
class Database
{
public:
    Database();
};

#endif // DATABASE_H
