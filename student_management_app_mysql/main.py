# flake8: noqa: E501
import sys
import mysql.connector
import dotenv
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, \
    QTableWidgetItem, QDialog, QLineEdit, QVBoxLayout, QComboBox, \
    QPushButton, QHeaderView, QToolBar, QStatusBar, QHBoxLayout, QLabel, \
    QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon

dotenv.load_dotenv()
PASSWORD = os.getenv("MYSQL_PASSWORD")

WINDOW_MIN_WIDTH = 600
WINDOW_MIN_HEIGHT = 400
DIALOG_WIDTH = 300
DIALOG_HEIGHT = 350
AVAILABLE_COURSES = ["Biology", "Physics", "Mathematics", "Astronomy"]


class DatabaseConnection:
    """
    Manages database connections and provides a context manager interface.
    """

    def __init__(self, host="localhost", user="root",
                 password=PASSWORD, db="school") -> None:
        """
        Initialize database connection parameters.

        Args:
            host: Database host address
            user: Database user name
            password: Database user password
            db: Database name
        """
        self.host = host
        self.user = user
        self.password = password
        self.db = db

    def connect(self) -> mysql.connector.connection.MySQLConnection:
        """
        Create and return a database connection.

        Returns:
            A MySQL database connection object
        """
        connection = mysql.connector.connect(host=self.host,
                                             user=self.user,
                                             password=self.password,
                                             database=self.db)
        return connection


class MainWindow(QMainWindow):
    """
    Main application window for the Student Management System.
    """

    def __init__(self) -> None:
        """
        Initialize the main window with menu, toolbar, table, and status bar.
        """
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        # Initialize UI components
        self._create_menu_items()
        self._create_table()
        self._create_toolbar()
        self._create_status_bar()

        # Detect a cell selection
        self.table.cellClicked.connect(self.selected)

    def _create_menu_items(self) -> None:
        """
        Create and configure the main menu items and their actions.
        """
        # Create menu items
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        # Add student action
        self.add_student_action = QAction(
            QIcon("icons/add.png"), "&Add Student", self)
        self.add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(self.add_student_action)

        # About action
        self.about_action = QAction("&About", self)
        help_menu_item.addAction(self.about_action)
        self.about_action.triggered.connect(self.about)

        # Search action
        self.search_action = QAction(
            QIcon("icons/search.png"), "&Search", self)
        self.search_action.triggered.connect(self.search)
        edit_menu_item.addAction(self.search_action)

        # Add keyboard shortcuts
        self.add_student_action.setShortcut("Ctrl+N")
        self.search_action.setShortcut("Ctrl+F")
        self.about_action.setShortcut("F1")

    def _create_table(self) -> None:
        """
        Create and configure the main table widget.
        """
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ("ID", "Name", "Course", "Phone Number"))
        self.table.verticalHeader().hide()
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents)

        # Set selection behavior to select entire rows
        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows)
        # Allow only one row to be selected at a time
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        self.setCentralWidget(self.table)

    def load_data(self) -> None:
        """
        Load student data from database and display it in the table.
        """
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students")
        result = cursor.fetchall()
        self.table.setRowCount(0)

        # Populate table with data
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                if column_number == 3:  # Phone number column
                    item = QTableWidgetItem("+" + str(data))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
                self.table.setItem(row_number, column_number, item)

        connection.close()
        self._adjust_window_size()

    def _adjust_window_size(self) -> None:
        """
        Calculate and set the optimal window size based on content.
        """
        # Calculate required width
        width = self.table.verticalHeader().width() + 4  # Left margin
        for i in range(self.table.columnCount()):
            width += self.table.columnWidth(i)

        # Calculate required height
        height = self.table.horizontalHeader().height() + 4  # Top margin
        for i in range(self.table.rowCount()):
            height += self.table.rowHeight(i)

        # Add margins for window frame and menu bar
        width += 40   # Add padding
        height += 60  # Add space for menu bar and padding

        # Set window size, but don't make it smaller than minimum
        self.resize(max(WINDOW_MIN_WIDTH, width),
                    max(WINDOW_MIN_HEIGHT, height))

    def _create_toolbar(self) -> None:
        """
        Create and configure the main toolbar.
        """
        # Create a toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(self.add_student_action)
        toolbar.addAction(self.search_action)

    def _create_status_bar(self) -> None:
        """
        Create and configure the main status bar.
        """
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

    def selected(self) -> None:
        """
        Handle table row selection and update status bar buttons.
        """
        # Remove existing buttons
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        # Add edit and delete buttons
        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(self.edit)
        self.statusbar.addWidget(edit_button)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete)
        self.statusbar.addWidget(delete_button)

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
    """
    Dialog for adding a new student to the database.
    """

    def __init__(self) -> None:
        """
        Initialize the insert dialog with input fields.
        """
        super().__init__()
        self.setWindowTitle("Add a new student")
        self.setFixedWidth(DIALOG_WIDTH)
        self.setFixedHeight(DIALOG_HEIGHT)

        layout = QVBoxLayout()
        self._create_widgets(layout)
        self.setLayout(layout)

    def _create_widgets(self, layout: QVBoxLayout) -> None:
        """
        Create and arrange the dialog widgets.

        Args:
            layout: The vertical layout to add widgets to
        """
        # Name input
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")

        # Course selection
        self.course_name = QComboBox()
        self.course_name.addItems(AVAILABLE_COURSES)

        # Phone number input
        self.phone_number = QLineEdit()
        self.phone_number.setPlaceholderText("Phone Number")

        # Submit button
        button = QPushButton("Submit")
        button.clicked.connect(self.add_student)

        # Add all widgets to layout
        layout.addWidget(self.student_name)
        layout.addWidget(self.course_name)
        layout.addWidget(self.phone_number)
        layout.addWidget(button)

    def add_student(self) -> None:
        """
        Add a new student to the database with the provided information.
        """
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO students (name, course, phone) VALUES (%s, %s, %s)",
            (self.student_name.text(),
             self.course_name.itemText(self.course_name.currentIndex()),
             self.phone_number.text())
        )
        connection.commit()
        cursor.close()
        connection.close()

        # Update the table with the new data and close the dialog
        main_window.load_data()
        self.close()


