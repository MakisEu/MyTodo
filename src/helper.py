# This Python file uses the following encoding: utf-8
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QStandardPaths, QFile, Qt
from PySide6.QtWidgets import QFileDialog
from PySide6.QtGui import QPixmap, QPainter, QColor, QImage

import re

def loadUiWidget(uifilename, parent=None):
    loader = QUiLoader()
    uifile = QFile(uifilename)
    uifile.open(QFile.ReadOnly)
    ui = loader.load(uifile, parent)
    uifile.close()
    return ui

def replace(s,toReplace,replaceWith):
    s=s.replace(toReplace,replaceWith)

def refreshTodos(model):
    pass

def get_save_filename_with_suffix(parent=None,fileDialogText="Save iCalendar File", defaultSuffix="ics", nameFilter="iCalendar Files (*.ics)",selectedFile="todos.ics"):
    # Create a QFileDialog instance instead of using static method
    dialog = QFileDialog(parent, fileDialogText)

    # Set the default suffix
    dialog.setDefaultSuffix(defaultSuffix)

    # Configure the dialog
    dialog.setAcceptMode(QFileDialog.AcceptSave)
    dialog.setNameFilter(nameFilter)

    # Set default directory and filename
    dialog.selectFile(selectedFile)  # Default filename

    if dialog.exec() == QFileDialog.Accepted:
        file_path = dialog.selectedFiles()[0]
        return file_path
    return ""
def get_load_filename_with_suffix(parent=None,fileDialogText="Load iCalendar File", defaultSuffix="ics", nameFilter="iCalendar Files (*.ics)",selectedFile="todos.ics"):
    # Create a QFileDialog instance instead of using static method
    dialog = QFileDialog(parent, fileDialogText)

    # Set the default suffix
    dialog.setDefaultSuffix(defaultSuffix)

    # Configure the dialog
    dialog.setAcceptMode(QFileDialog.AcceptOpen)
    dialog.setNameFilter(nameFilter)

    # Set default directory and filename
    dialog.selectFile(selectedFile)  # Default filename

    if dialog.exec() == QFileDialog.Accepted:
        file_path = dialog.selectedFiles()[0]
        return file_path
    return ""

def check_todo_format(string):
    # Regular expression for "TODO-" followed by one or more digits
    pattern = r"^todo-\d+$"

    if re.match(pattern, string):
        return True
    return False

def emoji_badge(emoji: str, size: int, locked: bool) -> QPixmap:
    base = QPixmap(size, size)
    base.fill(Qt.transparent)

    painter = QPainter(base)
    font = painter.font()
    font.setPointSize(int(size * 0.8))
    painter.setFont(font)
    painter.drawText(base.rect(), Qt.AlignCenter, emoji)
    painter.end()

    if not locked:
        return base

    # ---- Convert emoji to PURE BLACK using alpha mask ----
    black = QPixmap(size, size)
    black.fill(Qt.transparent)

    painter = QPainter(black)
    painter.setCompositionMode(QPainter.CompositionMode_Source)
    painter.fillRect(black.rect(), Qt.black)

    painter.setCompositionMode(QPainter.CompositionMode_DestinationIn)
    painter.drawPixmap(0, 0, base)
    painter.end()

    return black

from datetime import datetime, timedelta
from typing import List, Tuple, Dict

from datetime import datetime, timedelta
from typing import Dict

def calculate_max_streak(daily: Dict[str, int]) -> int:
    """
    Calculate the maximum consecutive streak of days with completed todos.

    Args:
        daily: Dict mapping date strings ("dd/mm/yyyy") to completed count (int).

    Returns:
        max_streak: int
    """
    if not daily:
        return 0

    # Convert keys to datetime.date objects
    dates = sorted(datetime.strptime(d, "%d/%m/%Y").date() for d, count in daily.items() if count > 0)
    if not dates:
        return 0

    max_streak = 1
    current_streak = 1

    for i in range(1, len(dates)):
        # Check if consecutive day
        if dates[i] == dates[i-1] + timedelta(days=1):
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 1

    return max_streak



if __name__ == "__main__":
    import sys
    #app = QtGui.QApplication(sys.argv)
    #MainWindow = loadUiWidget(":/forms/myform.ui")
    #MainWindow.show()
    #sys.exit(app.exec_())
