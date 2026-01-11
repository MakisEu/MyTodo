# self Python file uses the following encoding: utf-8
from PySide6.QtCore import QDateTime, QTextStream, QFile, QIODevice
from PySide6.QtSql import QSqlDatabase,QSqlQuery
from src.helper import replace
from src.todo import Todo
from src.achievement import Achievement
from src.reminder import Reminder

import time
class Database:
    def __init__(self,DB=None):
        self.DB=DB
    def openDB(self,path = "currentTodos.db"):
        self.DB = QSqlDatabase.addDatabase("QSQLITE")
        self.DB.setDatabaseName(path)
        self.DB.open()
    def closeDB(self):
        self.DB.close()
    def createTables(self):
        query= QSqlQuery(self.DB)
        query.prepare("""CREATE TABLE IF NOT EXISTS Todo( ID INT PRIMARY KEY NOT NULL, NAME TEXT NOT NULL, STATUS TEXT NOT NULL, START_DATE CHAR(19) NOT NULL, END_DATE CHAR(19) NOT NULL, DATE_CREATED CHAR(19) NOT NULL, TAG TEXT NOT NULL, DATE_COMPLETED CHAR(19) );""")
        query.exec()
        query.prepare("""CREATE TABLE IF NOT EXISTS Reminders( TODOID INT NOT NULL, MESSAGE TEXT NOT NULL, TITLE CHAR(50) NOT NULL, DATE CHAR(19) NOT NULL, PRIMARY KEY (TODOID,DATE), FOREIGN KEY (TODOID) REFERENCES Todo(ID) ON DELETE CASCADE);""")
        query.exec()
        query.prepare("""CREATE TABLE IF NOT EXISTS Task( TASKID INT NOT NULL, NAME TEXT NOT NULL, STATUS CHAR(50) NOT NULL, ISSUBTASKOF INT, ISTASKOF INT, PRIMARY KEY (TASKID), FOREIGN KEY (ISTASKOF) REFERENCES Todo(ID) ON DELETE CASCADE, FOREIGN KEY (ISSUBTASKOF) REFERENCES Task(TASKID) ON DELETE CASCADE);""")
        query.exec()
        query.prepare("""CREATE TABLE IF NOT EXISTS Achievements (CODE CHAR(30) PRIMARY KEY, TITLE TEXT NOT NULL, DESCRIPTION TEXT NOT NULL, GOAL TEXT NOT NULL, CURRENT_PROGRESS TEXT NOT NULL, UNLOCKED INTEGER NOT NULL DEFAULT 0, DATE_UNLOCKED CHAR(19), PERCENTAGE_DONE INTEGER DEFAULT 0 );""")
        query.exec()
        self.createAchievements()

    def createAchievements(self):
        achievements=[]

        total_todos=[10,30,50,100,200,500,1000,2000]
        for i in range(len(total_todos)):
            code_id=f"TOTAL_TODOS_{i}"
            title=f"Complete {total_todos[i]} Todos"
            description=f"Mark {total_todos[i]} Todos as Complete"
            goal=f"{total_todos[i]}"
            achievements.append(Achievement(code_id=code_id, title=title, description=description, goal=goal,current_progress="0"))
        streaks=[1,3,5,7,10,12,15,18,21,24,27,30]+[i for i in range(35,101,5)]
        for i in range(len(streaks)):
            code_id=f"MAX_STREAK_{i}"
            title=f"Keep a daily streak of {streaks[i]} days"
            description=f"Keep a daily streak of {streaks[i]} days"
            goal=f"{streaks[i]}"
            achievements.append(Achievement(code_id, title=title, description=description, goal=goal,current_progress="0"))
        for achievement in achievements:
            self.initializeAchievement(achievement)




        #achievements.append(Achievement(code_id="TOTAL_TODOS_1", title="Complete 10 Todos", description="Mark 10 Todos as Complete"), goal="10",current_progress="0")
        #achievements.append(Achievement(code_id="TOTAL_TODOS_2", title="Complete 30 Todos", description="Mark 30 Todos as Complete"), goal="30",current_progress="0")
        #achievements.append(Achievement(code_id="TOTAL_TODOS_3", title="Complete 50 Todos", description="Mark 50 Todos as Complete"), goal="50",current_progress="0")
        #achievements.append(Achievement(code_id="TOTAL_TODOS_4", title="Complete 50 Todos", description="Mark 50 Todos as Complete"), goal="50",current_progress="0")
        #achievements.append(Achievement(code_id="TOTAL_TODOS_5", title="Complete 100 Todos", description="Mark 100 Todos as Complete"), goal="100",current_progress="0")
        #achievements.append(Achievement(code_id="TOTAL_TODOS_6", title="Complete 200 Todos", description="Mark 200 Todos as Complete"), goal="200",current_progress="0")
        #achievements.append(Achievement(code_id="TOTAL_TODOS_7", title="Complete 500 Todos", description="Mark 500 Todos as Complete"), goal="500",current_progress="0")
        #achievements.append(Achievement(code_id="TOTAL_TODOS_8", title="Complete 1000 Todos", description="Mark 1000 Todos as Complete"), goal="1000",current_progress="0")


    def initializeAchievement(self, achievement):
        query= QSqlQuery(self.DB)
        query.prepare("INSERT OR IGNORE INTO Achievements (CODE,TITLE,DESCRIPTION,GOAL,CURRENT_PROGRESS) VALUES (:code,:title,:description,:goal,:current_progress);")
        query.bindValue(":code",achievement.code_id)
        query.bindValue(":title",achievement.title)
        query.bindValue(":description",achievement.description)
        query.bindValue(":goal",achievement.goal)
        query.bindValue(":current_progress",achievement.current_progress)
        if (not query.exec()):
          print ("The query has failed:\n", query.executedQuery())
          print("Error: ",query.lastError())
          print(f"ID:{achievement.code_id}")

    def getAllAchievements(self):
        query = QSqlQuery(self.DB)

        query.prepare("SELECT CODE, TITLE, DESCRIPTION, GOAL, CURRENT_PROGRESS, UNLOCKED, DATE_UNLOCKED, PERCENTAGE_DONE FROM Achievements;")
        query.exec()

        achievements=[]

        while (query.next()):
            code=query.value(0)
            title=query.value(1)
            description=query.value(2)
            goal=query.value(3)
            current_progress=query.value(4)
            unlocked=query.value(5)
            date_unlocked=query.value(6)
            percentage_done=query.value(7)

            ach=Achievement(code_id=code, title=title, description=description, goal=goal,current_progress=current_progress, unlocked=unlocked, date_unlocked=date_unlocked, percentage_done=percentage_done)
            achievements.append(ach)
        return achievements

    def update_achivement(self,achievement):
        # code_id, current_progress, unlocked, date_unlocked, percentage_done
        query = QSqlQuery(self.DB)
        query.prepare("UPDATE Achievements SET CURRENT_PROGRESS=:current_progress, UNLOCKED=:unlocked, DATE_UNLOCKED=:date_unlocked, PERCENTAGE_DONE=:percentage_done WHERE CODE=:code_id;")
        query.bindValue(":current_progress",achievement.current_progress)
        query.bindValue(":unlocked",achievement.unlocked)
        query.bindValue(":date_unlocked",achievement.date_unlocked)
        query.bindValue(":percentage_done",achievement.percentage_done)
        query.bindValue(":code_id",achievement.code_id)
        if (not query.exec()):
          print ("The query has failed:\n", query.executedQuery())
          print("Error: ",query.lastError())
          print(f"ID:{achievement.code_id}")




    def addTodo(self,newTodo):
        name=newTodo.getName()
        replace(name,"\'","\'\'")
        replace(name,"\"","\"\"")
        status=newTodo.getStatus()
        replace(status,"\'","\'\'")
        replace(status,"\"","\"\"")
        start_date=newTodo.getStartDate()
        replace(start_date,"\'","\'\'")
        replace(start_date,"\"","\"\"")
        end_date=newTodo.getEndDate()
        replace(end_date,"\'","\'\'")
        replace(end_date,"\"","\"\"")
        date_created=newTodo.getDateCreated()
        replace(date_created,"\'","\'\'")
        replace(date_created,"\"","\"\"")

        query = QSqlQuery(self.DB)
        query.prepare("INSERT INTO Todo (ID,NAME,STATUS,START_DATE,END_DATE,DATE_CREATED,TAG, DATE_COMPLETED) VALUES (:id,:name,:status,:start_date,:end_date,:date_created,:tag,:date_completed);")
        query.bindValue(":id",newTodo.getId())
        query.bindValue(":name",name)
        query.bindValue(":status",status)
        query.bindValue(":start_date",start_date)
        query.bindValue(":end_date",end_date)
        query.bindValue(":date_created",date_created)
        query.bindValue(":tag",newTodo.getTag())
        query.bindValue(":date_completed",None)
        if (not query.exec()):
          print ("The query has failed:\n", query.executedQuery())
          print("Error: ",query.lastError())
          print(f"ID:{newTodo.getId()}")



        query.prepare("INSERT INTO Reminders (TODOID,MESSAGE,TITLE,DATE) VALUES (:id,:msg,:title,:date);")
        query.bindValue(":id",newTodo.getId())
        query.bindValue(":msg",f"The todo {name} has started.")
        query.bindValue(":title","Todo Has Started")
        query.bindValue(":date",start_date)
        if (not query.exec()):
          print ("The query has failed:\n", query.executedQuery())
          print("Error: ",query.lastError())


        query.prepare("INSERT INTO Reminders (TODOID,MESSAGE,TITLE,DATE) VALUES (:id,:msg,:title,:date);")
        query.bindValue(":id",newTodo.getId())
        query.bindValue(":msg",f"The todo {name} has expired.")
        query.bindValue(":title","Todo Has Expired")
        query.bindValue(":date",end_date)
        if (not query.exec()):
          print ("The query has failed:\n", query.executedQuery())
          print("Error: ",query.lastError())

    def deleteTodo(self,id):
        query = QSqlQuery(self.DB)
        query.exec("PRAGMA foreign_keys = ON")
        query.prepare(f"DELETE FROM Todo WHERE ID = {id};")
        query.exec()

    def editTodo(self,td):
        query = QSqlQuery(self.DB)
        query.prepare("SELECT * FROM Todo WHERE ID;")
        query.exec()
        query.next()
        start=query.value(3)
        end=query.value(4)

        query.prepare("UPDATE Todo SET NAME=:name, START_DATE=:sd, END_DATE=:ed, TAG=:tag WHERE ID=:id;")
        query.bindValue(":name",td.getName())
        query.bindValue(":sd",td.getStartDate())
        query.bindValue(":ed",td.getEndDate())
        query.bindValue(":tag",td.getTag())
        query.bindValue(":id",td.getId())
        if (not query.exec()):
          print ("The query has failed:\n", query.executedQuery())
          print("Error: ",query.lastError())
          print(f"ID:{td.getId()}")

        query.prepare("DELETE FROM Reminders WHERE TODOID=:id;")
        query.bindValue(":id",td.getId())
        if (not query.exec()):
          print ("The query has failed:\n", query.executedQuery())
          print("Error: ",query.lastError())
          print(f"ID:{td.getId()}")

        query.prepare("INSERT INTO Reminders (TODOID,MESSAGE,TITLE,DATE) VALUES (:id,:msg,:title,:date);")
        query.bindValue(":id",td.getId())
        query.bindValue(":msg", f"The todo {td.getName()} has started.")
        query.bindValue(":title","Todo Has Started")
        query.bindValue(":date",td.getStartDate())
        if (not query.exec()):
          print ("The query has failed:\n", query.executedQuery())
          print("Error: ",query.lastError())
          print(f"ID:{td.getId()}")

        query.prepare("INSERT INTO Reminders (TODOID,MESSAGE,TITLE,DATE) VALUES (:id,:msg,:title,:date);")
        query.bindValue(":id",td.getId())
        query.bindValue(":msg",f"The todo {td.getName()} has expired.")
        query.bindValue(":title","Todo Has Expired")
        query.bindValue(":date",td.getEndDate())
        if (not query.exec()):
          print ("The query has failed:\n", query.executedQuery())
          print("Error: ",query.lastError())
          print(f"ID:{td.getId()}")

    def updateStatus(self,id,s):
        query = QSqlQuery(self.DB)
        if (s=="Completed"):
            query.prepare("UPDATE Todo SET STATUS=:status, DATE_COMPLETED=:datecompleted WHERE ID=:id;")
            query.bindValue(":status",s)
            query.bindValue(":id",id)
            query.bindValue(":datecompleted", QDateTime.currentDateTime().toString("dd/MM/yyyy hh:mm"))
            query.exec()


            query.prepare("DELETE FROM Reminders WHERE TODOID=:id;")
            query.bindValue(":id",id)

            if (not query.exec()):
              print ("The query has failed:\n", query.executedQuery())
              print("Error: ",query.lastError())
              print(f"ID:{id}")

        else:
            query.prepare("UPDATE Todo SET STATUS=:status WHERE ID=:id;")
            query.bindValue(":status",s)
            query.bindValue(":id",id)
        query.exec()

    def getReminders(self,datetime):
        query = QSqlQuery(self.DB)
        vec=[]
        query.prepare("SELECT TODOID,MESSAGE,TITLE FROM Reminders WHERE DATE=:datetime ;")
        query.bindValue(":datetime",datetime)
        query.exec()

        while (query.next()):
            vec.append(Reminder(query.value(0),query.value(1),query.value(2)));
        return vec
    def deleteReminder(self,id,datetime):
        query = QSqlQuery(self.DB)
        query.prepare("DELETE FROM Reminders WHERE TODOID=:id AND DATE=:datetime ;")
        query.bindValue(":id",id)
        query.bindValue(":datetime",datetime)
        query.exec()

    def getNextId(self):
        query = QSqlQuery(self.DB)
        query.prepare("SELECT MAX(id) FROM Todo ;")
        query.exec()
        if (query.next() and type(query.value(0))!=type("")):
            #print("Query result:",query.value(0))
            return query.value(0)+1;
        else:
            return 0;

    def removeDaily(self,suffix):
        query = QSqlQuery(self.DB)
        query.exec("PRAGMA foreign_keys = ON")
        query.prepare(f"DELETE FROM Todo WHERE NAME LIKE \'%{suffix}%\';")
        query.exec()

    def getTodoOfTheDay(self,date):
        query = QSqlQuery(self.DB)
        query.prepare("SELECT * FROM Todo WHERE substr(START_DATE,1,10) = :day ORDER BY START_DATE ASC;")
        query.bindValue(":day",date)
        query.exec()
        todos=[]

        while (query.next()):
            id=query.value(0)
            name=query.value(1)
            status=query.value(2)
            start_date=query.value(3)
            end_date=query.value(4)
            date_created=query.value(5)
            tag=query.value(6)
            td = Todo(name,start_date,end_date,date_created,id,tag)
            td.updateStatus(status)
            todos.append(td)

        return todos

    def getAllTodos(self):
        query = QSqlQuery(self.DB)

        query.prepare("SELECT ID, NAME, STATUS, START_DATE, END_DATE, DATE_CREATED, TAG, DATE_COMPLETED FROM Todo;")
        query.exec()

        todos=[]

        while (query.next()):
            id=query.value(0)
            name=query.value(1)
            status=query.value(2)
            start_date=query.value(3)
            end_date=query.value(4)
            date_created=query.value(5)
            tag=query.value(6)
            date_completed=query.value(7)
            td = Todo(name,start_date,end_date,date_created,id,tag)
            td.updateStatus(status)
            if (status=="Completed"):
                td.date_completed=date_completed
            todos.append(td)
        return todos


    def getTodos(self):
        query = QSqlQuery(self.DB)
        query.prepare("SELECT * FROM Todo;")
        if (not query.exec()):
            #Error
            print("Error")

        v=[]
        while (query.next()):
            id=query.value(0)
            name=query.value(1)
            status=query.value(2)
            start_date=query.value(3)
            end_date=query.value(4)
            date_created=query.value(5)
            tag=query.value(6)
            date_completed=query.value(7)
            td=Todo(name,start_date,end_date,date_created,id,tag)
            td.updateStatus(status)
            if (status=="Completed"):
                td.date_completed=date_completed
            v.append(td)
        return v

    def dump(self,filename):
        query = QSqlQuery(self.DB)
        file=QFile(filename)
        if not file.open(QFile.WriteOnly | QFile.Text):
            print(f"Cannot write to file: {filename}")
            return
        stream = QTextStream(file)
        tables = self.DB.tables()
        print(tables)
        system_tables = {'sqlite_sequence', 'sqlite_stat1', 'sqlite_stat2', 'sqlite_stat3', 'sqlite_stat4'}

        cnt=0
        for table in tables:
            if table in system_tables:
                continue
            print(cnt)
            cnt+=1

            if query.exec(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table}'"):
                if query.next():
                    create_stmt = query.value(0)
                    create_stmt = create_stmt.replace('CREATE TABLE', 'CREATE TABLE IF NOT EXISTS')
                    if create_stmt:
                        stream << " ".join(create_stmt.split()) << ";\n\n"

            # Dump the data from the table
            if query.exec(f"SELECT * FROM {table}"):
                columns = [query.record().field(i).name() for i in range(query.record().count())]
                stream << f"-- Data for table {table} --\n"
                while query.next():
                    row_data = [query.value(i) for i in range(query.record().count())]
                    # Format data for easier reading, e.g., with quotes for strings and handling None values
                    formatted_data = ", ".join(
                        [f"'{str(value).replace('\'', '\'\'')}'" if value is not None else "NULL" for value in row_data]
                    )
                    stream << f"INSERT OR REPLACE INTO {table} ({', '.join(columns)}) VALUES ({formatted_data});\n"
                stream << "\n"
        print("ok")
        file.close()
    def import_db(self,filename):
        query = QSqlQuery(self.DB)
        file=QFile(filename)
        if not file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
            return
        while not file.atEnd():
            line = file.readLine().toStdString()
            if (line.strip()!=""):
                query.prepare(line)
                query.exec()
        file.close()



