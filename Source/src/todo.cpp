#include "../headers/todo.h"


Todo::Todo(std::string name,std::string start_date,std::string end_date,std::string date_created,int id){
		this->editTodo(name,start_date,end_date,date_created);
		this->status="In Progress";
		this->id=id;
}
void Todo::editTodo(std::string name,std::string start_date,std::string end_date,std::string date_created ){
		this->name=name;
		this->start_date=start_date;
		this->end_date=end_date;
		this->date_created=date_created;

}

std::string Todo::getName(){
		return this->name;
}
std::string Todo::getStartDate(){
		return this->start_date;
}
std::string Todo::getEndDate(){
		return this->end_date;
}
std::string Todo::getDateCreated(){
		return this->date_created;
}
void Todo::updateStatus(std::string status){
		this->status=status;
}
int Todo::getId(){
		return this->id;
}
std::string Todo::getStatus(){
		return this->status;
}
Todo::~Todo(){
		//Write entry to history
}

