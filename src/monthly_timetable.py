from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QSizePolicy
from PySide6.QtCore import Qt, QDate,Signal
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QHBoxLayout, QPushButton

from src.CalendarEventWidget import ScrollableListWidget
from src.ui_colors import ui_colors

def print_detailed_z_order(widget):
    parent = widget.parentWidget()
    if parent:
        children = parent.children()
        index = children.index(widget)
        print(f"{widget.objectName()} z-order: {index} of {len(children)}. Children:")
        for child in children:
            print(child)


class SelectionOverlay(QWidget):
    """A transparent child widget that paints a semi-transparent blue overlay."""
    def __init__(self, parent=None,q_color=None):
        super().__init__(parent)
        # let mouse events pass through to underlying widgets
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        # allow translucent background
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # make sure it's visible and stacked above siblings
        self.hide()
        self.q_color=q_color

    def paintEvent(self, event):
        # paint a translucent blue rectangle over the whole area
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), self.q_color)
        painter.end()

class SquareCell(QWidget):
    """A wrapper widget that keeps its contents square (equal width and height)."""

    # Signal to notify when a cell is clicked
    cellClicked = Signal(object)

    def __init__(self, date,refresh_function=None,database=None,border_right="None",border_left="None",border_top="None",border_bottom="None"):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.database=database
        self.date=date
        self.refresh_function=refresh_function

        # Create the scrollable widget if the date is valid for this month
        content_widget = ScrollableListWidget(parent=self,database=self.database,refresh_function=refresh_function)
        content_widget.setContentsMargins(0, 0, 0, 0)
        #content_widget.populateList(date)
        content_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(content_widget)

        self.content_widget = content_widget
        self.setContentsMargins(0, 0, 0, 0)
        self.setAttribute(Qt.WA_StyledBackground)

        # Update the SquareCell style to:
        self.border_right=border_right
        self.border_left=border_left
        self.border_top=border_top
        self.border_bottom=border_bottom

        self.setStyleSheet(f"""
        border-top: {self.border_top};
        border-left: {self.border_left};
        border-right: {self.border_right};
        border-bottom: {self.border_bottom};
        margin: 0px;
        padding: 0px;
        background-color: {ui_colors.getBackgroundColor()};
        """)

        weekDay = date.dayOfWeek()
        if (date==QDate.currentDate()):
            self._selection_overlay_special = SelectionOverlay(parent=self.content_widget.container_widget,q_color=ui_colors.getTodayOverlayColor())
            self._selection_overlay_special.setGeometry(self.content_widget.rect())
            self._selection_overlay_special.show()
            self.raise_child_elements(self._selection_overlay_special)



        elif (weekDay in [6,7]):
            self._selection_overlay_special = SelectionOverlay(parent=self.content_widget.container_widget,q_color=ui_colors.getWeekendOverlayColor())
            self._selection_overlay_special.setGeometry(self.rect())
            self._selection_overlay_special.show()
            self.raise_child_elements(self._selection_overlay_special)







        self._selection_overlay = SelectionOverlay(parent=self.content_widget.container_widget,q_color=ui_colors.getSelectionOverlayColor())
        self._selection_overlay.setGeometry(self.content_widget.rect())
        self.raise_child_elements(self._selection_overlay)


        # Track selection state
        self.is_selected = False

        # Apply initial style
        self.update_style()


    def resizeEvent(self, event):
        super().resizeEvent(event)
        # keep overlay covering entire cell
        self._selection_overlay.setGeometry(self.rect())



    def mousePressEvent(self, event):
        """Handle mouse click events"""
        if event.button() == Qt.LeftButton:
            # Emit signal to notify parent about click
            self.cellClicked.emit(self)

        super().mousePressEvent(event)

    def set_selected(self, selected: bool):
        """Set the selection state of this cell"""
        self.is_selected = selected
        self.update_style()

    def update_style(self):
        """Update the cell style based on selection state"""
        #self.content_widget.setStyleSheet(f"""
        #background-color: {ui_colors.getBackgroundColor()};
        #border-top: {self.border_top};
        #border-left: {self.border_left};
        #border-right: {self.border_right};
        #border-bottom: {self.border_bottom};
        #margin: 0px;
        #padding: 0px;
        #""")

        if (self.is_selected):
            self._selection_overlay.show()
            self.raise_child_elements(self._selection_overlay)
        else:
            self._selection_overlay.hide()

    def raise_child_elements(self,overlay):
        overlay.raise_()
        self.content_widget.header_label.raise_()

        for event in self.content_widget.events:
            event.raise_()


