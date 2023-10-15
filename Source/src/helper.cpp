#include "../headers/helper.h"
#include "../headers/database.h"

#include <string>
#include <QTableView>




void replace(std::string& s, std::string const& toReplace, std::string const& replaceWith){
    std::string buf;
    std::size_t pos = 0;
    std::size_t prevPos;

    // Reserves rough estimate of final size of string.
    buf.reserve(s.size());

    while (true) {
        prevPos = pos;
        pos = s.find(toReplace, pos);
        if (pos == std::string::npos)
            break;
        buf.append(s, prevPos, pos - prevPos);
        buf += replaceWith;
        pos += toReplace.size();
    }

    buf.append(s, prevPos, s.size() - prevPos);
    s.swap(buf);
}

void refreshTodos(QTableView *tv){
    QSqlQueryModel* modal=new QSqlQueryModel();
    QSqlQuery* query=new QSqlQuery(DB);
    query->prepare("SELECT * FROM Todo;");
    query->exec();
    modal->setQuery(std::move(*query));
    delete query;
    tv->setModel(modal);
    int size=tv->width();
    tv->setColumnWidth(0,20);
    tv->setColumnWidth(1,300);
    tv->setColumnWidth(2,100);
    tv->setColumnWidth(3,125);
    tv->setColumnWidth(4,125);
    tv->setColumnWidth(5,125);




}

helper::helper()
{

}
