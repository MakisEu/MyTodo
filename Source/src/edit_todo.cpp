#include "../headers/edit_todo.h"
#include "../ui/ui_edit_todo.h"

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

void Edit_Todo::on_pushButton_3_clicked()
{
    //Cancel Button
        close();
}


void Edit_Todo::on_pushButton_4_clicked()
{
    //Edit Todo Button
}

