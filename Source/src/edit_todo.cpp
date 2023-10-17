#include "../headers/edit_todo.h"
#include "../ui/ui_edit_todo.h"
#include "../headers/todo.h"
#include "../headers/control_unit.h"
#include "../headers/helper.h"

#include <QMessageBox>

Edit_Todo::Edit_Todo(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Edit_Todo)
{
    ui->setupUi(this);
}

Edit_Todo::~Edit_Todo()
{
    delete ui;
}
void Edit_Todo::passTable(QTableView * p){
    tableView=p;
}
void Edit_Todo::setValues(Todo *td){

    //QString sd();
    //QString ed(QString::fromStdString(td->getEndDate()));
    QString s=QString::fromStdString(td->getStartDate());
    QDateTime sd=QDateTime::fromString(s,"dd/MM/yyyy hh:mm");
    ui->dateTimeEdit_3->setDateTime(sd);
    s=QString::fromStdString(td->getEndDate());
    sd=QDateTime::fromString(s,"dd/MM/yyyy hh:mm");
    id=td->getId();
    ui->dateTimeEdit_4->setDateTime(sd);
    ui->plainTextEdit_2->document()->setPlainText(QString::fromStdString(td->getName()));
}

void Edit_Todo::on_pushButton_3_clicked()
{
    //Cancel Button
    close();
}


void Edit_Todo::on_pushButton_4_clicked()
{
    //Edit Todo Button
    QString name=ui->plainTextEdit_2->toPlainText();
    QString startDate=ui->dateTimeEdit_3->text();
    QString endDate=ui->dateTimeEdit_4->text();

    QDateTime date = QDateTime::currentDateTime();
    QDateTime start=QDateTime::fromString(startDate,"dd/MM/yyyy hh:mm");
    QDateTime end=QDateTime::fromString(endDate,"dd/MM/yyyy hh:mm");

    if (date.secsTo(start)>=0 && date.secsTo(end)>0){
        if (start.secsTo(end)>0){
            ControlUnit *cu  =  new ControlUnit();
            Todo *td=new Todo(name.toStdString(),startDate.toStdString(),endDate.toStdString(),"",id);
            cu->EditTodo(td);
            delete td;
            delete cu;
            refreshTodos(tableView);
            close();
        }
        else{
            QMessageBox::critical(this, "Incorrect Date", "Start Date is after End Date!");
        }
    }
    else{
        QMessageBox::critical(this, "Incorrect Date", "Start Date or End Date are set before current date!");
    }

}

