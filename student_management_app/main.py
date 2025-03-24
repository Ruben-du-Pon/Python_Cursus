import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, \
    QTableWidgetItem, QDialog, QLineEdit, QVBoxLayout, QComboBox, \
    QPushButton, QHeaderView, QToolBar, QStatusBar, QHBoxLayout, QLabel, \
    QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon


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
        add_student_action = QAction(
            QIcon("icons/add.png"), "&Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("&About", self)
        help_menu_item.addAction(about_action)
        about_action.triggered.connect(self.about)

        search_action = QAction(QIcon("icons/search.png"), "&Search", self)
        search_action.triggered.connect(self.search)
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

        # Create a toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # Create a status bar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect a cell selection
        self.table.cellClicked.connect(self.selected)

    def selected(self):
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(self.edit)
        self.statusbar.addWidget(edit_button)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete)
        self.statusbar.addWidget(delete_button)

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

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
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
        main_window.load_data()
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
        self.search_button.clicked.connect(self.search)

        # Add widgets to layout
        layout = QVBoxLayout()
        layout.addWidget(self.search_input)
        layout.addWidget(self.search_button)

        self.setLayout(layout)

    def search(self):
        name = self.search_input.text()
        items = main_window.table.findItems(
            name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            main_window.table.item(item.row(), 1).setSelected(True)


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit")
        self.setFixedWidth(300)
        self.setFixedHeight(350)

        layout = QVBoxLayout()

        # Get the selected row
        index = main_window.table.currentRow()
        name = main_window.table.item(index, 1).text()
        course = main_window.table.item(index, 2).text()
        phone = main_window.table.item(index, 3).text().lstrip("+")
        self.student_id = main_window.table.item(index, 0).text()

        # Create widgets
        self.student_name = QLineEdit(name)
        self.student_name.setPlaceholderText("Name")

        self.course_name = QComboBox()
        courses = ["Biology", "Physics", "Mathematics", "Astronomy"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course)

        self.phone_number = QLineEdit(phone)
        self.phone_number.setPlaceholderText("Phone Number")

        button = QPushButton("Submit")
        button.clicked.connect(self.edit_student)

        # Add widgets to layout
        layout.addWidget(self.student_name)
        layout.addWidget(self.course_name)
        layout.addWidget(self.phone_number)
        layout.addWidget(button)

        self.setLayout(layout)

    def edit_student(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",  # noqa: E501
                       (self.student_name.text(),
                        self.course_name.itemText(self.course_name.currentIndex()),  # noqa: E501
                        self.phone_number.text(),
                        self.student_id))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()
        self.close()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete")

        # Get the selected row
        index = main_window.table.currentRow()
        self.name = main_window.table.item(index, 1).text()
        self.course = main_window.table.item(index, 2).text()
        self.phone = main_window.table.item(index, 3).text().lstrip("+")
        self.student_id = main_window.table.item(index, 0).text()

        layout = QVBoxLayout()
        layout.setSpacing(0)

        # Add confirmation message
        message = QLabel("Are you sure you want to delete this student?")
        layout.addWidget(message)

        layout.addSpacing(20)

        # Add student details
        layout.addWidget(QLabel(f"Name: {self.name}"))
        layout.addWidget(QLabel(f"Course: {self.course}"))
        layout.addWidget(QLabel(f"Phone: {self.phone}"))

        layout.addSpacing(20)

        # Create horizontal button layout
        button_layout = QHBoxLayout()
        ok_button = QPushButton("Ok")
        ok_button.clicked.connect(self.delete_student)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def delete_student(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?",
                       (self.student_id, ))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()
        self.close()

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText(
            f"Sucessfully deleted {self.name} from the student records")
        confirmation_widget.exec()


class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        # Create layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 25, 10)

        # Create label with content
        content = """
        This app was created during the course "The Python Mega Course".
        Feel free to modify and reuse this app.
        """
        label = QLabel(content)
        label.setWordWrap(True)  # Enable text wrapping
        layout.addWidget(label)

        # Add OK button
        button = QPushButton("OK")
        button.clicked.connect(self.close)
        layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())
