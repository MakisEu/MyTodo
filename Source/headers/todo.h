#ifndef TODO_H
#define TODO_H
#include <string>


class Todo{
		private:
				std::string name;
				std::string start_date;
				std::string end_date;
				std::string date_created;
				int id;
				std::string status;
		public:
                Todo(std::string name,std::string start_date,std::string end_date,std::string date_created,int id);
				void editTodo(std::string name,std::string start_date,std::string end_date);
				std::string getName();
				std::string getStartDate();
				std::string getEndDate();
				std::string getDateCreated();
				void updateStatus(std::string status);
				int getId();
				std::string getStatus();
                std::string toString();
				~Todo();
};

#endif
