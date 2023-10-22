#ifndef REMINDER_H
#define REMINDER_H

#include <QString>


/*
 * Reminder is a simple class for a reminder
*/
class Reminder
{
public:
    /*
     * The id of the todo of the reminder
    */
    int todoId;
    /*
     * The message that will be shown in the notification
    */
    QString message;
    /*
     * The Title of thenotification
    */
    QString title;
    /*
     * Default constructoe
    */
    Reminder(int id,QString msg,QString ttl);
};

#endif // REMINDER_H
