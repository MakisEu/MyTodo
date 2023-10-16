#include "../headers/mainwindow.h"
#include "../ui/ui_mainwindow.h"
#include "../headers/add_todo.h"
#include "../headers/database.h"
#include "../headers/edit_todo.h"
#include "../headers/history.h"
#include "../headers/helper.h"
#include "../headers/control_unit.h"

#include <QMainWindow>
#include <QMessageBox>
#include <iostream>
#include <string>


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
}

MainWindow::~MainWindow()
{
    delete hist;
    closeDB();
    delete ui;
}


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


void MainWindow::on_pushButton_1_clicked()
{
    //Edit Todo Button
    Edit_Todo *edit_todo = new Edit_Todo();
    edit_todo->setWindowTitle("Edit Todo");
    edit_todo->passTable(ui->tableView);
    edit_todo->setWindowModality(Qt::ApplicationModal);
    QItemSelectionModel *select=ui->tableView->selectionModel();
    int id=select->selectedRows(0).value(0).data().toInt();
    std::string name,sd,ed,dc,stat;
    name=select->selectedRows(1).value(0).data().toString().toStdString();
    stat=select->selectedRows(2).value(0).data().toString().toStdString();
    sd=select->selectedRows(3).value(0).data().toString().toStdString();
    ed=select->selectedRows(4).value(0).data().toString().toStdString();
    dc=select->selectedRows(5).value(0).data().toString().toStdString();

    Todo *td=new Todo(name,sd,ed,dc,id);
    edit_todo->setValues(td);
    delete td;

    edit_todo->show();

}


void MainWindow::on_pushButton_5_clicked()
{
    //History Button
    delete hist;
    hist = new History();
    hist->setWindowTitle("History");
    hist->show();
}


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
    QMessageBox::StandardButton reply;
    reply = QMessageBox::question(this, "Delete Todo", "Are you sure you want to delete the selected Todo?",
                                  QMessageBox::Yes|QMessageBox::No);
    if (reply == QMessageBox::Yes){
    QItemSelectionModel *select=ui->tableView->selectionModel();
    int id=select->selectedRows(0).value(0).data().toInt();
    std::string name,sd,ed,dc,stat;
    name=select->selectedRows(1).value(0).data().toString().toStdString();
    stat=select->selectedRows(2).value(0).data().toString().toStdString();
    sd=select->selectedRows(3).value(0).data().toString().toStdString();
    ed=select->selectedRows(4).value(0).data().toString().toStdString();
    dc=select->selectedRows(5).value(0).data().toString().toStdString();
    ControlUnit *cu=new ControlUnit();

    Todo *td=new Todo(name,sd,ed,dc,id);
    td->updateStatus(stat);
    cu->DeleteTodo(td);
    delete cu;
    delete td;
    refreshTodos(ui->tableView);
    }

}


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
    ControlUnit *cu=new ControlUnit();

    Todo *td=new Todo(name,sd,ed,dc,id);
    cu->UpdateTodoStatus(td,"Completed");
    delete td;
    delete cu;
    refreshTodos(ui->tableView);

}






