#ifndef HELPER_H
#define HELPER_H

#include <string>
#include <QTableView>

void replace( std::string& s, std::string const& toReplace, std::string const& replaceWith);
void refreshTodos(QTableView *tv);
class helper
{
public:
    helper();
    void refreshTodos(QTableView *tv);
};

#endif // HELPER_H
