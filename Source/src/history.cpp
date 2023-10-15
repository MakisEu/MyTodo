#include "../headers/history.h"
#include "../ui/ui_history.h"

#include "../headers/control_unit.h"
#include "../headers/todo.h"
#include "../headers/control_unit.h"
#include "../headers/database.h"
#include <string>

History::History(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::History)
{
    ui->setupUi(this);
    ControlUnit *cu=new ControlUnit();
    std::vector<Todo*> vec=getTodos();
    std::string s;
    QString qs;
    ui->listWidget->setWordWrap(true);
    ui->listWidget->addItem("Current Todo:\n");
    for (std::vector<Todo*>::iterator i = vec.begin(); i != vec.end(); ++i)
    {
        s=(*i)->getName()+"  "+(*i)->getStartDate()+"  "+(*i)->getEndDate()+"  "+(*i)->getDateCreated()+"  "+(*i)->getStatus();
        qs=QString::fromStdString(s);
        //qs.guh
        //items<< s;
        ui->listWidget->addItem(qs);
    }
    ui->listWidget->addItem("\nOld Todo:\n");

}

History::~History()
{
    delete ui;
}

void History::on_pushButton_clicked()
{
    //Clear History Button
}

