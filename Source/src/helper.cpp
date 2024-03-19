#include "../headers/helper.h"
#include "../headers/database.h"
#include "../headers/reminder.h"
#include "../headers/database.h"

#include <string>



/*
 * Replaces the sequence toReplace in the string s with the sequence replaceWith
*/
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
/*
 * Inserts every Todo in the table tv and sets custom sizes for each column
*/
void refreshTodos(QAbstractItemModel *model){
    //QSqlQueryModel* modal=new QSqlQueryModel();
    QSqlQuery* query=new QSqlQuery(DB);
    query->prepare("SELECT * FROM Todo;");
    query->exec();
    QSqlQueryModel* sqlmodel = qobject_cast<QSqlQueryModel*>(model);
    if (sqlmodel!=nullptr){
        sqlmodel->clear();
        sqlmodel->setQuery(std::move(*query));
    }
    //modal->setQuery(std::move(*query));
    delete query;
    //delete tv->model();
    //tv->setModel(modal);
    //int size=tv->width();
}
/*
 *  Creates the command to send a notification (os specific -only Linux is supported currently) based on the type of reminder and returns the command
*/
std::string getCommand(Reminder *r){
    std::string s;
    QString title;
    if (r->message.contains("started")){
        title="Todo Has Started";
    }
    else{
        title="Todo Has Expired";
    }
    s="notify-send '"+title.toStdString()+"' \""+r->message.toStdString()+"\"";
    return s;
}

