#include "../headers/todo.h"


Todo::Todo(std::string name,std::string start_date,std::string end_date,std::string date_created,int id){
        this->editTodo(name,start_date,end_date);
		this->status="In Progress";
        this->id=id;
        this->date_created=date_created;

}
void Todo::editTodo(std::string name,std::string start_date,std::string end_date ){
		this->name=name;
		this->start_date=start_date;
		this->end_date=end_date;

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
std::string toString(){
        std::string s;
        //s=std::to_string(id)+"{Delimiter}"+name+"{Delimiter}"+start_date+"{Delimiter}"+end_date+"{Delimiter}"+date_created+"{Delimiter}"+status;
        return s;
}

Todo::~Todo(){
		//Write entry to history
}