class CustomGridWidget(QWidget):
    def __init__(self, title="Monthly View", parent=None, database=None,refresh_function=None):
        super().__init__(parent)
        self.database = database
        self.title = title
        self.cells = []  # Store references to all cells
        self.current_selected_cell = None
        self.refresh_function=refresh_function
        current_date = QDate.currentDate()
        self.setup_ui(current_date)


    def setup_ui(self, current_date: QDate):
        """
        Set up the full UI for the monthly grid, including:
        - Title with month navigation arrows
        - 6x7 date grid
        """
        # Clear existing layout and widgets safely
        old_layout = self.layout()
        if old_layout:
            while old_layout.count():
                item = old_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
                elif item.layout():
                    sub_layout = item.layout()
                    while sub_layout.count():
                        sub_item = sub_layout.takeAt(0)
                        if sub_item.widget():
                            sub_item.widget().deleteLater()

            # Remove the old layout from the widget
            QWidget().setLayout(old_layout)

        self.cells = []
        self.current_selected_cell = None

        # ----------------- Main Layout -----------------
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # ----------------- Header with Arrows -----------------
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(4)

        # Left arrow
        left_btn = QPushButton("◀")
        left_btn.setFixedSize(32, 32)
        left_btn.clicked.connect(lambda: self.setup_ui(current_date.addMonths(-1)))

        # Title label
        title_label = QLabel(current_date.toString("MMMM yyyy"))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(f"""
            QLabel {{
                font-size: 16px;
                font-weight: bold;
                padding: 2px;
                margin: 0px;
                background-color: {ui_colors.getBackgroundColor()};
                border-left: 1px solid {ui_colors.getHeaderBorderColor()};
                border-right: 1px solid {ui_colors.getHeaderBorderColor()};
                border-top: 1px solid {ui_colors.getHeaderBorderColor()};
                color: {ui_colors.getTextColor()};
            }}
        """)
        title_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        title_label.setFixedHeight(40)

        # Right arrow
        right_btn = QPushButton("▶")
        right_btn.setFixedSize(32, 32)
        right_btn.clicked.connect(lambda: self.setup_ui(current_date.addMonths(1)))

        # Add arrows and title to header layout
        header_layout.addWidget(left_btn)
        header_layout.addWidget(title_label)
        header_layout.addWidget(right_btn)

        # ----------------- Add header to main layout -----------------
        main_layout.addLayout(header_layout)

        # ----------------- Grid Layout -----------------
        grid_layout = self.create_grid(current_date)
        main_layout.addLayout(grid_layout)

        # Refresh the cell contents for the new month
        self.refreshCells(main_month=current_date.month())


    def __setup_ui(self,current_date):
        self.cells = []  # Store references to all cells
        self.current_selected_cell = None

        # Main vertical layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)


        grid_layout=self.create_grid(current_date=current_date)

        # Title label
        title_label = QLabel(self.title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(f"""
             QLabel {{
                font-size: 16px;
                font-weight: bold;
                padding: 2px;
                /*border-radius: 4px;*/
                margin: 0px;
                background-color: {ui_colors.getBackgroundColor()};
                border-left: 1px solid {ui_colors.getHeaderBorderColor()};
                border-right: 1px solid {ui_colors.getHeaderBorderColor()};
                border-top: 1px solid {ui_colors.getHeaderBorderColor()};
                color: {ui_colors.getTextColor()};

            }}
        """)
        self.setStyleSheet(f"""
          CustomGridWidget {{
            margin: 0px;
            padding: 0px;
            background-color: {ui_colors.getBackgroundColor()};
        }}""")
        title_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        title_label.setFixedHeight(40)

        main_layout.addWidget(title_label)
        main_layout.addLayout(grid_layout)
        self.refreshCells(main_month=current_date.month())
        #main_layout.setStretch(0, 0)
        #main_layout.setStretch(1, 1)
    def on_cell_clicked(self, clicked_cell):
        """Handle cell click - single selection mode"""
        # Deselect previously selected cell
        if self.current_selected_cell:
            self.current_selected_cell.set_selected(False)

        # Select the clicked cell
        clicked_cell.set_selected(True)
        self.current_selected_cell = clicked_cell

    def refreshCells(self,main_month=None):
        #print("In refresh")

        for cell in self.cells:
            #print("Cell: ", str(cell.date))
            cell.content_widget.populateList(cell.date,main_month=main_month)


    def create_grid(self,current_date):
        # Grid layout for the 6x7 cells
        self.cells=[]
        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        # Add column headers (Days of the week)
        days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        for col, day in enumerate(days_of_week):
            day_label = QLabel(day)
            day_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            border_right = f"1px solid {ui_colors.getHeaderBorderColor()}"
            border_top = f"1px solid {ui_colors.getHeaderBorderColor()}"
            border_bottom = f"1px solid {ui_colors.getHeaderBorderColor()}"
            border_left = f"1px solid {ui_colors.getHeaderBorderColor()}" if (col==0) else "None"

            day_label.setStyleSheet(f"""QLabel {{
                font-weight: bold;
                background-color: {ui_colors.getBackgroundColor()};
                border-top: {border_top};
                border-left: {border_left};
                border-right: {border_right};
                border-bottom: {border_bottom};
                color: {ui_colors.getTextColor()};
            }}""")

            grid_layout.addWidget(day_label, 0, col)

        rows, cols = 6, 7
        # Determine the start date as the first Sunday before the current month

        # Determine the start date as the first Sunday before the current month
        for row in range(1,rows+1):
            grid_layout.setRowStretch(row, 1)
        for col in range(cols):
            grid_layout.setColumnStretch(col, 1)

        first_of_month = QDate(current_date.year(), current_date.month(), 1)
        start_date = first_of_month.addDays(-first_of_month.dayOfWeek()-7)  # Go back to the previous Sunday
        self.title=current_date.toString("MMMM yyyy")

        # Fill the grid with dates
        for row in range(1, rows + 1):  # Start from row 1 to leave space for the header
            for col in range(cols):
                # Ensure the date is within the 6x7 grid range, including previous and next months
                current_date = start_date.addDays(row * 7 + col)

                # Wrap it inside a square container

                border_right = f"1px solid {ui_colors.getBorderColor()}"
                border_left = f"1px solid {ui_colors.getBorderColor()}" if (col==0) else "None"
                border_top = "None"
                border_bottom = f"1px solid {ui_colors.getBorderColor()}"

                cell = SquareCell(current_date,refresh_function=self.refresh_function,database=self.database,border_right=border_right,border_left=border_left,border_top=border_top,border_bottom=border_bottom)



                cell.setContentsMargins(0, 0, 0, 0)  # Add this line
                cell.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                cell.sizePolicy().setHeightForWidth(True)
                cell.cellClicked.connect(self.on_cell_clicked)


                grid_layout.addWidget(cell, row, col)
                self.cells.append(cell)

        return grid_layout

    def change_month(self, delta, reference_date):
        """
        Move the calendar by delta months (-1 for previous, +1 for next)
        """
        # Update current_date
        self.current_date = self.current_date.addMonths(delta)

        # Re-run setup_ui with the new month
        self.setup_ui(self.current_date)


# Run example
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication, QMainWindow
    from database import Database

    app = QApplication(sys.argv)
    database = Database()
    database.openDB()

    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Monthly Calendar View")
            self.setGeometry(100, 100, 900, 700)
            grid_widget = CustomGridWidget(database=database)
            self.setCentralWidget(grid_widget)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
