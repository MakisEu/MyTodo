#include "../headers/edit_todo.h"
#include "../ui/ui_edit_todo.h"
#include "../headers/todo.h"
#include "../headers/control_unit.h"
#include "../headers/helper.h"

#include <QMessageBox>

/*
 * Constructor sets up the GUI
*/
Edit_Todo::Edit_Todo(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Edit_Todo)
{
    ui->setupUi(this);
}
/*
 * Deletes the window created from .ui
*/
Edit_Todo::~Edit_Todo()
{
    delete ui;
}
/*
 * Takes the todo table pointer from the main window and stores it for later usage
*/
void Edit_Todo::passTable(QAbstractItemModel * p){
    tableView=p;
}
/*
 * Takes the todo that will be edited and sets the values of the fields as the values of the todo
*/
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
    ui->comboBoxTags->setCurrentIndex(ui->comboBoxTags->findText(QString::fromStdString(td->getTag())));
}
/*
 * Closes the window
*/
void Edit_Todo::on_pushButton_3_clicked()
{
    //Cancel Button
    close();
}

/*
 * Checks if the user inputed values are valid, and if they are, creates a todo with these values and callw the method EditTodo
 * of ControlUnit and refreshes the table of todos. If the values are invalid, it informs the user
*/
void Edit_Todo::on_pushButton_4_clicked()
{
    //Edit Todo Button
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
            Todo *td=new Todo(name.toStdString(),startDate.toStdString(),endDate.toStdString(),"",id,tag.toStdString());
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
    else{
        QMessageBox::critical(this, "Name is too long", "The name of the Todo exceeds 150 characters!");
    }

}

