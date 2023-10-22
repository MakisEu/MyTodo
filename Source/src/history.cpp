#include "../headers/history.h"
#include "../ui/ui_history.h"

#include "../headers/control_unit.h"
#include "../headers/todo.h"
#include "../headers/control_unit.h"
#include "../headers/database.h"
#include <string>
#include <fstream>


/*
 * Constructor sets up the GUI and loads the history
*/
History::History(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::History)
{
    ui->setupUi(this);
    this->setAttribute( Qt::WA_QuitOnClose, false );
    ui->listWidget->setWordWrap(true);
    loadHistory();
}

/*
 * calls the getStringTodos and getPastTodos methods of ControlUnit
 * and sets the values of the list with the vectors of string that was returned
 *
*/
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


/*
 * Deletes the window created from .ui
*/
History::~History()
{
    delete ui;
}
/*
 * Clears the history file's past todos
*/
void History::on_pushButton_clicked()
{
    //Clear History Button
    std::ofstream fout;
    fout.open("History.txt",std::ios::trunc | std::ios::out);
    fout.close();
    ui->listWidget->clear();
    loadHistory();

}



