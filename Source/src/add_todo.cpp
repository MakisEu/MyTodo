#include "../headers/add_todo.h"
#include "../ui/ui_add_todo.h"

Add_Todo::Add_Todo(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Add_Todo)
{
    ui->setupUi(this);
}

Add_Todo::~Add_Todo()
{
    delete ui;
}

void Add_Todo::on_pushButton_3_clicked()
{
    //Cancel Button
    close();

}


void Add_Todo::on_pushButton_4_clicked()
{
    //Add Todo Button
}

