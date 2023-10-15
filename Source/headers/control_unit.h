#ifndef CONTROL_UNIT_H 
#define CONTROL_UNIT_H

#include <vector>
#include <string>
#include "todo.h"
#include <QtSql>


class ControlUnit{
		private:
                int nextId;
		public:
				ControlUnit();
                bool AddTodo(std::string name,std::string start_date,std::string end_date,std::string date_created);
				bool EditTodo(std::string name,std::string start_date,std::string end_date,int id);
				bool DeleteTodo(int id);
				bool UpdateTodoStatus(std::string status);
				~ControlUnit();

};


#endif


