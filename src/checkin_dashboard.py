# -*- coding: utf-8 -*-
import sys
from datetime import datetime, timedelta
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QApplication, QGraphicsView,
    QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem, QScrollArea,
    QFrame, QProgressBar, QPushButton
)
from PySide6.QtGui import QColor, QBrush, QFont, QPen
from PySide6.QtCore import Qt, QRectF, QDate


# ------------------------------------------------------------------
# UI Colors
# ------------------------------------------------------------------
class ui_colors:
    system_theme = "black"

    @staticmethod
    def getBackgroundColor():
        return "#202326" if ui_colors.system_theme == "black" else "#f5f5f5"

    @staticmethod
    def getTextColor():
        return "#ffffff" if ui_colors.system_theme == "black" else "#000000"

    @staticmethod
    def getSecondaryTextColor():
        return "#a3a3a3"

    @staticmethod
    def getHeatmapColor(level: int):
        """Return color intensity for heatmap based on level (0–5)"""
        if ui_colors.system_theme == "black":
            colors = ["#2c2c2c", "#3a5c3a", "#4a7f4a", "#60af60", "#80d080", "#a0f0a0"]
        else:
            colors = ["#e5e5e5", "#c0e0c0", "#90c090", "#60a060", "#409040", "#207020"]
        return colors[min(level, 5)]

    @staticmethod
    def getBorderColor():
        return "#aaaaaa" if ui_colors.system_theme == "black" else "#000000"


# ------------------------------------------------------------------
# Todo Object
# ------------------------------------------------------------------
class Todo:
    def __init__(self, name: str, start_date: str, end_date: str, date_created: str, id: int, tag: str):
        self.editTodo(name, start_date, end_date, tag)
        self.status = "Not Started"
        self.id = id
        self.date_created = date_created
        self.tag = tag

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

# ------------------------------------------------------------------
# Achievements Popup
# ------------------------------------------------------------------
class AchievementsPopup(QWidget):
    def __init__(self, achievements):
        super().__init__()
        self.setWindowTitle("Achievements")
        layout = QVBoxLayout(self)
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        container = QWidget()
        container_layout = QVBoxLayout(container)

        for a in achievements:
            frame = QFrame()
            frame.setFrameShape(QFrame.StyledPanel)
            frame.setStyleSheet(f"background-color:{ui_colors.getBackgroundColor()}; border: 1px solid {ui_colors.getBorderColor()};")
            vbox = QVBoxLayout(frame)
            label = QLabel(a["title"])
            label.setStyleSheet(f"color:{ui_colors.getTextColor()}")
            progress = QProgressBar()
            progress.setMaximum(a["target"])
            progress.setValue(a["progress"])
            progress.setTextVisible(True)
            vbox.addWidget(label)
            vbox.addWidget(progress)
            container_layout.addWidget(frame)

        scroll.setWidget(container)
        layout.addWidget(scroll)
        self.resize(600, 400)

