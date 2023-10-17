#ifndef REMINDER_H
#define REMINDER_H

#include <QString>

class Reminder
{
public:
    int todoId;
    QString message;
    QString title;

    Reminder(int id,QString msg,QString ttl);
};

#endif // REMINDER_H
