#ifndef HELPER_H
#define HELPER_H

#include <string>
#include <QSqlQueryModel>
#include "reminder.h"

/*
 * Replaces the sequence toReplace in the string s with the sequence replaceWith
*/
void replace( std::string& s, std::string const& toReplace, std::string const& replaceWith);
/*
 * Refreshes the Todo table of the main window
*/
void refreshTodos(QAbstractItemModel *model);
/*
 *  Return the command to run in the console to send notification
*/
std::string getCommand(Reminder *r);

#endif // HELPER_H
