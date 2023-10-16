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
    this->setAttribute( Qt::WA_QuitOnClose, false );
    ControlUnit *cu=new ControlUnit();
    std::vector<std::string> vec=cu->getStringTodos();
    QString qs;
    ui->listWidget->setWordWrap(true);
    ui->listWidget->addItem("Current Todo:\n");
    for (std::vector<std::string>::iterator i = vec.begin(); i != vec.end(); ++i)
    {
        qs=QString::fromStdString(*i);
        //qs.guh
        //items<< s;
        ui->listWidget->addItem(qs);
    }
    ui->listWidget->addItem("\nOld Todo:\n");
    vec=cu->getPastHistory();
    for (std::vector<std::string>::iterator i = vec.begin(); i != vec.end(); ++i)
    {
        qs=QString::fromStdString(*i);
        //qs.guh
        //items<< s;
        ui->listWidget->addItem(qs);
    }

    delete cu;

}

History::~History()
{
    delete ui;
}

void History::on_pushButton_clicked()
{
    //Clear History Button
}

