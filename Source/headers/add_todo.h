#ifndef ADD_TODO_H
#define ADD_TODO_H

#include <QWidget>
#include <QTableView>

namespace Ui {
class Add_Todo;
}

class Add_Todo : public QWidget
{
    Q_OBJECT

public:
    explicit Add_Todo(QWidget *parent = nullptr);
    //Add_Todo(QWidget *parent,QWidget *p);
    void passTable(QTableView *p);
    ~Add_Todo();

private slots:
    void on_pushButton_3_clicked();

    void on_pushButton_4_clicked();

private:
    Ui::Add_Todo *ui;
    int nextId;
    QTableView* tableView;
};

#endif // ADD_TODO_H
