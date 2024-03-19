#ifndef TODO_H
#define TODO_H
#include <string>

/*
 * Todo is a class thatrepresents a todo and holds the relevant information and methods
*/
class Todo{
        private:
                /*
                * The name of the todo
                */
                std::string name;
                /*
                * The start date of the todo
                */
				std::string start_date;
                /*
                * The end date of the todo
                */
				std::string end_date;
                /*
                * The date the todo was created
                */
				std::string date_created;
                /*
                * The id of the todo
                */
				int id;
                /*
                * The status of the todo
                */
                std::string status;
                /*
                * The tag of the todo
                */
                std::string tag;
		public:
                /*
                * Default constructor of the Todo
                */
                Todo(std::string name,std::string start_date,std::string end_date,std::string date_created,int id,std::string tag);
                /*
                * Method that edits the values of the todo
                */
                void editTodo(std::string name,std::string start_date,std::string end_date,std::string tag);
                /*
                * Getter for the name
                */
				std::string getName();
                /*
                * Getter for the start date
                */
				std::string getStartDate();
                /*
                * Getter for the end date
                */
				std::string getEndDate();
                /*
                * Getter for the date the todo was created
                */
				std::string getDateCreated();
                /*
                * Updates the status of the todo
                */
				void updateStatus(std::string status);
                /*
                * Getter for the id
                */
				int getId();
                /*
                * Getter for the status
                */
                std::string getStatus();
                /*
                 * Getter for the tag
                */
                std::string getTag();
                /*
                * Returns the string representation of the todo
                */
                std::string toString();
                /*
                * Default destructor of the Todo
                */
				~Todo();
};

#endif