# ------------------------------------------------------------------
# Dashboard Widget
# ------------------------------------------------------------------
class TodoDashboard(QWidget):
    WEEKDAYS = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

    def __init__(self, todos):
        super().__init__()
        self.todos = todos
        self.daily_checkins = {}  # date_str -> completed_todo_count
        self.current_year = datetime.now().year
        self.achievements = []
        self.setWindowTitle("Todo Dashboard")
        self.setStyleSheet(f"background-color:{ui_colors.getBackgroundColor()}; color:{ui_colors.getTextColor()}")
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(15)

        # Daily Check-in / Streak
        self.checkin_label = QLabel()
        self.layout.addWidget(self.checkin_label)

        # Heatmap scene
        self.heatmap_scene = QGraphicsScene()
        self.heatmap_view = QGraphicsView(self.heatmap_scene)
        self.heatmap_view.setFixedHeight(150)
        self.layout.addWidget(self.heatmap_view)

        # Heatmap navigation
        nav_layout = QHBoxLayout()
        self.prev_year_btn = QPushButton("<")
        self.next_year_btn = QPushButton(">")
        self.year_label = QLabel(str(self.current_year))
        self.year_label.setAlignment(Qt.AlignCenter)
        self.prev_year_btn.clicked.connect(self.prev_year)
        self.next_year_btn.clicked.connect(self.next_year)
        nav_layout.addWidget(self.prev_year_btn)
        nav_layout.addWidget(self.year_label)
        nav_layout.addWidget(self.next_year_btn)
        self.layout.addLayout(nav_layout)

        # Achievements button
        self.achievements_btn = QPushButton("Show Achievements")
        self.achievements_btn.clicked.connect(self.show_achievements)
        self.layout.addWidget(self.achievements_btn)

        # Initialize
        self.process_checkins()
        self.update_checkin_label()
        self.draw_heatmap()

    # -------------------------
    # Process todos to mark daily completions
    # -------------------------
    def process_checkins(self):
        for todo in self.todos:
            if todo.getStatus() == "Completed":
                date_str = todo.getEndDate()  # assuming format "YYYY-MM-DD"
                if date_str not in self.daily_checkins:
                    self.daily_checkins[date_str] = 0
                self.daily_checkins[date_str] += 1

    # -------------------------
    # Daily Check-in logic
    # -------------------------
    def check_in_today(self):
        today_str = datetime.now().strftime("%Y-%m-%d")
        if today_str not in self.daily_checkins:
            self.daily_checkins[today_str] = 0
        self.update_checkin_label()

    def current_streak(self):
        streak = 0
        today = datetime.now()
        while True:
            day_str = today.strftime("%Y-%m-%d")
            if self.daily_checkins.get(day_str, 0) > 0:
                streak += 1
            else:
                break
            today -= timedelta(days=1)
        return streak

    def update_checkin_label(self):
        streak = self.current_streak()
        last_date = max(self.daily_checkins.keys(), default="N/A")
        self.checkin_label.setText(f"Current streak: {streak} days | Last check-in: {last_date}")
        self.checkin_label.setStyleSheet(f"font-size:16px; color:{ui_colors.getTextColor()}")

    # -------------------------
    # Heatmap logic (horizontal)
    # -------------------------
    def draw_heatmap(self):
        self.heatmap_scene.clear()
        cell_size = 15
        padding = 2
        first_day = datetime(self.current_year,1,1)
        last_day = datetime(self.current_year,12,31)
        day = first_day

        week = 0
        month_labels_drawn = {}
        while day <= last_day:
            day_of_week = day.weekday()
            x = week * (cell_size + padding) + 30  # offset for weekdays labels
            y = day_of_week * (cell_size + padding) + 20  # offset for month labels
            day_str = day.strftime("%Y-%m-%d")
            count = self.daily_checkins.get(day_str, 0)
            color = QColor(ui_colors.getHeatmapColor(min(count,5)))

            rect = QGraphicsRectItem(x, y, cell_size, cell_size)
            rect.setBrush(QBrush(color))
            rect.setPen(QPen(ui_colors.getBorderColor()))
            rect.setToolTip(f"{day_str}: {count} completed")
            self.heatmap_scene.addItem(rect)

            # Month label
            if day.month not in month_labels_drawn:
                month_x = x
                label_item = QGraphicsTextItem(day.strftime("%b"))
                label_item.setDefaultTextColor(QColor(ui_colors.getTextColor()))
                label_item.setFont(QFont("Segoe UI", 10))
                label_item.setPos(month_x, 0)
                self.heatmap_scene.addItem(label_item)
                month_labels_drawn[day.month] = True

            day += timedelta(days=1)
            if day.weekday() == 0:
                week += 1

        # Weekday labels
        for i, wd in enumerate(self.WEEKDAYS):
            label_item = QGraphicsTextItem(wd)
            label_item.setDefaultTextColor(QColor(ui_colors.getTextColor()))
            label_item.setFont(QFont("Segoe UI", 10))
            label_item.setPos(0, i*(cell_size+padding)+20)
            self.heatmap_scene.addItem(label_item)

        # Scene rect
        self.heatmap_scene.setSceneRect(0,0, (week+1)*(cell_size+padding)+50, 7*(cell_size+padding)+30)

    # -------------------------
    # Heatmap year navigation
    # -------------------------
    def prev_year(self):
        self.current_year -= 1
        self.year_label.setText(str(self.current_year))
        self.draw_heatmap()

    def next_year(self):
        self.current_year += 1
        self.year_label.setText(str(self.current_year))
        self.draw_heatmap()

    # -------------------------
    # Achievements popup
    # -------------------------
    def show_achievements(self):
        self.popup = AchievementsPopup(self.achievements)
        self.popup.show()


# -------------------------
# Demo
# -------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Example todos
    todos = [
        Todo("Finish math homework", "2026-01-03", "2026-01-03", "2026-01-01", 1, "Education"),
        Todo("Clean desk", "2026-01-03", "2026-01-03", "2026-01-02", 2, "Personal"),
        Todo("Read physics notes", "2026-01-02", "2026-01-02", "2026-01-02", 3, "School"),
    ]
    for t in todos:
        t.updateStatus("Completed")

    dashboard = TodoDashboard(todos)
    dashboard.achievements = [
        {"title": "First Todo", "progress": 1, "target": 1, "description": "Complete your first todo"},
        {"title": "Week Streak", "progress": 2, "target": 7, "description": "Complete todos 7 days in a row"},
        {"title": "Monthly Master", "progress": 10, "target": 30, "description": "Complete 30 todos this month"},
    ]
    dashboard.resize(900, 500)
    dashboard.show()
    sys.exit(app.exec())
