#include "../headers/mainwindow.h"
#include "../ui/ui_mainwindow.h"
#include <iostream>
#include "../headers/add_todo.h"
#include "../headers/database.h"
#include "../headers/edit_todo.h"
#include "../headers/history.h"
#include "../headers/helper.h"

#include <QMainWindow>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{

    openDB();
    createTables();
    ui->setupUi(this);
    ui->tableView->setWordWrap(true);
    //ui->tableView->setModel(QAbstractItemView::SingleSelection);
    refreshTodos(ui->tableView);
}

MainWindow::~MainWindow()
{
    closeDB();
    delete ui;
}


void MainWindow::on_pushButton_2_clicked()
{
    //Add Todo Button
    Add_Todo *add_todo = new Add_Todo();
    add_todo->setWindowTitle("Add Todo");
    add_todo->setWindowModality(Qt::ApplicationModal);
    refreshTodos(ui->tableView);
    add_todo->show();
    add_todo->test(ui->tableView);
}


void MainWindow::on_pushButton_1_clicked()
{
    //Edit Todo Button
    Edit_Todo *edit_todo = new Edit_Todo();
    edit_todo->setWindowTitle("Edit Todo");
    edit_todo->show();

}


void MainWindow::on_pushButton_5_clicked()
{
    //History Button
    History *history = new History();
    history->setWindowTitle("History");
    history->show();
}


void MainWindow::on_pushButton_3_clicked()
{
    //Delete Todo Button
}


void MainWindow::on_pushButton_4_clicked()
{
    //Mark as completed Button
}





