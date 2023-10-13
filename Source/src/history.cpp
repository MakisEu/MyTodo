#include "../headers/history.h"
#include "../ui/ui_history.h"

History::History(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::History)
{
    ui->setupUi(this);
}

History::~History()
{
    delete ui;
}

void History::on_pushButton_clicked()
{
    //Clear History Button
}

