#ifndef ADD_TODO_H
#define ADD_TODO_H

#include <QWidget>
#include <QSqlQueryModel>

namespace Ui {
class Add_Todo;
}
/*
 * Add_todo is the class that interacts with the window that shows up when the user click on the Add Todo button
*/
class Add_Todo : public QWidget
{
    Q_OBJECT

public:
    /*
     * Consttuctor for the window
    */
    explicit Add_Todo(QWidget *parent = nullptr);
    /*
     * Method that passes the table of Todoes from the main window into this window
    */
    void passTable(QAbstractItemModel *p);
    /*
     * Destructor for the window
    */
    ~Add_Todo();

private slots:
    /*
     * Actions taken when the Cancel button is pressed
    */
    void on_pushButton_3_clicked();

    /*
     * Actions taken when the Add Todo button is pressed
    */
    void on_pushButton_4_clicked();

private:
    /*
     * Window created from the .ui file
    */
    Ui::Add_Todo *ui;
    /*
     * The table of todos
    */
    QAbstractItemModel* tableView;
};

#endif // ADD_TODO_H
