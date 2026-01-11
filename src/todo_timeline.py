# -*- coding: utf-8 -*-
import sys
from datetime import datetime, timedelta
from PySide6.QtWidgets import (
    QWidget, QApplication, QVBoxLayout, QHBoxLayout, QLabel,
    QGraphicsView, QGraphicsScene, QGraphicsRectItem,
    QGraphicsEllipseItem, QGraphicsTextItem,
    QPushButton, QScrollArea, QFrame, QProgressBar, QGridLayout
)
from PySide6.QtGui import QColor, QBrush, QFont, QPen, QPainter, QFontMetrics
from PySide6.QtCore import Qt, QRectF, QDateTime
from src.todo import Todo
from src.ui_colors import ui_colors
from src.achievement import Achievement
from src.helper import emoji_badge, calculate_max_streak

# ================================================================
# TIMELINE
# ================================================================
class CompletedTimeline(QFrame):
    SPACING = 180
    DOT_R = 8

    def __init__(self):
        super().__init__()
        self.setObjectName("CompletedTimeline")
        self.setStyleSheet(f"""
            QFrame#CompletedTimeline {{
                background: {ui_colors.getBackgroundColor()};
                border: 1px solid {ui_colors.getBorderColor()};
                border-radius: 12px;
            }}
        """)
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setStyleSheet("border:none;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(self.view)

    def setTodos(self, todos):
        todos_ = [
            t for t in todos
            if t.getStatus() == "Completed" and
            QDateTime.fromString(t.date_completed, "dd/MM/yyyy hh:mm")
            <= QDateTime.currentDateTime()
        ]
        self.rebuild(todos_)

    #def resizeEvent(self, e):
    #    self.rebuild()

    def rebuild(self,todos):
        self.scene.clear()

        y = self.height() // 2
        x = 100
        dot_positions = []
        max_title_width=140

        # ----- Draw all completed todos -----
        for t in todos:
            dot_positions.append(x)

            # Completed dot
            dot = QGraphicsEllipseItem(QRectF(x - self.DOT_R, y - self.DOT_R,
                                              self.DOT_R * 2, self.DOT_R * 2))
            dot.setBrush(QBrush(QColor(ui_colors.getGreenIndicator())))
            dot.setPen(Qt.NoPen)
            dot.setToolTip(f"{t.getName()}\n{t.date_completed} • {t.getTag()}")
            self.scene.addItem(dot)

            # Task title

            font = QFont("Segoe UI", 10, QFont.Bold)
            fm = QFontMetrics(font)
            title_text = t.getName()
            elided_text = fm.elidedText(title_text, Qt.ElideRight, max_title_width)

            title = QGraphicsTextItem(elided_text)
            title.setFont(font)
            title.setDefaultTextColor(QColor(ui_colors.getTextColor()))
            # Center title above dot
            title.setTextWidth(max_title_width)
            title.setPos(x - max_title_width/2, y - 48)
            self.scene.addItem(title)

            # Task date
            date = QGraphicsTextItem(t.date_completed)
            date.setFont(QFont("Segoe UI", 8))
            date.setDefaultTextColor(QColor(ui_colors.getNonMonthTextColor()))
            date.setPos(x - 70, y + 20)
            self.scene.addItem(date)

            x += self.SPACING

        # ----- Timeline line -----
        pen = QPen(QColor(ui_colors.getBorderColor()))
        pen.setWidth(2)

        if dot_positions:
            # Extend line to include present marker
            present_x = x
            self.scene.addLine(dot_positions[0] - 60, y,
                               present_x, y, pen)
        else:
            # No completed todos: draw a line from start to present
            present_x = x
            self.scene.addLine(present_x - self.SPACING, y,
                               present_x, y, pen)

        # ----- Present marker (prettier) -----
        present_x = x
        outer_r = self.DOT_R + 6
        inner_r = self.DOT_R - 1
        accent = QColor(ui_colors.getGreenIndicator())

        # Outer ring
        outer = QGraphicsEllipseItem(
            QRectF(
                present_x - outer_r,
                y - outer_r,
                outer_r * 2,
                outer_r * 2
            )
        )
        outer.setBrush(Qt.NoBrush)
        outer_pen = QPen(accent)
        outer_pen.setWidth(2)
        outer.setPen(outer_pen)
        outer.setOpacity(0.5)
        self.scene.addItem(outer)

        # Inner dot
        inner = QGraphicsEllipseItem(
            QRectF(
                present_x - inner_r,
                y - inner_r,
                inner_r * 2,
                inner_r * 2
            )
        )
        inner.setBrush(QBrush(accent))
        inner.setPen(Qt.NoPen)
        inner.setToolTip("Present moment")
        self.scene.addItem(inner)

        # Label
        present_label = QGraphicsTextItem("Now")
        present_label.setFont(QFont("Segoe UI", 9, QFont.Bold))
        present_label.setDefaultTextColor(QColor(ui_colors.getNonMonthTextColor()))
        present_label.setPos(present_x - 16, y - 52)
        self.scene.addItem(present_label)

        # ----- Update scene rect -----
        self.scene.setSceneRect(0, 0, present_x + 100, self.height())


# ================================================================
# CHECK-IN PANEL
# ================================================================
class CheckinPanel(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("CheckinPanel")
        self.setStyleSheet(f"""
            QFrame#CheckinPanel {{
                background: {ui_colors.getBackgroundColor()};
                border: 1px solid {ui_colors.getBorderColor()};
                border-radius: 12px;
            }}

            QFrame#CheckinPanel * {{
                border: none;
            }}

            QLabel {{
                color: {ui_colors.getTextColor()};
            }}
        """)


        self.setFixedSize(380, 200)

        # ----------------- Header -----------------
        header_layout = QHBoxLayout()

        # Check-in indicator
        self.checkin_indicator = QLabel()
        self.checkin_indicator.setFixedSize(24, 24)
        self.checkin_indicator.setStyleSheet(f"""
            background: transparent;
            border-radius: 12px;

        """)

        checkin_title = QLabel("Daily Check-in")
        checkin_title.setFont(QFont("Segoe UI", 10, QFont.Bold))

        header_layout.addWidget(self.checkin_indicator)
        header_layout.addSpacing(8)
        header_layout.addWidget(checkin_title)
        header_layout.addStretch()

        # Add streak counter to top-right
        self.streak_label = QLabel("0🔥")
        self.streak_label.setObjectName("streak_label")
        self.streak_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.streak_label.setToolTip("0-day streak")
        header_layout.addWidget(self.streak_label)

        # ----------------- Progress Grid -----------------
        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(8)
        grid_layout.setVerticalSpacing(6)

        self.day_labels = []
        self.day_indicators = []

        # Add day labels and progress indicators
        days = ["M", "T", "W", "T", "F", "S", "S"]
        for i, day in enumerate(days):
            # Day label
            lbl = QLabel(day)
            lbl.setFont(QFont("Segoe UI", 8))
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet(f"color: {ui_colors.getNonMonthTextColor()};")
            grid_layout.addWidget(lbl, 0, i)
            self.day_labels.append(lbl)

            # Progress indicator - SQUARE style
            indicator = QLabel()
            indicator.setFixedSize(24, 24)
            indicator.setStyleSheet(f"""
                background: transparent;
            """)
            grid_layout.addWidget(indicator, 1, i, Qt.AlignCenter)
            self.day_indicators.append(indicator)

        # ----------------- Footer -----------------
        footer_layout = QVBoxLayout()
        footer_layout.setContentsMargins(0, 8, 0, 0)
        footer_layout.setSpacing(4)

        self.last_activity = QLabel("Last activity: —")
        self.last_activity.setFont(QFont("Segoe UI", 8))
        self.last_activity.setStyleSheet(f"color: {ui_colors.getNonMonthTextColor()};")

        self.tip_message = QLabel()
        self.tip_message.setFont(QFont("Segoe UI", 9))
        self.tip_message.setStyleSheet(f"color: {ui_colors.getTextColor()}; font-style: italic;")
        self.tip_message.setWordWrap(True)

        footer_layout.addWidget(self.last_activity)
        footer_layout.addWidget(self.tip_message)

        # ----------------- Main Layout -----------------
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 12, 16, 12)
        main_layout.setSpacing(12)
        main_layout.addLayout(header_layout)
        main_layout.addLayout(grid_layout)
        main_layout.addLayout(footer_layout)

    def update(self, daily: dict):
        """Update the check-in panel based on daily completion data."""
        today_dt = datetime.now()
        today_str = today_dt.strftime("%d/%m/%Y")
        completed_today = daily.get(today_str, 0) > 0

        # ----------------- Check-in indicator -----------------
        self.checkin_indicator.setStyleSheet(f"""
            background: {ui_colors.getGreenIndicator() if completed_today else ui_colors.getBorderColor()};
            border-radius: 12px;
        """)

        # ----------------- Streak calculation -----------------
        streak = 0
        d = today_dt

        # If today is not completed, start counting from yesterday
        if not completed_today:
            d -= timedelta(days=1)

        # Count consecutive completed days backwards
        while daily.get(d.strftime("%d/%m/%Y"), 0) > 0:
            streak += 1
            d -= timedelta(days=1)

        # Update streak label
        self.streak_label.setText(f"{streak}🔥")
        self.streak_label.setToolTip(f"{streak}-day streak")

        # ----------------- Weekly progress grid -----------------
        # Show current week: Monday → Sunday
        start_of_week = today_dt - timedelta(days=today_dt.weekday())  # Monday
        for i in range(7):
            day_dt = start_of_week + timedelta(days=i)
            day_str = day_dt.strftime("%d/%m/%Y")
            completed = daily.get(day_str, 0) > 0

            bg_color = ui_colors.getGreenIndicator() if completed else ui_colors.getBorderColor()
            self.day_indicators[i].setStyleSheet(f"""
                background: {bg_color};
            """)

        # ----------------- Footer -----------------
        last_activity = max(daily.keys(), default="—")
        self.last_activity.setText(f"Last activity: {last_activity}")

        if completed_today:
            self.tip_message.setText("Great job! You've completed today's check-in.")
        else:
            self.tip_message.setText("Complete a small task today to check-in!")

    # ================================================================
# HEATMAP
# ================================================================
class Heatmap(QFrame):
    WEEKDAYS = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

    def __init__(self):
        super().__init__()
        self.setObjectName("Heatmap")
        self.setStyleSheet(f"""
            QFrame#Heatmap {{
                background: {ui_colors.getBackgroundColor()};
                border: 1px solid {ui_colors.getBorderColor()};
                border-radius: 12px;
            }}
        """)

        self.year = datetime.now().year
        self.daily = {}

        # ---------- Graphics ----------
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setStyleSheet("border: none; background: transparent;")

        # ---------- Year controls ----------
        controls = QHBoxLayout()
        controls.setContentsMargins(0, 0, 0, 0)

        self.prev_btn = QPushButton("◀")
        self.next_btn = QPushButton("▶")
        self.year_label = QLabel(str(self.year))
        self.year_label.setAlignment(Qt.AlignCenter)
        self.year_label.setStyleSheet(f"color:{ui_colors.getTextColor()};")

        self.prev_btn.clicked.connect(self.prev_year)
        self.next_btn.clicked.connect(self.next_year)

        controls.addStretch()
        controls.addWidget(self.prev_btn)
        controls.addSpacing(10)
        controls.addWidget(self.year_label)
        controls.addSpacing(10)
        controls.addWidget(self.next_btn)
        controls.addStretch()

        # ---------- Layout ----------
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.view)
        layout.addLayout(controls)
        self.setFixedHeight(160 + 28)  # heatmap + controls

    # ---------- Public API ----------
    def setDaily(self, daily: dict):
        self.daily = daily
        self.draw()

    # ---------- Year navigation ----------
    def prev_year(self):
        self.year -= 1
        self.draw()
        self.year_label.setText(str(self.year))

    def next_year(self):
        self.year += 1
        self.year_label.setText(str(self.year))
        self.draw()

    # ---------- Drawing ----------
    def draw(self):
        self.scene.clear()
        size, pad = 14, 2

        # Weekday labels
        for i, wd in enumerate(self.WEEKDAYS):
            t = QGraphicsTextItem(wd)
            t.setDefaultTextColor(QColor(ui_colors.getTextColor()))
            t.setPos(0, i * (size + pad) + 20)
            self.scene.addItem(t)

        day = datetime(self.year, 1, 1)
        week = 0
        seen_months = set()

        while day.year == self.year:
            dow = day.weekday()
            x = week * (size + pad) + 30
            y = dow * (size + pad) + 20

            date_str = day.strftime("%d/%m/%Y")
            freq = self.daily.get(date_str, 0)

            r = QGraphicsRectItem(x, y, size, size)
            r.setBrush(QBrush(QColor(ui_colors.heat(freq))))
            r.setPen(Qt.NoPen)
            r.setToolTip(f"{date_str}: {freq}")
            self.scene.addItem(r)

            if day.month not in seen_months:
                m = QGraphicsTextItem(day.strftime("%b"))
                m.setDefaultTextColor(QColor(ui_colors.getTextColor()))
                m.setPos(x, 0)
                self.scene.addItem(m)
                seen_months.add(day.month)

            day += timedelta(days=1)
            if day.weekday() == 0:
                week += 1

