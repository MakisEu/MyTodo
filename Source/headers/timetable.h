#ifndef TIMETABLE_H
#define TIMETABLE_H

#include <QWidget>
#include <list>
#include "todo.h"

namespace Ui {
class TimeTable;
}

class TimeTable : public QWidget
{
    Q_OBJECT

public:
    explicit TimeTable(QWidget *parent = nullptr);
    ~TimeTable();
    void CreateColumns();
    //void refreshTimetable(QString date);
    QString getCellData(std::list<Todo>& s,QString period);

private:
    Ui::TimeTable *ui;
    //QString weekStart,weekEnd;
    //int testRefreshButton=4;
    void populateColumn(int row,int column, QString date, std::list<Todo>& allTodoOfTheDay);
    QString getHour(int row);
};

#endif // TIMETABLE_H
