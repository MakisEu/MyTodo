#include "../headers/edit_todo.h"
#include "../ui/ui_edit_todo.h"
#include "../headers/todo.h"
#include "../headers/control_unit.h"
#include "../headers/helper.h"

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
    ControlUnit *cu  =  new ControlUnit();
    Todo *td=new Todo(name.toStdString(),startDate.toStdString(),endDate.toStdString(),"",id);
    cu->EditTodo(td);
    delete td;
    delete cu;
    refreshTodos(tableView);
    close();

}

