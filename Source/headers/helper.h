#ifndef HELPER_H
#define HELPER_H

#include <string>
#include <QTableView>
#include "reminder.h"

void replace( std::string& s, std::string const& toReplace, std::string const& replaceWith);
void refreshTodos(QTableView *tv);
std::string getCommand(Reminder *r);

#endif // HELPER_H
