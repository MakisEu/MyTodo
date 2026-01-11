# This Python file uses the following encoding: utf-8

class Achievement:
    def __init__(self, code_id=None, title=None, description=None, goal=None, current_progress=None, unlocked=None, date_unlocked=None, percentage_done=None):
        self.code_id=code_id
        self.title=title
        self.description=description
        self.goal=goal
        self.current_progress=current_progress
        self.unlocked=unlocked
        self.date_unlocked=date_unlocked
        self.percentage_done=percentage_done
