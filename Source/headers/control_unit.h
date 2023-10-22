#ifndef CONTROL_UNIT_H 
#define CONTROL_UNIT_H

#include <vector>
#include <string>
#include "todo.h"
#include <QtSql>

/*
 * ControlUnit is the class that controls all the operation of the Todo database (Not the Reminder database)
*/
class ControlUnit{
        private:

                /*
                 * The id of the next Todo
                */
                int nextId;
        public:
                /*
                 * Default Constructor
                */
                ControlUnit();
                /*
                 * Adds a Todo to the database
                */
                bool AddTodo(std::string name,std::string start_date,std::string end_date,std::string date_created);
                /*
                 * Edits an existing Todo
                */
                bool EditTodo(Todo *td);
                /*
                 * Deletes an existing Todo
                */
                bool DeleteTodo(Todo *td);
                /*
                 * Updates the status of an existing Todo
                */
                bool UpdateTodoStatus(Todo *td,std::string status);
                /*
                 * Returns all the Todo of the database in String format
                */
                std::vector<std::string> getStringTodos();
                /*
                 * Return history of the past todo that have been removed in the database
                */
                std::vector<std::string> getPastHistory();
                /*
                 * Default destructor
                */
				~ControlUnit();

};


#endif


