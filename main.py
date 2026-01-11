# This Python file uses the following encoding: utf-8
import sys
import rc_assets
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QCoreApplication

from src.MainWindow import MainWindow


if __name__ == "__main__":
    QCoreApplication.setOrganizationName("MakisApps")
    #QCoreApplication.setOrganizationDomain("mysoft.com")
    QCoreApplication.setApplicationName("MyTodo")
    app = QApplication(sys.argv)

    # Create and show the ToDoApp window
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
