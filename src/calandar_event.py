# calendar_event.py
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QSizePolicy,QToolTip, QMenu
from PySide6.QtGui import QFontMetrics, QAction
from src.ui_colors import ui_colors
from src.edit_todo import Edit_Todo
from datetime import datetime
from src.control_unit import ControlUnit


class calandar_event(QLabel):
    def __init__(self, event_item,parent=None,max_name_length=128,refresh_function=None,database=None):
        super().__init__(parent)
        self.event_item = event_item
        self.setWordWrap(False)
        self.parent=parent
        self.refresh_function=refresh_function
        self.database=database
        self.edit_todo=None

        # Get the name and elide it (truncate with "...")
        #fm = QFontMetrics(self.font())
        bg_color = ui_colors.getCompletedTodoColor() if self.event_item.status == "Completed" else ui_colors.getMissedTodoColor() if datetime.strptime(self.event_item.end_date, "%d/%m/%Y %H:%M") < datetime.now() else ui_colors.getEventColor()


        truncated_text = self.fontMetrics().elidedText(event_item.name, Qt.ElideRight, max_name_length-self.fontMetrics().boundingRect("."*5).width())  # 140px max width (adjust as needed)
        self.setText(truncated_text)

        self.setStyleSheet(f"""
            calandar_event {{
                border: 1px solid {bg_color};
                margin: 2px;
                font-size: 12px;
                text-align: center;
                white-space: nowrap;
                border-radius: 2px;
                color: {ui_colors.getEventTextColor()};
                background-color: {bg_color};

            }}

            calandar_event:hover {{
                background-color: ui_colors.getEventColor();
                background-image: linear-gradient(45deg, #9b30ff, #8a2be2);
            }}
        """)

        self.setToolTip(f"Name: {event_item.name} \nStart Date: {event_item.start_date}\nEnd Date: {event_item.end_date}\nDate Created: {event_item.date_created}\nStatus: {event_item.status}\nTag: {event_item.tag}")
        #tooltip_font = QFont("Arial", 10)  # Adjust font as needed
        #QToolTip.setFont(tooltip_font)

        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.setAlignment(Qt.AlignCenter)

        #self.setMaximumWidth(max_name_length)
        self.setMaximumHeight(20)
        self.mouseDoubleClickEvent = self.on_item_double_clicked
        self.mouseReleaseEvent = self.on_item_click_released

    def edit_todo_button(self):
        del self.edit_todo
        self.edit_todo = Edit_Todo(database=self.database)

        self.edit_todo.refreshData.connect(self.refresh_function)
        self.edit_todo.setWindowTitle("Edit Todo")
        self.edit_todo.setWindowModality(Qt.ApplicationModal)

        self.edit_todo.setValues(self.event_item)

        self.edit_todo.show()

    def on_item_double_clicked(self, event):
        self.edit_todo_button()

        print(f"Double-clicked on1: {self.event_item.getName()}")

    def on_item_click_released(self, event):
        print(f"Clicked on: {self.event_item.getName()}")

    def contextMenuEvent(self, event):
        """Right-click on an item to show the menu."""
        menu = QMenu(self)

        # Add actions to the context menu
        edit_action = QAction("Edit Todo", self)
        edit_action.triggered.connect(self.edit_todo_button)
        menu.addAction(edit_action)

        complete_action = QAction("Mark Todo as Complete", self)
        complete_action.triggered.connect(self.mark_todo_complete_button)
        menu.addAction(complete_action)

        delete_action = QAction("Delete Todo", self)
        delete_action.triggered.connect(self.delete_todo_button)
        menu.addAction(delete_action)

        # Add a separator
        menu.addSeparator()

        for action in self.parent.menuActions:
            menu.addAction(action)

        # Show the menu at the position of the cursor
        menu.exec(event.globalPos())
    def mark_todo_complete_button(self):
        cu=ControlUnit(database=self.database)

        cu.UpdateTodoStatus(self.event_item,"Completed")
        self.refresh_function()

    def delete_todo_button(self):
        cu=ControlUnit(database=self.database)
        self.event_item.updateStatus("Deleted")
        cu.DeleteTodo(self.event_item)
        self.refresh_function()


