#ifndef DATABASE_H
#define DATABASE_H

#include <QtSql>
#include <string>
#include "todo.h"
#include "reminder.h"
#include <list>
extern QSqlDatabase DB;

/*
 * Opens/Creates the database
*/
void openDB();
/*
 * Closes the database
*/
void closeDB();
/*
 * Creates the tables of todos and reminders
*/
void createTables();
/*
 * Add a todo to the database
*/
void addTodo(Todo* newTodo);
/*
 * Returns all the todos of the database as a vector
*/
std::vector<Todo*> getTodos();
/*
 * Deletes the todo with a specific id from the database
*/
void deleteTodo(int id);
/*
 * Edits an existing todo in the database
*/
void editTodo(Todo *td);
/*
 * Updates the status of the todo with a specific id
*/
void updateStatus(int id,std::string s);
/*
 * Returns all the reminders in the database with a specific datetime
*/
std::vector<Reminder*> getReminders(QString datetime);
/*
 * Deletes a reminder with a specfic datetime and Todo id
*/
void deleteReminder(int id, QString datetime);

void removeDaily(std::string suffix);
std::list<Todo> getTodoOfTheDay(QString date);

#endif // DATABASE_H
