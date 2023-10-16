#ifndef EDIT_TODO_H
#define EDIT_TODO_H

#include <QWidget>
#include <QTableView>
#include "../headers/todo.h"
namespace Ui {
class Edit_Todo;
}

class Edit_Todo : public QWidget
{
    Q_OBJECT

public:
    explicit Edit_Todo(QWidget *parent = nullptr);
    void setValues(Todo *td);
    void passTable(QTableView *p);

    ~Edit_Todo();

private slots:
    void on_pushButton_3_clicked();

    void on_pushButton_4_clicked();

private:
    Ui::Edit_Todo *ui;
    QTableView* tableView;
    int id;

};

#endif // EDIT_TODO_H