# ================================================================
# ACHIEVEMENTS POPUP
# ================================================================
class AchievementsPopup(QWidget):
    def __init__(self, achievements):
        super().__init__()
        self.setWindowTitle("Achievements")
        self.resize(640, 420)

        # --- Scroll area (persistent) ---
        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)

        # --- Container widget ---
        self.container = QWidget()
        self.grid = QGridLayout(self.container)
        self.grid.setSpacing(12)

        self.scroll.setWidget(self.container)

        # --- Main layout ---
        layout = QVBoxLayout(self)
        layout.addWidget(self.scroll)

        self.refresh(achievements)
        self.setAttribute(Qt.WA_DeleteOnClose)


    def refresh(self, achievements: list[Achievement]):
        """Rebuild the achievements grid using Achievement objects"""

        # Clear existing cards
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Rebuild grid
        for i, achievement in enumerate(achievements):
            card = QFrame()
            card.setFixedSize(180, 130)
            card.setStyleSheet(f"""
                background: {ui_colors.getBackgroundColor()};
                border: 1px solid {ui_colors.getBorderColor()};
                border-radius: 8px;
            """)

            v = QVBoxLayout(card)
            v.setSpacing(4)
            v.setAlignment(Qt.AlignCenter)


            # -------- Badge --------
            badge = QLabel()
            badge.setFixedSize(40, 40)
            badge.setAlignment(Qt.AlignCenter)

            badge.setStyleSheet("""
                QLabel {
                    border: none;
                    background: transparent;
                }
            """)

            badge.setPixmap(emoji_badge("🏅", 40, locked=not achievement.unlocked))




            if achievement.unlocked:
                badge.setToolTip(f"Unlocked on {achievement.date_unlocked}")
            else:
                # visually "locked" badge
                badge.setToolTip("Achievement not unlocked")

            # -------- Title --------
            title = QLabel(achievement.title or "")
            title.setAlignment(Qt.AlignCenter)
            title.setWordWrap(True)
            title.setStyleSheet(f"""
                color: {ui_colors.getTextColor()};
                font-weight: bold;
                font-size: 11px;
            """)

            # -------- Description --------
            desc = QLabel(achievement.description or "")
            desc.setAlignment(Qt.AlignCenter)
            desc.setWordWrap(True)
            desc.setStyleSheet(f"""
                color: {ui_colors.getSecondaryTextColor()};
                font-size: 9px;
            """)

            # -------- Progress --------
            bar = QProgressBar()
            bar.setRange(0, 100)
            bar.setValue(int(achievement.percentage_done or 0))
            bar.setFormat(f"{int(achievement.percentage_done or 0)}%")
            bar.setAlignment(Qt.AlignCenter)
            bar.setFixedHeight(10)
            bar.setStyleSheet("""
            QProgressBar {
                background-color: #1f1f1f;
                border-radius: 5px;
                border: none;
                color: white;
                font-size: 9px;
            }

            QProgressBar::chunk {
                background-color: #d4af37;
                border-radius: 5px;
            }
            """)

            bar.setTextVisible(True)

            # -------- Assemble --------
            v.addWidget(badge, alignment=Qt.AlignHCenter)
            v.addWidget(title)
            v.addWidget(desc)
            v.addWidget(bar)

            self.grid.addWidget(card, i // 3, i % 3)

    @staticmethod
    def updateAchivements(database,daily):
        achievements=database.getAllAchievements()

        max_streak=calculate_max_streak(daily)
        total_completed=sum(list(daily.values()))
        date = QDateTime.currentDateTime().toString("dd/MM/yyyy hh:mm")

        changed_achievements=[]

        for achievement in achievements:
            previous_progress=achievement.current_progress
            if ("TOTAL_TODOS" in achievement.code_id and achievement.unlocked==0):

                if (total_completed>=int(achievement.goal)):
                    achievement.current_progress=achievement.goal
                    achievement.unlocked=1
                    achievement.date_unlocked=date
                    achievement.percentage_done=100
                    changed_achievements.append(achievement)

                elif(total_completed>int(previous_progress)):
                    achievement.current_progress=str(total_completed)
                    achievement.percentage_done=round((int(achievement.current_progress)/int(achievement.goal))*100)
                    print(int(achievement.current_progress), total_completed, achievement.percentage_done)
                    changed_achievements.append(achievement)

            elif ("MAX_STREAK" in achievement.code_id and achievement.unlocked==0):

                if (max_streak>=int(achievement.goal)):
                    achievement.current_progress=achievement.goal
                    achievement.unlocked=1
                    achievement.date_unlocked=date
                    achievement.percentage_done=100
                    changed_achievements.append(achievement)

                elif(max_streak>int(previous_progress)):
                    achievement.current_progress=str(max_streak)
                    achievement.percentage_done=round((int(achievement.current_progress)/int(achievement.goal))*100)
                    changed_achievements.append(achievement)

        # code_id, current_progress, unlocked, date_unlocked, percentage_done
        for achievement in changed_achievements:
            database.update_achivement(achievement)
# ================================================================
# DASHBOARD
# ================================================================
class TodoDashboard(QWidget):
    def __init__(self,database, todos=[],parent=None):
        super().__init__(parent)
        self.database=database
        self.parent=parent
        self.todos = todos
        self.year = datetime.now().year
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.setStyleSheet(f"background:{ui_colors.getBackgroundColor()}")
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        self.timeline = CompletedTimeline()
        self.timeline.setFixedHeight(220)
        layout.addWidget(self.timeline)

        self.checkin = CheckinPanel()
        layout.addWidget(self.checkin, alignment=Qt.AlignHCenter)

        self.heatmap = Heatmap()
        layout.addWidget(self.heatmap)

        self.achievements_btn = QPushButton("🏆 View Achievements")
        self.achievements_btn.clicked.connect(self.show_achievements)
        layout.addWidget(self.achievements_btn, alignment=Qt.AlignRight)

        self.process(todos)

    def process(self, todos):
        self.todos = todos
        self.timeline.setTodos(self.todos)

        daily = {}
        for t in self.todos:
            if t.getStatus() == "Completed":
                date = datetime.strptime(
                    t.date_completed, "%d/%m/%Y %H:%M").strftime("%d/%m/%Y")
                daily[date] = daily.get(date, 0) + 1

        self.checkin.update(daily)
        self.heatmap.setDaily(daily)
        AchievementsPopup.updateAchivements(self.database,daily)


    def show_achievements(self):
        #self.popup = AchievementsPopup([
        #    {"title":"First Todo","progress":1,"target":1},
        #    {"title":"7-Day Streak","progress":5,"target":7},
        #    {"title":"100 Todos","progress":32,"target":100},
        #])
        self.popup = AchievementsPopup(self.database.getAllAchievements())
        self.popup.show()


# ================================================================
# DEMO
# ================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    todos = []
    for i in range(10):
        t = Todo(
            f"Task {i+1}",
            (datetime.now()-timedelta(days=i)).strftime("%d/%m/%Y"),
            "Demo"
        )
        t.updateStatus("Completed")
        todos.append(t)

    w = TodoDashboard(todos)
    w.resize(1000, 900)
    w.show()
    sys.exit(app.exec())