class SearchDialog(QDialog):
    """
    Dialog for searching students in the database.
    """

    def __init__(self) -> None:
        """
        Initialize the search dialog with search input field.
        """
        super().__init__()
        self.setWindowTitle("Search")
        self.setFixedWidth(DIALOG_WIDTH)
        self.setFixedHeight(DIALOG_HEIGHT)

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

    def search(self) -> None:
        """
        Search for a student by name and highlight matching rows.
        """
        name = self.search_input.text()
        items = main_window.table.findItems(
            name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            main_window.table.item(item.row(), 1).setSelected(True)


class EditDialog(QDialog):
    """
    Dialog for editing existing student information.
    """

    def __init__(self) -> None:
        """
        Initialize the edit dialog with pre-filled student information.
        """
        super().__init__()
        self.setWindowTitle("Edit")
        self.setFixedWidth(300)
        self.setFixedHeight(350)

        layout = QVBoxLayout()

        # Get the selected student's current information
        self._get_selected_student_info()

        # Create and populate input widgets
        self._create_widgets(layout)
        self.setLayout(layout)

    def _get_selected_student_info(self) -> None:
        """
        Retrieve the selected student's information from the table.
        """
        index = main_window.table.currentRow()
        self.student_name_text = main_window.table.item(index, 1).text()
        self.course_text = main_window.table.item(index, 2).text()
        self.phone_text = main_window.table.item(index, 3).text().lstrip("+")
        self.student_id = main_window.table.item(index, 0).text()

    def _create_widgets(self, layout: QVBoxLayout) -> None:
        """
        Create and arrange the dialog widgets with existing student data.

        Args:
            layout: The vertical layout to add widgets to
        """
        # Name input
        self.student_name = QLineEdit(self.student_name_text)
        self.student_name.setPlaceholderText("Name")

        # Course selection
        self.course_name = QComboBox()
        self.course_name.addItems(AVAILABLE_COURSES)
        self.course_name.setCurrentText(self.course_text)

        # Phone number input
        self.phone_number = QLineEdit(self.phone_text)
        self.phone_number.setPlaceholderText("Phone Number")

        # Submit button
        button = QPushButton("Submit")
        button.clicked.connect(self.edit_student)

        # Add widgets to layout
        layout.addWidget(self.student_name)
        layout.addWidget(self.course_name)
        layout.addWidget(self.phone_number)
        layout.addWidget(button)

    def edit_student(self) -> None:
        """
        Update the student's information in the database.
        """
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = %s, course = %s, phone = %s WHERE id = %s",  # noqa: E501
            (self.student_name.text(),
             self.course_name.itemText(self.course_name.currentIndex()),
             self.phone_number.text(),
             self.student_id)
        )
        connection.commit()
        cursor.close()
        connection.close()

        main_window.load_data()
        self.close()


class DeleteDialog(QDialog):
    """
    Dialog for confirming and executing student deletion.
    """

    def __init__(self) -> None:
        """
        Initialize the delete confirmation dialog.
        """
        super().__init__()
        self.setWindowTitle("Delete")

        # Get the selected student's information
        self._get_selected_student_info()

        # Create and populate the layout
        layout = QVBoxLayout()
        layout.setSpacing(0)
        self._create_widgets(layout)
        self.setLayout(layout)

    def _get_selected_student_info(self) -> None:
        """
        Retrieve the selected student's information from the table.
        """
        index = main_window.table.currentRow()
        self.name = main_window.table.item(index, 1).text()
        self.course = main_window.table.item(index, 2).text()
        self.phone = main_window.table.item(index, 3).text().lstrip("+")
        self.student_id = main_window.table.item(index, 0).text()

    def _create_widgets(self, layout: QVBoxLayout) -> None:
        """
        Create and arrange the dialog widgets.

        Args:
            layout: The vertical layout to add widgets to
        """
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

    def delete_student(self) -> None:
        """
        Delete the student from the database and show confirmation.
        """
        # Delete from database
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students WHERE id = %s",
                       (self.student_id,))
        connection.commit()
        cursor.close()
        connection.close()

        # Refresh table
        main_window.load_data()
        self.close()

        # Show confirmation message
        self._show_confirmation()

    def _show_confirmation(self) -> None:
        """
        Display a confirmation message after successful deletion.
        """
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText(
            f"Successfully deleted {self.name} from the student records"
        )
        confirmation_widget.exec()


class AboutDialog(QDialog):
    """
    Dialog displaying information about the application.
    """

    def __init__(self) -> None:
        """
        Initialize the about dialog.
        """
        super().__init__()
        self.setWindowTitle("About")

        # Create layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 15, 15)

        self._create_widgets(layout)
        self.setLayout(layout)

    def _create_widgets(self, layout: QVBoxLayout) -> None:
        """
        Create and arrange the dialog widgets.

        Args:
            layout: The vertical layout to add widgets to
        """
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


# Application entry point
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    main_window.load_data()
    sys.exit(app.exec())
