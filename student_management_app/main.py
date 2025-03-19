import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, \
    QTableWidgetItem, QDialog, QLineEdit, QVBoxLayout, QComboBox, \
    QPushButton, QHeaderView
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(600, 400)

        # Create menu items
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        # Create sub-menu items
        add_student_action = QAction("&Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("&About", self)
        help_menu_item.addAction(about_action)

        search_action = QAction("&Search", self)
        add_student_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)

        # Create a table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ("ID", "Name", "Course", "Phone Number"))
        self.table.verticalHeader().hide()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.
                                                           ResizeMode.
                                                           ResizeToContents)

        self.setCentralWidget(self.table)

    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                if column_number == 3:
                    item = QTableWidgetItem("+" + str(data))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
                self.table.setItem(row_number, column_number, item)
        connection.close()

        # Calculate required width and height
        width = self.table.verticalHeader().width() + 4  # Left margin
        for i in range(self.table.columnCount()):
            width += self.table.columnWidth(i)  # Add width of each column

        height = self.table.horizontalHeader().height() + 4  # Top margin
        for i in range(self.table.rowCount()):
            height += self.table.rowHeight(i)  # Add height of each row

        # Add margins for window frame and menu bar
        width += 40   # Add some padding
        height += 60  # Add space for menu bar and padding

        # Set window size, but don't make it smaller than minimum
        self.resize(max(600, width), max(400, height))

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add a new student")
        self.setFixedWidth(300)
        self.setFixedHeight(350)

        layout = QVBoxLayout()

        # Create widgets
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")

        self.course_name = QComboBox()
        courses = ["Biology", "Physics", "Mathematics", "Astronomy"]
        self.course_name.addItems(courses)

        self.phone_number = QLineEdit()
        self.phone_number.setPlaceholderText("Phone Number")

        button = QPushButton("Submit")
        button.clicked.connect(self.add_student)

        # Add widgets to layout
        layout.addWidget(self.student_name)
        layout.addWidget(self.course_name)
        layout.addWidget(self.phone_number)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) "
                       "VALUES (?, ?, ?)",
                       (self.student_name.text(),
                        self.course_name.itemText(
                           self.course_name.currentIndex()),
                        self.phone_number.text()))
        connection.commit()
        cursor.close()
        connection.close()
        student_management_system.load_data()
        self.close()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search")
        self.setFixedWidth(300)
        self.setFixedHeight(350)

        # Create the widgets
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Name")

        self.search_button = QPushButton("Search")

        # Add widgets to layout
        layout = QVBoxLayout()
        layout.addWidget(self.search_input)
        layout.addWidget(self.search_button)

        self.setLayout(layout)


app = QApplication(sys.argv)
student_management_system = MainWindow()
student_management_system.show()
student_management_system.load_data()
sys.exit(app.exec())
