#include "history.h"
#include "ui_history.h"

#include "control_unit.h"
#include "todo.h"
#include "control_unit.h"
#include "database.h"
#include <string>
#include <fstream>
#include <QStandardItemModel>

History::History(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::History)
{
    ui->setupUi(this);
    this->setAttribute( Qt::WA_QuitOnClose, false );
    ui->listWidget->setWordWrap(true);
    loadHistory();
}
void History::loadHistory(){

    ControlUnit *cu=new ControlUnit();
    std::vector<std::string> vec=cu->getStringTodos();
    QString qs;
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
    std::ofstream fout;
    fout.open("History.txt",std::ios::trunc | std::ios::out);
    fout.close();
    ui->listWidget->clear();
    loadHistory();

}




