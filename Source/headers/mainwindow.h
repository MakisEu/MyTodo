#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include "../headers/add_todo.h"
#include "../headers/database.h"
#include "../headers/history.h"
#include "../headers/reminder.h"
#include <QMainWindow>
#include <QMap>
#include <QDateTime>


QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT


public:
    MainWindow(QWidget *parent = nullptr);
    //void refreshTodos();
    ~MainWindow();
private slots:
    void on_pushButton_2_clicked();

    void on_pushButton_1_clicked();

    void on_pushButton_5_clicked();

    void on_pushButton_3_clicked();

    void on_pushButton_4_clicked();

    void CheckNotify();



private:
    Ui::MainWindow *ui;
    History *hist;
    QMap <QDateTime,Reminder> d;
    //Add_Todo* add_todo;
};
#endif // MAINWINDOW_H
