#ifndef EDIT_TODO_H
#define EDIT_TODO_H

#include <QWidget>

namespace Ui {
class edit_todo;
}

class edit_todo : public QWidget
{
    Q_OBJECT

public:
    explicit edit_todo(QWidget *parent = nullptr);
    ~edit_todo();

private:
    Ui::edit_todo *ui;
};

#endif // EDIT_TODO_H
