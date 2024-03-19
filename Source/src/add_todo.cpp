#include "../headers/add_todo.h"
#include "../ui/ui_add_todo.h"
#include "../headers/mainwindow.h"
#include "../headers/helper.h"
#include "../headers/control_unit.h"
#include <string>
#include <QTableView>
#include <QMessageBox>


/*
 * Constructor sets up the GUI and sets the default values of the timedate fields
*/
Add_Todo::Add_Todo(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Add_Todo)
{
    ui->setupUi(this);
    QDateTime date = QDateTime::currentDateTime();
    date=date.addSecs(60);
    ui->dateTimeEdit_3->setDateTime(date);
    date=date.addSecs(60*60*2);
    ui->dateTimeEdit_4->setDateTime(date);

}

/*
 * Deletes the window created from .ui
*/
Add_Todo::~Add_Todo()
{

    delete ui;
}
/*
 * Takes the todo table pointer from the main window and stores it for later usage
*/
void Add_Todo::passTable(QAbstractItemModel * p){
    tableView=p;
}
/*
 * Closes the window
*/
void Add_Todo::on_pushButton_3_clicked()
{
    //Cancel Button

    close();
}

/*
 * Checks if the user inputed values are valid, and if they are, calls the method AddTodo
 * of ControlUnit and refreshes the table of todos. If the values are invalid, it informs the user
*/
void Add_Todo::on_pushButton_4_clicked()
{
    //Add Todo Button
    QString name=ui->plainTextEdit_2->toPlainText();
    QString startDate=ui->dateTimeEdit_3->text();
    QString endDate=ui->dateTimeEdit_4->text();
    QString tag=ui->comboBoxTags->currentText();
    QDateTime date = QDateTime::currentDateTime();


    QDateTime start=QDateTime::fromString(startDate,"dd/MM/yyyy hh:mm");
    QDateTime end=QDateTime::fromString(endDate,"dd/MM/yyyy hh:mm");
    if (name.length()<=150){
    if (date.secsTo(start)>=0 && date.secsTo(end)>0){
        if (start.secsTo(end)>0){
    ControlUnit *cu  =  new ControlUnit();
    QString formattedTime = date.toString("dd/MM/yyyy hh:mm");
    cu->AddTodo(name.toStdString(),startDate.toStdString(),endDate.toStdString(),formattedTime.toStdString(),tag.toStdString());
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
    else{
    QMessageBox::critical(this, "Name is too long", "The name of the Todo exceeds 150 characters!");
    }

}

