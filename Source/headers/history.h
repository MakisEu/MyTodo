#ifndef HISTORY_H
#define HISTORY_H

#include <QWidget>

namespace Ui {
class History;
}

class History : public QWidget
{
    Q_OBJECT

public:
    explicit History(QWidget *parent = nullptr);
    ~History();

private slots:
    void on_pushButton_clicked();
    void loadHistory();
private:
    Ui::History *ui;
};

#endif // HISTORY_H
