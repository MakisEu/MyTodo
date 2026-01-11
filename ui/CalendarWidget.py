# This Python file uses the following encoding: utf-8
from PySide6 import QtCore
from PySide6 import QtWidgets


import sys
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette

class CalendarEventWidget(QWidget):
    def __init__(self, event_number: str, event_description: str):
        super().__init__()

        # Set up the main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)  # Set margins for the widget

        # Create the main dark gray frame
        dark_gray_frame = QFrame(self)
        dark_gray_frame.setStyleSheet("background-color: darkgray; border-radius: 10px;")
        dark_gray_frame.setFixedSize(200, 100)  # Set fixed size for the widget

        # Create a vertical layout for the dark gray frame
        dark_gray_layout = QVBoxLayout(dark_gray_frame)

        # Create the event number label
        number_label = QLabel(event_number, self)
        number_label.setStyleSheet("background-color: lightgray; color: darkgray; padding: 5px;")
        number_label.setAlignment(Qt.AlignRight)  # Align to the right

        # Create the event description label
        description_label = QLabel(event_description, self)
        description_label.setStyleSheet("background-color: lightgray; color: darkgray; padding: 5px;")
        description_label.setWordWrap(True)  # Allow text to wrap

        # Add the labels to the dark gray layout
        dark_gray_layout.addWidget(number_label)
        dark_gray_layout.addWidget(description_label)

        # Add the dark gray frame to the main layout
        main_layout.addWidget(dark_gray_frame)

        # Set the layout for the widget
        self.setLayout(main_layout)

# Example usage
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    # Create an instance of the CalendarEventWidget
    event_widget = CalendarEventWidget("10", "Greece: Orthodox Good Friday")
    event_widget.show()

    sys.exit(app.exec())

