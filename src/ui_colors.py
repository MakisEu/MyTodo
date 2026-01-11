# This Python file uses the following encoding: utf-8
from PySide6.QtGui import QColor


class ui_colors:
    system_theme="black"
    @staticmethod
    def getBackgroundColor():
        if (ui_colors.system_theme=="black"):
            return "#202326"
        if (ui_colors.system_theme=="white"):
            return "#d3d3d3"
    @staticmethod
    def getTextColor():
        if (ui_colors.system_theme=="black"):
            return "#ffffff"
        if (ui_colors.system_theme=="white"):
            return "#000000"
    @staticmethod
    def getBorderColor():
        if (ui_colors.system_theme=="black"):
            return "#aaaaaa"
        if (ui_colors.system_theme=="white"):
            return "#000000"
    @staticmethod
    def getHeaderBorderColor():
        if (ui_colors.system_theme=="black"):
            return "#aaaaaa"
        if (ui_colors.system_theme=="white"):
            return "#000000"
    @staticmethod
    def getScrollAreaColor():
        if (ui_colors.system_theme=="black"):
            return "#2c2c2c"
        if (ui_colors.system_theme=="white"):
            return "#d3d3d3"
    @staticmethod
    def getDayTitleBackgroundColor():
        if (ui_colors.system_theme=="black"):
            return "#292c30"
        if (ui_colors.system_theme=="white"):
            return "#58c9c7"
    @staticmethod
    def getSelectionOverlayColor():
        if (ui_colors.system_theme=="black"):
            return  QColor(0, 120, 215, 80) # #204051
        if (ui_colors.system_theme=="white"):
            return  QColor(0, 120, 215, 80) # #204051
    @staticmethod
    def getTodayOverlayColor():
        if (ui_colors.system_theme=="black"):
            return  QColor(0x60, 0xAF, 0x62, 100) # #182c1b
        if (ui_colors.system_theme=="white"):
            return  QColor(0x60, 0xAF, 0x62, 100) # #182c1b
    @staticmethod
    def getWeekendOverlayColor():
        if (ui_colors.system_theme=="black"):
            return  QColor(124, 125, 127, 70) # #1d1f22
        if (ui_colors.system_theme=="white"):
            return  QColor(124, 125, 127, 70) # #1d1f22
    @staticmethod
    def getEventColor():
        if (ui_colors.system_theme=="black"):
            return "#c1d4e7"
        if (ui_colors.system_theme=="white"):
            return "#c1d4e7"
    @staticmethod
    def getEventTextColor():
        if (ui_colors.system_theme=="black"):
            return "#111315"
        if (ui_colors.system_theme=="white"):
            return "#c1d4e7"
    @staticmethod
    def getNonMonthTextColor():
        if (ui_colors.system_theme=="black"):
            return "#a3a3a3"
        if (ui_colors.system_theme=="white"):
            return "#a3a3a3"
    @staticmethod
    def getTimelineLineColor():
        return ui_colors.getBorderColor()

    @staticmethod
    def getTimelineDotColor():
        if ui_colors.system_theme == "black":
            return "#60af62"
        return "#3a9d23"

    @staticmethod
    def getSecondaryTextColor():
        return ui_colors.getNonMonthTextColor()

    @staticmethod
    def getCompletedTodoColor():
        return "#16DB65"
    @staticmethod
    def getMissedTodoColor():
        return "#E92C2C"
    def getGreenIndicator():
        return "#60af62"
    @staticmethod
    def heat(level):
        colors = ["#2c2c2c", "#355c35", "#4a7f4a",
                  "#60af60", "#80d080", "#a0f0a0"]
        return colors[min(level, 5)]


if __name__ == "__main__":
    print(ui_colors.getBackgroundColor())
    print(ui_colors.getTextColor())
    print(ui_colors.getBorderColor())
