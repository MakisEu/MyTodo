#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include "../headers/add_todo.h"
#include "../headers/database.h"
#include "../headers/history.h"
#include "../headers/edit_todo.h"
#include "../headers/reminder.h"
#include "../headers/timetable.h"
#include <QMainWindow>
#include <QMap>
#include <QDateTime>


QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

/*
 * MainWindow is the the main window of the application
*/
class MainWindow : public QMainWindow
{
    Q_OBJECT


public:
    /*
     * Consttuctor for the window
    */
    MainWindow(QWidget *parent = nullptr);
    /*
     * Destructor for the window
    */
    ~MainWindow();
private slots:
    /*
     * Actions taken when the Add Todo button is pressed
    */
    void on_pushButton_2_clicked();
    /*
     * Actions taken when the Edit Todo button is pressed
    */
    void on_pushButton_1_clicked();
    /*
     * Actions taken when the History button is pressed
    */
    void on_pushButton_5_clicked();
    /*
     * Actions taken when the Delete Todo button is pressed
    */
    void on_pushButton_3_clicked();
    /*
     * Actions taken when the Mark as completed button is pressed
    */
    void on_pushButton_4_clicked();
    /*
     * Actions taken every time the QTimer times out(every 1 second)
    */
    void CheckNotify();



    void on_pushButton_clicked();

    void on_tabWidget_tabBarClicked(int index);

private:
    /*
     * Window created from the .ui file
    */
    Ui::MainWindow *ui;
    /*
     * The history window
    */
    History *hist;
    Edit_Todo *edit_todo;
    Add_Todo *add_todo;
    TimeTable *timetable;
};
#endif // MAINWINDOW_H
