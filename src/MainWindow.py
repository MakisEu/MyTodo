import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget,QVBoxLayout, QLabel, QToolBar,QTabWidget, QToolButton, QMenu, QFileDialog
from PySide6.QtGui import QAction, QPixmap, QIcon
from PySide6.QtCore import Qt, QTimer, QSize, QUrl
from PySide6.QtMultimedia import QSoundEffect
from src.monthly_timetable import CustomGridWidget
from src.database import Database
from icalendar import Calendar, Event, vText, vDatetime
from datetime import datetime
from src.helper import get_save_filename_with_suffix, get_load_filename_with_suffix, check_todo_format
from src.control_unit import ControlUnit
from src.todo import Todo
from src.list_view import CustomListView
from src.todo_timeline import TodoDashboard
from src.WeeklyTimetable import TimeTable
import rc_assets
import gc



class CustomWidget2(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("This is Custom Widget 2")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MyTodo")
        self.setGeometry(100, 100, 1000, 1000)

        icon = QIcon()
        icon.addFile(u":/icons/assets/todo_icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.setWindowIcon(icon)


        self.database = Database()
        self.database.openDB()
        self.database.createTables()


        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Create tab widget
        tab_widget = QTabWidget()
        tab_widget.setMovable(True)
        tab_widget.currentChanged.connect(self.refreshAllData)
        main_layout.addWidget(tab_widget)
        #self.tab_widget=tab_widget


        # Add tabs with custom widgets
        self.monthly_view=CustomGridWidget(parent=central_widget,database=self.database,refresh_function=self.refreshAllData)
        self.list_view=CustomListView(database=self.database,parent=central_widget,refresh_function=self.refreshAllData)
        self.todo_timeline=TodoDashboard(database=self.database,todos=self.database.getAllTodos(),parent=central_widget)
        self.weekly_timetable=TimeTable(database=self.database,parent=central_widget)
        #self.list_view.refreshData.connect(self.refreshAllData)

        tab_widget.addTab(self.monthly_view, "Event monthly view")
        tab_widget.addTab(self.list_view.ui.list_widget, "Todo list view")
        tab_widget.addTab(self.todo_timeline, "Todo completion timeline")
        tab_widget.addTab(self.weekly_timetable, "Timetable")

        effect = QSoundEffect(self)
        effect.setSource(QUrl("qrc:/sounds/assets/pop-6.wav"))
        effect.setVolume(1);
        effect.setLoopCount(1)
        self.effect=effect

        self.create_toolbar()
        timer = QTimer(self)
        timer.timeout.connect(self.check_notify)
        timer.start(1000)
        self.refresh=True

    def refreshAllData(self):
        #print("Refreshed data")
        #print(f"Current tab: {self.tab_widget.tabText(self.tab_widget.currentIndex())}")
        self.list_view.refreshTodos()
        self.monthly_view.refreshCells()
        self.todo_timeline.process(todos=self.database.getAllTodos())
        self.weekly_timetable.create_columns()

        gc.collect()


    def check_notify(self):
        """Checks every time it is called if there is any reminder for the current datetime and if there are, send notifications"""

        from PySide6.QtCore import QDateTime

        date = QDateTime.currentDateTime()
        formatted_time = date.toString("dd/MM/yyyy hh:mm")

        # Get the reminders for the current datetime
        reminders = self.database.getReminders(formatted_time)
        if (len(reminders)==0):
            return

        messages_start = ""
        messages_end = ""

        # Process each reminder
        for reminder in reminders:
            # Categorize messages into 'started' and 'expired'
            if "started" in reminder.message:
                messages_start += reminder.message + "\n"
            else:
                messages_end += reminder.message + "\n"

            # Delete the reminder and update its status
            self.database.deleteReminder(reminder.todo_id, formatted_time)
            self.database.updateStatus(reminder.todo_id, "In Progress")

        self.effect.play()

        self.trayNotification(messages_start, messages_end)
        #self.toastNotification(messages_start, messages_end)

    # Refresh the todos UI
    def trayNotification(self, messages_start, messages_end):
        from PySide6.QtGui import QIcon
        from PySide6.QtWidgets import QSystemTrayIcon
        # Show tray notifications
        tray_icon = QSystemTrayIcon(self)
        tray_icon.setIcon(QIcon(QPixmap(":/icons/assets/todo_icon.png")))
        tray_icon.setVisible(True)

        if len(messages_start) > 2:
            tray_icon.showMessage(
                "Todo Has Started", messages_start, QIcon(QPixmap(":/icons/assets/todo_icon.png")), 2500
            )
            self.refreshAllData()


        if len(messages_end) > 2:
            tray_icon.showMessage(
                "Todo Has Expired", messages_end, QIcon(QPixmap(":/icons/assets/todo_icon.png")), 2500
            )
            self.refreshAllData()
        tray_icon.setVisible(False)
        del tray_icon

    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        def create_button(text, menu):
            button = QToolButton()
            button.setText(text)
            button.setMenu(menu)
            button.setPopupMode(QToolButton.InstantPopup)
            button.setStyleSheet("QToolButton::menu-indicator { image: none; }")
            return button

        def create_action(text, slot):
            action = QAction(text, self)
            action.triggered.connect(slot)
            return action

        # File Menu
        file_menu = QMenu(self)

        export_submenu = QMenu("Export", self)
        export_submenu.addAction(create_action("Export to .sql", self.on_export_sql))
        export_submenu.addAction(create_action("Export to .ics", self.on_export_ics))

        import_submenu = QMenu("Import", self)
        import_submenu.addAction(create_action("Import from .sql", self.on_import_sql))
        import_submenu.addAction(create_action("Import from .ics", self.on_import_ics))

        file_menu.addMenu(export_submenu)
        file_menu.addMenu(import_submenu)

        # Actions Menu
        actions_menu = QMenu(self)
        for text, slot in [("New Action", self.on_new_action),
                           ("Edit Action", self.on_edit_action),
                           ("Delete Action", self.on_delete_action)]:
            actions_menu.addAction(create_action(text, slot))

        # Settings Menu
        settings_menu = QMenu(self)
        for text, slot in [("Preferences", self.on_preferences),
                           ("Configuration", self.on_configuration)]:
            settings_menu.addAction(create_action(text, slot))

        # View Menu
        view_menu = QMenu(self)

        themes_submenu = QMenu("Themes", self)
        for text, slot in [("Light Theme", self.on_light_theme),
                           ("Dark Theme", self.on_dark_theme),
                           ("System Theme", self.on_system_theme)]:
            themes_submenu.addAction(create_action(text, slot))
        view_menu.addMenu(themes_submenu)

        view_menu.addSeparator()
        view_menu.addAction(create_action("Toggle Fullscreen", self.on_toggle_fullscreen))

        # Help Menu
        help_menu = QMenu(self)
        for text, slot in [("About", self.on_about),
                           ("Documentation", self.on_documentation)]:
            help_menu.addAction(create_action(text, slot))

        help_menu.addSeparator()
        help_menu.addAction(create_action("Support", self.on_support))

        # Add all buttons to toolbar
        for name, menu in [("File", file_menu),
                           ("Actions", actions_menu),
                           ("Settings", settings_menu),
                           ("View", view_menu),
                           ("Help", help_menu)]:
            toolbar.addWidget(create_button(name, menu))

    # File menu methods
    def on_export_sql(self):
        print("Exporting to .sql...")
        output_file=get_save_filename_with_suffix(fileDialogText="Save database File", defaultSuffix="db", nameFilter="Database Files (*.db *.sql)",selectedFile="database.db")

        self.database.dump(output_file)

    def on_export_ics(self):
        print("Exporting to .ics...")

        output_file=get_save_filename_with_suffix()
        print(output_file)

        todos=self.database.getAllTodos()

        cal = Calendar()
        cal.add('prodid', '-//MyImprovedTodo//EN')
        cal.add('version', '2.0')
        cal.add('name', 'Todo List')

        for todo in todos:
            event = Event()
            todo_id, name, status, start_date, end_date, date_created, tag = todo.id, todo.name, todo.status, todo.start_date, todo.end_date, todo.date_created, todo.tag

            # Parse dates
            dt_start = datetime.strptime(start_date, '%d/%m/%Y %H:%M')
            dt_end = datetime.strptime(end_date, '%d/%m/%Y %H:%M')
            dt_created = datetime.strptime(date_created, '%d/%m/%Y %H:%M')

            # Standard iCalendar properties
            event.add('uid', f"todo-{todo_id}")
            event.add('dtstamp', datetime.now())
            event.add('created', dt_created)
            event.add('dtstart', dt_start)
            event.add('dtend', dt_end)
            event.add('summary', name)
            event.add('categories', [tag] if tag else ['General'])

            # Map to standard iCalendar status for compatibility
            status_map = {
                'completed': 'COMPLETED',
                'done': 'COMPLETED',
                'pending': 'NEEDS-ACTION',
                'in progress': 'IN-PROCESS',
                'cancelled': 'CANCELLED'
            }
            ical_status = status_map.get(status.lower(), 'NEEDS-ACTION')
            event.add('status', ical_status)

            # CUSTOM PROPERTIES - These will be ignored by standard parsers
            # but preserved for re-import
            event.add('X-TODO-APP-STATUS', status)  # Original status verbatim
            event.add('X-TODO-APP-ID', str(todo_id))
            event.add('X-TODO-APP-DATE-CREATED', date_created)
            event.add('X-TODO-APP-TAG', tag)

            # Add description that includes custom data for human readability
            desc = f"""{{Todo Item: {name}
                       Status: {status}
                       Original ID: {todo_id}
                       Created: {date_created}
                       Tag: {tag}}}
    [Custom app data preserved in X-TODO-APP-* properties]"""
            event.add('description', desc)

            cal.add_component(event)

        with open(output_file, 'wb') as f:
            f.write(cal.to_ical())

        print(f"Exported {len(todos)} todos with custom properties to {output_file}")

    # Usage


    def on_import_sql(self):
        print("Importing from .sql...")
        input_file=get_load_filename_with_suffix(fileDialogText="Import database File", defaultSuffix="db", nameFilter="Database Files (*.db *.sql)",selectedFile="database.db")

        self.database.import_db(input_file)
        self.monthly_view.refreshCells()

    def on_import_ics(self):
        print("Importing from .ics...")

        input_file=get_load_filename_with_suffix()

        # Read the ICS file content
        with open(input_file, 'rb') as f:
            cal = Calendar.from_ical(f.read())

        todos = []

        for component in cal.walk('vevent'):

            # Extract fields from the VEVENT component
            uid=str(component.get('uid'))
            if (check_todo_format(uid)):
                id=uid.split("-")[-1]
            else:
                id=None
            id = id
            name = str(component.get('summary'))

            # Extract dates (ensure they're in correct format)
            dtstart = component.get('dtstart').dt
            dtend = component.get('dtend').dt
            dtcreated = component.get('created').dt

            # Format the dates to match your database model
            if dtstart:
                start_date = dtstart.strftime('%d/%m/%Y %H:%M')
            if dtend:
                end_date = dtend.strftime('%d/%m/%Y %H:%M')
            if dtcreated:
                date_created = dtcreated.strftime('%d/%m/%Y %H:%M')

            # Get custom data if available (X-TODO-APP-*)
            tag = str(component.get('X-TODO-APP-TAG', ''))

            # Try to map the status correctly
            status_map = {
                'COMPLETED': 'completed',
                'NEEDS-ACTION': 'pending',
                'IN-PROCESS': 'in progress',
                'CANCELLED': 'cancelled'
            }
            status = status_map.get(str(component.get('status', 'NEEDS-ACTION')).upper(), 'pending')

            # Map to your Todo object or database model
            # Here, you could insert the todo object into your database
            todo=Todo(name,start_date,end_date,date_created,id,tag)
            todo.status=status
            todos.append(todo)

            # If you're using a database or ORM, you can store the todo here
            # Example: self.database.save(todo)
        existing_todos=self.database.getAllTodos()
        existing_todos_dict={}
        for todo in existing_todos:
            hash=todo.getName()+"|"+str(todo.getStartDate())+"|"+str(todo.getEndDate())
            existing_todos_dict[hash]=todo
        cu  =  ControlUnit(self.database)
        cnt=0
        print (existing_todos_dict.keys())
        for todo in todos:
            hash=todo.getName()+"|"+str(todo.getStartDate())+"|"+str(todo.getEndDate())
            #print (hash)
            if hash not in existing_todos_dict.keys():
                print(todo.toString())
                cu.AddTodo(todo)
                #existing_todos_dict[hash]=todo
                cnt+=1

        print(f"Imported {cnt} new todos from the .ics file.")
        self.monthly_view.refreshCells()


    # Actions menu methods
    def on_new_action(self):
        print("Creating new action...")

    def on_edit_action(self):
        print("Editing action...")

    def on_delete_action(self):
        print("Deleting action...")

    # Settings menu methods
    def on_preferences(self):
        print("Opening preferences...")

    def on_configuration(self):
        print("Opening configuration...")

    # View menu methods
    def on_light_theme(self):
        print("Light theme applied!")

    def on_dark_theme(self):
        print("Dark theme applied!")

    def on_system_theme(self):
        print("System theme applied!")

    def on_toggle_fullscreen(self):
        print("Toggling fullscreen!")
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    # Help menu methods
    def on_about(self):
        print("Showing about dialog...")

    def on_documentation(self):
        print("Opening documentation...")

    def on_support(self):
        print("Opening support page...")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
