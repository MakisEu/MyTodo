from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    Qt,
    QObject,
)


class lightweight_table_model(QAbstractTableModel):
    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self._data: list[list[str]] = []
        self._horizontal_headers: list[str] = []
        self._vertical_headers: list[str] = []

    # ==================== Required Overrides ====================

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._data)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._data[0]) if self._data else 0

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid():
            return None

        if role in (Qt.DisplayRole, Qt.EditRole):
            return self._data[index.row()][index.column()]

        return None

    def setData(self, index: QModelIndex, value, role: int = Qt.EditRole) -> bool:
        if not index.isValid() or role != Qt.EditRole:
            return False

        self._data[index.row()][index.column()] = str(value)
        self.dataChanged.emit(index, index, [role])
        return True

    def flags(self, index: QModelIndex):
        if not index.isValid():
            return Qt.NoItemFlags

        return (
            Qt.ItemIsSelectable
            | Qt.ItemIsEnabled
            | Qt.ItemIsEditable
        )

    def headerData(self, section: int, orientation: Qt.Orientation,
                   role: int = Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            if section < len(self._horizontal_headers):
                return self._horizontal_headers[section]

        if orientation == Qt.Vertical:
            if section < len(self._vertical_headers):
                return self._vertical_headers[section]

        return None

    # ==================== Custom / Invokable Methods ====================

    def clear(self):
        self.beginResetModel()
        self._data.clear()
        self._horizontal_headers.clear()
        self._vertical_headers.clear()
        self.endResetModel()

    def setRowCount(self, rows: int):
        self.beginResetModel()
        current_columns = self.columnCount()
        self._data = [
            ["" for _ in range(current_columns)]
            for _ in range(rows)
        ]
        self._vertical_headers = [""] * rows
        self.endResetModel()

    def setColumnCount(self, columns: int):
        self.beginResetModel()
        for row in self._data:
            if len(row) < columns:
                row.extend([""] * (columns - len(row)))
            else:
                del row[columns:]
        self._horizontal_headers = [""] * columns
        self.endResetModel()

    def setHorizontalHeaderLabels(self, labels: list[str]):
        self._horizontal_headers = list(labels)
        if labels:
            self.headerDataChanged.emit(
                Qt.Horizontal, 0, len(labels) - 1
            )

    def setVerticalHeaderLabels(self, labels: list[str]):
        self._vertical_headers = list(labels)
        if labels:
            self.headerDataChanged.emit(
                Qt.Vertical, 0, len(labels) - 1
            )
