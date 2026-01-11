from src.database import Database
import sys
from src.calandar_event import calandar_event
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame, QHBoxLayout, QSizePolicy, QPushButton, QMenu
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, Signal, QDateTime, QDate
from src.ui_colors import ui_colors
from src.add_todo import AddTodo



class ScrollableListWidget(QWidget):
    item_double_clicked = Signal(str)
    empty_space_double_clicked = Signal()

    def __init__(self, parent=None,database=None,refresh_function=None):
        super().__init__()
        self.database = database
        self.parent=parent
        self.events=[]
        self.refresh_function=refresh_function
        self.main_month=None
        self.menuActions=[]
        self.add_todo=None

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)  # Remove main layout margins
        main_layout.setSpacing(0)

        # Header
        header_layout = QHBoxLayout()
        header_label = QLabel("Header Text",parent=self)
        header_label.setStyleSheet(f"""
        QLabel {{
            background-color: {ui_colors.getDayTitleBackgroundColor()};
            padding: 0px;
            margin: 0px;
            border-top: None;
            border-bottom: None;

            color: {ui_colors.getTextColor()};
        }}""")
        header_label.setAlignment(Qt.AlignRight)
        header_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Expanding horizontally

        #header_layout.addStretch(1)  # Ensure the header label takes up all available space
        #header_layout.addStretch()
        header_layout.addWidget(header_label)

        self.header_label = header_label

        main_layout.addLayout(header_layout)

        # Scrollable area
        self.scroll_area = QScrollArea(self)

        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setViewportMargins(0,0,0,0)
        self.scroll_area.setFrameShape(QFrame.NoFrame)  # Remove frame
        self.scroll_area.setStyleSheet(f"""
        QScrollArea {{
            border: None;
            margin: 0px;
            padding: 0px
        }}
        """)
        #self.scroll_area.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        #self.scroll_area.setFrameShape(QFrame.NoFrame)


        # Container widget setup
        self.container_widget = QWidget()
        self.container_layout = QVBoxLayout(self.container_widget)
        self.container_layout.setAlignment(Qt.AlignTop)
        self.container_layout.setContentsMargins(0, 0, 0, 0)  # Remove container margins
        self.container_layout.setSpacing(0)  # Remove spacing between items
        #self.container_widget.setStyleSheet("background-color: blue;")

        # Size policies for expansion
        self.container_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scroll_area.setWidget(self.container_widget)

        main_layout.addWidget(self.scroll_area)


        # Scroll arrows
        self.up_button = QPushButton("↑", self)
        self.down_button = QPushButton("↓", self)

        for button in [self.up_button, self.down_button]:
            button.setFixedSize(20, 20)
            button.setStyleSheet("""
                background-color: rgba(0, 0, 0, 0.2);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 0px;
            """)
            button.setCursor(Qt.PointingHandCursor)
            button.setVisible(False)  # Hide initially

        self.up_button.clicked.connect(self.scroll_up)
        self.down_button.clicked.connect(self.scroll_down)

        # Position the buttons
        self.up_button.setParent(self)
        self.down_button.setParent(self)

        # Position the buttons on top-right, stacked vertically
        self.up_button.move(self.width() - 10, (self.height() - self.up_button.height() * 2 - 5) // 2 + 20)  # Top button a bit lower
        self.down_button.move(self.width() - 10, self.up_button.y() + self.up_button.height() + 5)  # Bottom button




        # Show or hide the buttons based on overflow
        self.show_hide_buttons()

        add_todo_action = QAction("Add Todo", self)
        add_todo_action.triggered.connect(self.add_todo_button)
        self.menuActions.append(add_todo_action)



        #print(parent.styleSheet())

    def show_hide_buttons(self):
        """Check if there's overflow and show/hide scroll buttons accordingly."""
        # Only show the buttons if the container is taller than the scroll area
        if self.container_widget.height() > self.scroll_area.height():
            self.down_button.setVisible(True)
            self.up_button.setVisible(True)
        else:
            self.down_button.setVisible(False)
            self.up_button.setVisible(False)

    def scroll_up(self):
        """Scroll up the content."""
        scroll_pos = self.scroll_area.verticalScrollBar().value()
        self.scroll_area.verticalScrollBar().setValue(scroll_pos - 10)  # Scroll up by 10 pixels

        # Check if we can show the down button after scrolling
        self.show_hide_buttons()

    def scroll_down(self):
        """Scroll down the content."""
        scroll_pos = self.scroll_area.verticalScrollBar().value()
        self.scroll_area.verticalScrollBar().setValue(scroll_pos + 10)  # Scroll down by 10 pixels

        # Check if we can show the up button after scrolling
        self.show_hide_buttons()
    def populateList(self, date,main_month=None):
        # Clear existing items
        self.date=date
        if (not main_month):
            main_month=QDate.currentDate().month()
            self.main_month=main_month

        while self.container_layout.count():
            child = self.container_layout.takeAt(0)
            if child.widget():
                a=child.widget()
                child.widget().deleteLater()
                del a # del the widget
                del child   # del the layout item



        day = date.toString("MMM dd")
        self.header_label.setText(day)

        if (date.month()!= main_month):
            self.header_label.setStyleSheet(f"""
            QLabel {{
                background-color: {ui_colors.getDayTitleBackgroundColor()};
                padding: 0px;
                margin: 0px;
                border-top: None;
                border-bottom: None;
                color: {ui_colors.getNonMonthTextColor()};
            }}""")

        todo_of_the_day = self.database.getTodoOfTheDay(date.toString("dd/MM/yyyy"))

        self.events=[]
        for todo in todo_of_the_day:
            event_widget = calandar_event(todo,parent=self,refresh_function=self.refresh_function,database=self.database)
            # Ensure horizontal expansion
            event_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.events.append(event_widget)
            # Add stretch to fill horizontal space
            self.container_layout.addWidget(event_widget, stretch=1)

        self.show_hide_buttons()

    def add_todo_button(self):
        del self.add_todo
        self.add_todo = AddTodo(database=self.database)
        self.add_todo.setAttribute(Qt.WA_DeleteOnClose)
        self.add_todo.refreshData.connect(self.refresh_function)
        self.add_todo.setup_values(QDateTime.currentDateTime(),isDateTime=True)
        self.add_todo.setWindowTitle("Add Todo")
        self.add_todo.setWindowModality(Qt.ApplicationModal)

        self.add_todo.show()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton and self.scroll_area.widget().children():
            self.empty_space_double_clicked.emit()
            #add_todo = AddTodo(self.parent)
            #add_todo.setWindowTitle("Add Todo")
            #add_todo.setWindowModality(Qt.ApplicationModal)
            #add_todo.show()

            self.add_todo_button()

            print("Empty space double-clicked!")
        super().mouseDoubleClickEvent(event)


    def resizeEvent(self, event):
        """Reposition buttons when resizing."""
        super().resizeEvent(event)

        # Center the buttons vertically and position them on the right edge

        self.up_button.move(self.width() - 20, (self.height() - self.up_button.height() * 2 - 5) // 2 + 20)  # Top button a bit lower
        self.down_button.move(self.width() - 20, self.up_button.y() + self.up_button.height())  # Bottom button

        self.show_hide_buttons()

    def contextMenuEvent(self, event):
        """Right-click on empty space in the scroll area."""
        # Create the menu for empty space
        menu = QMenu(self)

        for action in self.menuActions:
            menu.addAction(action)

        # Show the menu at the position of the cursor
        menu.exec(event.globalPos())


# Example usage remains the same
if __name__ == "__main__":
    app = QApplication(sys.argv)
    database = Database()
    database.openDB()
    datetime = QDateTime.currentDateTime().addDays(-5)
    main_widget = ScrollableListWidget(database=database)
    main_widget.populateList(datetime.date())
    main_widget.setWindowTitle("Scrollable List Example")
    main_widget.resize(300, 400)
    main_widget.show()
    print(main_widget.styleSheet())
    sys.exit(app.exec())
