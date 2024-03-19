#include "../headers/timetable.h"
#include "../headers/database.h"
#include "../ui/ui_timetable.h"
#include <QDateTime>
#include <QStandardItemModel>

TimeTable::TimeTable(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::TimeTable)
{
    ui->setupUi(this);
    ui->Table->setModel(new QStandardItemModel(12,7));
    this->CreateColumns();
}

TimeTable::~TimeTable()
{
    delete ui->Table->model();
    delete ui;
}

void TimeTable::CreateColumns(){
    QStringList columns, rows;

    QDate startDate = QDate::currentDate().addDays(-3);
    //weekStart=startDate.addDays(1).toString("dd/MM/yyyy");
    //weekStart+=" 00:00";

    for (int i=0;i<7;i++){
        QString date=startDate.addDays(i).toString("dd/MM");
        columns << date;

        date=startDate.addDays(i).toString("dd/MM/yyyy");
        std::list<Todo> allTodoOfTheDay=getTodoOfTheDay(date);
        for (int j=0;j<24 && !allTodoOfTheDay.empty();j=j+2){
            this->populateColumn(j,i,date,allTodoOfTheDay);
        }
    }
    //weekEnd=startDate.toString("dd/MM/yyyy")+" 23:59";
    qobject_cast<QStandardItemModel*>(ui->Table->model())->setHorizontalHeaderLabels(columns);
    for (int i=0;i<24;i+=2){
        rows<< this->getHour(i);
    }
    qobject_cast<QStandardItemModel*>(ui->Table->model())->setVerticalHeaderLabels(rows);
    ui->Table->resizeRowsToContents();
    ui->Table->resizeColumnsToContents();
    //ui->tableWidget->setEditTriggers(QAbstractItemView::NoEditTriggers);

}

QString TimeTable::getHour(int row){
    QString hours;
    if (row<10){
        hours=" 0"+QString::number(row);
    }
    else{
        hours=" "+QString::number(row);
    }
    hours+=":00 -\n";
    row+=2;
    if (row<10){
        hours+=" 0"+QString::number(row);
    }
    else{
        hours+=" "+QString::number(row);
    }
    hours=hours+":00";
    return hours;
}

void TimeTable::populateColumn(int row,int column, QString date, std::list<Todo>& allTodoOfTheDay){
    QString hours,limit;
    if (row<10){
        hours=" 0"+QString::number(row);
        if (row<9){
            limit=" 0"+QString::number(row+1);
        }
        else{
            limit=" "+QString::number(row+1);
        }
    }
    else{
        hours=" "+QString::number(row);
        limit=" "+QString::number(row+1);
    }
    QString cellContent=this->getCellData(allTodoOfTheDay,date+limit);

    ui->Table->model()->setData(ui->Table->model()->index(row/2, column), cellContent);

    /*QTableWidgetItem *pCell = ui->tableWidget->item(row, column);
    if(!pCell)
    {
        pCell = new QTableWidgetItem;
        ui->tableWidget->setItem(row, column, pCell);
    }
    pCell->setText(cellContent);*/
}

QString TimeTable::getCellData(std::list<Todo>& s,QString period){
    QString cellData="";
    int cnt=1;
    std::list<Todo>::iterator i = s.begin();
    while (i != s.end())
    {
        QDateTime Date=QDateTime::fromString(QString::fromStdString(i->getStartDate()),"dd/MM/yyyy hh:mm");
        //Date=QDateTime::fromString(QString::fromStdString((*i)->getEndDate()),"dd/MM/yyyy hh:mm");
        QDateTime upperBound=QDateTime::fromString(period+":59","dd/MM/yyyy hh:mm");
        if (!( Date<=upperBound)){
            return cellData;
        }
        //Other codestuff
        //cellData+=QString::number(cnt++)+QString::fromStdString((*i)->getName())+"\n";
        cellData+=QString::fromStdString(i->getName())+" ("+QString::number(i->getId())+")\n";
        Date=QDateTime::fromString(QString::fromStdString(i->getEndDate()),"dd/MM/yyyy hh:mm");
        if (Date<=upperBound){
            s.erase(i++);
        }
        else{
            ++i;
        }
    }
    return cellData.trimmed();

}

/*void TimeTable::refreshTimetable(QString date){
    //QString date=;//=startDate.addDays(3).toString("dd/MM");
    QStringList newHeaders;
    ui->tableWidget->removeColumn(0);
    ui->tableWidget->insertColumn(6);
    for (int i=0;i<6;i++){
        newHeaders << ui->tableWidget->horizontalHeaderItem(i)->text();
    }

    //date=startDate.addDays(i).toString("dd/MM/yyyy");
    std::list<Todo> allTodoOfTheDay=getTodoOfTheDay(date);
    for (int row=0;row<24;row++){
        this->populateColumn(row,6,date,allTodoOfTheDay);
    }
    date.chop(5);
    newHeaders << date;
    ui->tableWidget->setHorizontalHeaderLabels(newHeaders);
}*/

