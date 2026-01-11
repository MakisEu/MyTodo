# This Python file uses the following encoding: utf-8

class Todo:
    def __init__(self, name: str, start_date: str, end_date: str, date_created: str, id: int, tag: str):
        self.editTodo(name, start_date, end_date, tag)
        self.status = "Not Started"
        self.id = id
        self.date_created = date_created
        self.tag = tag
        self.date_completed=None

    def editTodo(self, name: str, start_date: str, end_date: str, tag: str):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.tag = tag

    def getName(self) -> str:
        return self.name

    def getStartDate(self) -> str:
        return self.start_date

    def getEndDate(self) -> str:
        return self.end_date

    def getDateCreated(self) -> str:
        return self.date_created

    def updateStatus(self, status: str):
        self.status = status

    def getId(self) -> int:
        return self.id

    def getStatus(self) -> str:
        return self.status

    def getTag(self) -> str:
        return self.tag

    def toString(self) -> str:
        s = f"{self.name}  {self.start_date}  {self.end_date}  {self.date_created}  {self.status} {self.tag}"
        return s

    def __del__(self):
        # Write entry to history
        pass

