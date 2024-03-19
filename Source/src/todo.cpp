#include "../headers/todo.h"


/*
 * Sets the values of the todo and the status into the default string of every todo
*/
Todo::Todo(std::string name,std::string start_date,std::string end_date,std::string date_created,int id, std::string tag){
        this->editTodo(name,start_date,end_date,tag);
        this->status="Not Started";
        this->id=id;
        this->date_created=date_created;
        this->tag=tag;
}
/*
 * Edits the values of the todo
*/
void Todo::editTodo(std::string name,std::string start_date,std::string end_date, std::string tag){
		this->name=name;
		this->start_date=start_date;
		this->end_date=end_date;
        this->tag=tag;
}
/*
 * Getter for the name
*/
std::string Todo::getName(){
		return this->name;
}
/*
 * Getter for the start date
*/
std::string Todo::getStartDate(){
		return this->start_date;
}
/*
 * Getter for the end date
*/
std::string Todo::getEndDate(){
		return this->end_date;
}
/*
 * Getter for the date created
*/
std::string Todo::getDateCreated(){
		return this->date_created;
}
/*
 * Updates the status of the todo
*/
void Todo::updateStatus(std::string status){
		this->status=status;
}
/*
 * Getter for the id
*/
int Todo::getId(){
		return this->id;
}
/*
 * Getter for the status
*/
std::string Todo::getStatus(){
		return this->status;
}
/*
 * Getter for the status
*/
std::string Todo::getTag(){
        return this->tag;
}
/*
 * Creates a string with the values of the todo and returns it
*/
std::string Todo::toString(){
        std::string s;
        s=name+"  "+start_date+"  "+end_date+"  "+date_created+"  "+status+" "+tag;
        //s=std::to_string(id)+"{Delimiter}"+name+"{Delimiter}"+start_date+"{Delimiter}"+end_date+"{Delimiter}"+date_created+"{Delimiter}"+status;
        return s;
}
/*
 * Default destructor
*/
Todo::~Todo(){
		//Write entry to history
}

