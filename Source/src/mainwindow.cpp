#include "../headers/mainwindow.h"
#include "../ui/ui_mainwindow.h"
#include <iostream>
#include "../headers/add_todo.h"
#include "../headers/edit_todo.h"
#include "../headers/history.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_pushButton_2_clicked()
{
    //Add Todo Button
    Add_Todo *add_todo = new Add_Todo();
    add_todo->setWindowTitle("Add Todo");
    add_todo->show();
}


void MainWindow::on_pushButton_clicked()
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

