#ifndef EDIT_TODO_H
#define EDIT_TODO_H

#include <QWidget>
#include <QTableView>
#include "../headers/todo.h"
namespace Ui {
class Edit_Todo;
}

/*
 * Edit_Todo is the class that interacts with the window that shows up when the user click on the Edit Todo button
*/
class Edit_Todo : public QWidget
{
    Q_OBJECT

public:
    /*
     * Consttuctor for the window
    */
    explicit Edit_Todo(QWidget *parent = nullptr);
    /*
     * Method that sets the default values of the todo, which are the values the toto had
    */
    void setValues(Todo *td);
    /*
     * Method that passes the table of Todoes from the main window into this window
    */
    void passTable(QTableView *p);
    /*
     * Destructor for the window
    */
    ~Edit_Todo();

private slots:
    /*
     * Actions taken when the Cancel button is pressed
    */
    void on_pushButton_3_clicked();
    /*
     * Actions taken when the Edit Todo button is pressed
    */
    void on_pushButton_4_clicked();

private:
    /*
     * Window created from the .ui file
    */
    Ui::Edit_Todo *ui;
    /*
     * The table of todos
    */
    QTableView* tableView;
    /*
     * The id of the todo that is beign edited
    */
    int id;

};

#endif // EDIT_TODO_H
