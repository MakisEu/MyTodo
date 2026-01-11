# This Python file uses the following encoding: utf-8
from src.todo import Todo
from src.database import Database


class ControlUnit:
    def __init__(self,database):
        if (not database):
            database = Database()
            database.openDB()
            database.createTables()
        self.database=database
        self.nextId=self.database.getNextId()

    def AddTodo(self,td):
        td.id=self.nextId
        self.database.addTodo(td)
        self.nextId+=1
        return True

    def EditTodo(self,td):
        self.database.editTodo(td)
        return True


    def DeleteTodo(self,td):
        self.database.deleteTodo(td.getId())
        with open("History.txt", "a") as myfile:
            if (td.getStatus()!="Completed"):
                td.updateStatus("Deleted")
            myfile.write(td.toString()+"\n")
        return True

    def UpdateTodoStatus(self,td,status):
        self.database.updateStatus(td.getId(),status)
        td.updateStatus(status)
        #if (status=="Completed"):
            #self.DeleteTodo(td)
        return True

    def getStringTodos(self):
        v=self.database.getTodos()
        strings=[]

        for i in range(len(v)):
            strings.append(v[i].toString())
        return strings

    def getPastHistory(self):
        strings=[]
        with open("History.txt", "r") as myfile:
            strings = [line.rstrip() for line in myfile]
        return strings

