#ifndef HISTORY_H
#define HISTORY_H

#include <QWidget>

namespace Ui {
class History;
}
/*
 * History is the class that interacts with the window that shows up when the user click on the History button
*/
class History : public QWidget
{
    Q_OBJECT

public:
    /*
     * Consttuctor for the window
    */
    explicit History(QWidget *parent = nullptr);
    /*
     * Destructor for the window
    */
    ~History();

private slots:
    /*
     * Actions taken when the Clear Past History button is pressed
    */
    void on_pushButton_clicked();
private:
    /*
     * Window created from the .ui file
    */
    Ui::History *ui;
    /*
     * Loads the current and past todos into a list view
    */
    void loadHistory();

};

#endif // HISTORY_H
