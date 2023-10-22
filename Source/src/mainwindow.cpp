#include "../headers/mainwindow.h"
#include "../ui/ui_mainwindow.h"
#include "../headers/add_todo.h"
#include "../headers/database.h"
#include "../headers/edit_todo.h"
#include "../headers/history.h"
#include "../headers/helper.h"
#include "../headers/control_unit.h"
#include "../headers/reminder.h"

#include <QMainWindow>
#include <QMessageBox>
#include <iostream>
#include <string>
#include <QMap>
#include <QErrorMessage>


/*
 * Sets up the window, refreshes the todo table and starts a Qtimer every 1 second
*/
MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{

    openDB();
    createTables();
    ui->setupUi(this);
    ui->tableView->setWordWrap(true);
    ui->tableView->setSelectionBehavior(QAbstractItemView::SelectRows);
    //ui->tableView->setModel(QAbstractItemView::SingleSelection);
    refreshTodos(ui->tableView);
    QTimer *timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), this, SLOT(CheckNotify()));
    timer->start(1000);
}
/*
 * Destructor for the window that closes any open History window, closes the database and the application
*/
MainWindow::~MainWindow()
{
    delete hist;
    closeDB();
    delete ui;
}

/*
 * Creates the Add_Todo window and passes the todo table to it
*/
void MainWindow::on_pushButton_2_clicked()
{
    //Add Todo Button
    Add_Todo *add_todo = new Add_Todo();
    add_todo->setWindowTitle("Add Todo");
    add_todo->setWindowModality(Qt::ApplicationModal);
    ui->tableView->setSelectionBehavior(QAbstractItemView::SelectRows);
    ui->tableView->setSelectionMode(QAbstractItemView::SingleSelection);
    refreshTodos(ui->tableView);
    add_todo->show();
    add_todo->passTable(ui->tableView);
}

/*
 * Creates the Edit_Todo window, passes the todo table to it and also passes the todo that will be edited.
 * If no todo is selected, it informs the user
*/
void MainWindow::on_pushButton_1_clicked()
{
    //Edit Todo Button

    QItemSelectionModel *select=ui->tableView->selectionModel();
    int id=select->selectedRows(0).value(0).data().toInt();
    std::string name,sd,ed,dc,stat;
    name=select->selectedRows(1).value(0).data().toString().toStdString();
    stat=select->selectedRows(2).value(0).data().toString().toStdString();
    sd=select->selectedRows(3).value(0).data().toString().toStdString();
    ed=select->selectedRows(4).value(0).data().toString().toStdString();
    dc=select->selectedRows(5).value(0).data().toString().toStdString();

    if (!(id==0 && name=="" && stat=="" && ed=="" && sd=="" && dc=="")){
    Edit_Todo *edit_todo = new Edit_Todo();
    edit_todo->setWindowTitle("Edit Todo");
    edit_todo->passTable(ui->tableView);
    edit_todo->setWindowModality(Qt::ApplicationModal);


    Todo *td=new Todo(name,sd,ed,dc,id);
    edit_todo->setValues(td);
    delete td;

    edit_todo->show();
    }
    else{
    QMessageBox::critical(this, "No Todo Selected", "Please select Todo to edit!");
    }

}

/*
 * Creates the History window and passes the todo table to it
*/
void MainWindow::on_pushButton_5_clicked()
{
    //History Button
    delete hist;
    hist = new History();
    hist->setWindowTitle("History");
    hist->show();
}

/*
 * Delete the todo that is selected (after the user confirms the deletion) from the database and refreshes the todo table
*/
void MainWindow::on_pushButton_3_clicked()
{
    //Delete Todo Button
    /*QItemSelectionModel *select=ui->tableView->selectionModel();
    QString s;
    s=select->selectedRows(0).value(0).data().toString();
    s=select->selectedRows(1).value(0).data().toString();
    s=select->selectedRows(2).value(0).data().toString();
    s=select->selectedRows(3).value(0).data().toString();
    */

    QItemSelectionModel *select=ui->tableView->selectionModel();
    int id=select->selectedRows(0).value(0).data().toInt();
    std::string name,sd,ed,dc,stat;
    name=select->selectedRows(1).value(0).data().toString().toStdString();
    stat=select->selectedRows(2).value(0).data().toString().toStdString();
    sd=select->selectedRows(3).value(0).data().toString().toStdString();
    ed=select->selectedRows(4).value(0).data().toString().toStdString();
    dc=select->selectedRows(5).value(0).data().toString().toStdString();

    if (!(id==0 && name=="" && stat=="" && ed=="" && sd=="" && dc=="")){
    QMessageBox::StandardButton reply;
    reply = QMessageBox::question(this, "Delete Todo", "Are you sure you want to delete the selected Todo?",
                                  QMessageBox::Yes|QMessageBox::No);
    if (reply == QMessageBox::Yes){
    ControlUnit *cu=new ControlUnit();

    Todo *td=new Todo(name,sd,ed,dc,id);
    td->updateStatus(stat);
    cu->DeleteTodo(td);
    delete cu;
    delete td;
    refreshTodos(ui->tableView);
    }
    }
    else{
    QMessageBox::critical(this, "No Todo Selected", "Please select Todo to delete!");

    }

}

/*
 * Sets the selected Todo as Completed and removes it from the database
*/
void MainWindow::on_pushButton_4_clicked()
{
    //Mark as completed Button
    QItemSelectionModel *select=ui->tableView->selectionModel();
    int id=select->selectedRows(0).value(0).data().toInt();
    std::string name,sd,ed,dc,stat;
    name=select->selectedRows(1).value(0).data().toString().toStdString();
    stat=select->selectedRows(2).value(0).data().toString().toStdString();
    sd=select->selectedRows(3).value(0).data().toString().toStdString();
    ed=select->selectedRows(4).value(0).data().toString().toStdString();
    dc=select->selectedRows(5).value(0).data().toString().toStdString();
    if (!(id==0 && name=="" && stat=="" && ed=="" && sd=="" && dc=="")){
    ControlUnit *cu=new ControlUnit();

    Todo *td=new Todo(name,sd,ed,dc,id);
    cu->UpdateTodoStatus(td,"Completed");
    delete td;
    delete cu;
    refreshTodos(ui->tableView);
    }
    else{
    QMessageBox::critical(this, "No Todo Selected", "Please select Todo to Complete!");

    }
}
/*
 * Checks every time it is called if there is any reminder for the current datetime and if there are, send notifications
*/
void MainWindow::CheckNotify(){
    QDateTime date = QDateTime::currentDateTime();
    QString formattedTime = date.toString("dd/MM/yyyy hh:mm");
    std::vector<Reminder*> v=getReminders(formattedTime);
    std::string s;
    if (!v.empty()){
        for(std::vector<Reminder*>::iterator it = v.begin() ;it != v.end() ;++it){
            std::system(getCommand(*it).c_str());
            deleteReminder((*it)->todoId,formattedTime);
            updateStatus((*it)->todoId,"In Progress");
        }
        refreshTodos(ui->tableView);
    }

}




