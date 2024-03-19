#include "../headers/mainwindow.h"
#include "../ui/ui_mainwindow.h"
#include "../headers/add_todo.h"
#include "../headers/database.h"
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

    hist=nullptr;
    edit_todo=nullptr;
    add_todo=nullptr;
    openDB();
    createTables();
    ui->setupUi(this);
    timetable=nullptr;
    ui->tabWidget->addTab(new QWidget(this),"Timetable");
    //delete timetable;

    ui->tableView->setWordWrap(true);
    ui->tableView->setSelectionBehavior(QAbstractItemView::SelectRows);
    ui->tableView->setModel(new QSqlQueryModel());
    //ui->tableView->setModel(QAbstractItemView::SingleSelection);
    refreshTodos(ui->tableView->model());

    ui->tableView->setColumnWidth(0,20);
    ui->tableView->setColumnWidth(1,300);
    ui->tableView->setColumnWidth(2,100);
    ui->tableView->setColumnWidth(3,125);
    ui->tableView->setColumnWidth(4,125);
    ui->tableView->setColumnWidth(5,125);
    ui->tableView->setColumnWidth(6,125);

    QTimer *timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), this, SLOT(CheckNotify()));
    timer->start(1000);
}
/*
 * Destructor for the window that closes any open History window, closes the database and the application
*/
MainWindow::~MainWindow()
{
    delete ui->tableView->model();
    delete edit_todo;
    delete add_todo;
    delete timetable;
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
    delete add_todo;
    add_todo = new Add_Todo();
    add_todo->setWindowTitle("Add Todo");
    add_todo->setWindowModality(Qt::ApplicationModal);
    ui->tableView->setSelectionBehavior(QAbstractItemView::SelectRows);
    ui->tableView->setSelectionMode(QAbstractItemView::SingleSelection);
    refreshTodos(ui->tableView->model());
    add_todo->show();
    add_todo->passTable(ui->tableView->model());
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
    std::string name,sd,ed,dc,stat,tag;
    name=select->selectedRows(1).value(0).data().toString().toStdString();
    stat=select->selectedRows(2).value(0).data().toString().toStdString();
    sd=select->selectedRows(3).value(0).data().toString().toStdString();
    ed=select->selectedRows(4).value(0).data().toString().toStdString();
    dc=select->selectedRows(5).value(0).data().toString().toStdString();
    tag=select->selectedRows(6).value(0).data().toString().toStdString();

    if (!(id==0 && name=="" && stat=="" && ed=="" && sd=="" && dc=="")){
    delete edit_todo;
    edit_todo = new Edit_Todo();
    edit_todo->setWindowTitle("Edit Todo");
    edit_todo->passTable(ui->tableView->model());
    edit_todo->setWindowModality(Qt::ApplicationModal);


    Todo *td=new Todo(name,sd,ed,dc,id,tag);
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

    Todo *td=new Todo(name,sd,ed,dc,id,"");
    td->updateStatus(stat);
    cu->DeleteTodo(td);
    delete cu;
    delete td;
    refreshTodos(ui->tableView->model());
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
    std::string name,sd,ed,dc,stat,tag;
    name=select->selectedRows(1).value(0).data().toString().toStdString();
    stat=select->selectedRows(2).value(0).data().toString().toStdString();
    sd=select->selectedRows(3).value(0).data().toString().toStdString();
    ed=select->selectedRows(4).value(0).data().toString().toStdString();
    dc=select->selectedRows(5).value(0).data().toString().toStdString();
    tag=select->selectedRows(6).value(0).data().toString().toStdString();
    if (!(id==0 && name=="" && stat=="" && ed=="" && sd=="" && dc=="")){
    ControlUnit *cu=new ControlUnit();

    Todo *td=new Todo(name,sd,ed,dc,id,tag);
    cu->UpdateTodoStatus(td,"Completed");
    delete td;
    delete cu;
    refreshTodos(ui->tableView->model());
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
    timetable;
    std::vector<Reminder*> v=getReminders(formattedTime);
    std::string s;
    if (!v.empty()){
        std::string messagesStart="";
        std::string messagesEnd="";
        for(std::vector<Reminder*>::iterator it = v.begin() ;it != v.end() ;++it){
            //std::system(getCommand(*it).c_str());
            if ((*it)->message.contains("started")){
                messagesStart=messagesStart+(*it)->message.toStdString()+"\n";
            }
            else{
                messagesEnd=messagesEnd+(*it)->message.toStdString()+"\n";
            }
            deleteReminder((*it)->todoId,formattedTime);
            updateStatus((*it)->todoId,"In Progress");
            delete (*it);
        }
        if (messagesStart.length()>2){
            std::string command="notify-send 'Todo Has Started' \""+messagesStart+"\"";
            system(command.c_str());
        }
        if (messagesEnd.length()>2){
            std::string command="notify-send 'Todo Has Expired' \""+messagesEnd+"\"";
            system(command.c_str());
        }
        refreshTodos(ui->tableView->model());
    }

}





void MainWindow::on_pushButton_clicked()
{
    //Daily Todos:
    QMessageBox::StandardButton reply;
    reply = QMessageBox::question(this, "Renew Old Daily Todos", "Are you sure you want to delete and restart the Daily Todos?",
                                  QMessageBox::Yes|QMessageBox::No);
    if (reply == QMessageBox::Yes){
    QDateTime date = QDateTime::currentDateTime();
    std::string suffix="(Daily)*";
    //In Progress
    std::string start = date.toString("dd/MM/yyyy hh:mm").toStdString();
    date.setTime(QTime(23, 59, 0));
    std::string end = date.toString("dd/MM/yyyy hh:mm").toStdString();
    date.setTime(QTime(0, 0, 0));
    std::string created = date.toString("dd/MM/yyyy hh:mm").toStdString();


    removeDaily(suffix);
    ControlUnit* cu=new ControlUnit();
    //Do 1 LeetCode:
    std::string taskName="Solve 1 LeetCode Problem";
    cu->AddTodo(taskName+suffix,start,end,created,"Education");
    //Study for Uni:
    taskName="Study for at least 30 minutes";
    cu->AddTodo(taskName+suffix,start,end,created,"Education");
    //Work on web dev:
    taskName="Work on learning Web Development";
    cu->AddTodo(taskName+suffix,start,end,created,"Education");
    //Study ML:
    taskName="Apply machine learning on 1 dataset";
    cu->AddTodo(taskName+suffix,start,end,created,"Education");
    //Work on projects:
    taskName="Work on an existing project";
    cu->AddTodo(taskName+suffix,start,end,created,"Education");
    //Study for owed subjects:
    taskName="Study Applied Mathematics";
    cu->AddTodo(taskName+suffix,start,end,created,"Education");
    delete cu;
    refreshTodos(ui->tableView->model());
    }
}


void MainWindow::on_tabWidget_tabBarClicked(int index)
{
    if (index==1){
        timetable=new TimeTable(this);
        delete ui->tabWidget->widget(1);
        ui->tabWidget->removeTab(1);
        ui->tabWidget->addTab(timetable,"Timetable");
        delete ui->tableView->model();
        ui->tableView->setModel(nullptr);
    }
    else if (index==0){
        ui->tabWidget->removeTab(1);
        delete timetable;
        timetable=nullptr;
        ui->tabWidget->addTab(new QWidget(),"Timetable");
        ui->tableView->setModel(new QSqlQueryModel());
        refreshTodos(ui->tableView->model());

    }
}

