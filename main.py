import sys
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QWidget,
    QHBoxLayout, QDialog, QLabel, QLineEdit, QMessageBox, QComboBox
)
from PyQt6.QtCore import Qt
import sqlite3

DB_PATH = "CemeteryLookUp.db"

class CemeteryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cemetery Lookup")
        self.setGeometry(100, 100, 450, 500)

        # Main Layout
        layout = QVBoxLayout()

        # Table Widget
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Full Name", "Cemetery", "Years of Life"])
        self.table.cellDoubleClicked.connect(self.open_details)
        layout.addWidget(self.table)

        # Buttons Layout
        button_layout = QHBoxLayout()
        self.add_person_button = QPushButton("Add Person")
        self.add_cemetery_button = QPushButton("Add Cemetery")
        self.delete_person_button = QPushButton("Delete Person")
        self.add_person_button.clicked.connect(self.add_person)
        self.add_cemetery_button.clicked.connect(self.add_cemetery)
        self.delete_person_button.clicked.connect(self.delete_person)
        button_layout.addWidget(self.add_person_button)
        button_layout.addWidget(self.add_cemetery_button)
        button_layout.addWidget(self.delete_person_button)
        layout.addLayout(button_layout)

        # Central Widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Load Data
        self.load_data()

    def load_data(self):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        query = """
        SELECT Person.id, Person.FullName, Cemetery.Title, Person.YearsOfLife
        FROM Person
        JOIN GeoSpot ON Person.GeoSpot_id = GeoSpot.id
        JOIN Cemetery ON GeoSpot.Cemetery_id = Cemetery.id
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        connection.close()

        self.table.setRowCount(0)  # Clear table before reloading
        self.table.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

    def add_person(self):
        dialog = PersonAddDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_data()

    def add_cemetery(self):
        dialog = AddCemeteryDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_data()

    def delete_person(self):
        dialog = DeletePersonDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_data()

    def open_details(self, row, column):
        person_id = self.table.item(row, 0).text()
        dialog = PersonDetailsDialog(person_id, self)
        dialog.exec()

     
    def load_cemeteries(self):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute("SELECT Title FROM Cemetery")
        cemeteries = cursor.fetchall()
        connection.close()

        self.cemetery_combo.addItems([cemetery[0] for cemetery in cemeteries])

class PersonDetailsDialog(QDialog):
    def __init__(self, person_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Details for Person ID {person_id}")
        self.setGeometry(200, 200, 400, 600)

        layout = QVBoxLayout()

        # Query details
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        query = """
        SELECT Person.FullName, Person.YearsOfLife, Cemetery.Title, GeoSpot.XCords, GeoSpot.YCords, Person.ImageLink
        FROM Person
        JOIN GeoSpot ON Person.GeoSpot_id = GeoSpot.id
        JOIN Cemetery ON GeoSpot.Cemetery_id = Cemetery.id
        WHERE Person.id = ?
        """
        cursor.execute(query, (person_id,))
        details = cursor.fetchone()

        if details:
            image_link = details[5]
            if image_link:
                pixmap = QPixmap(image_link)
                if not pixmap.isNull():  # Ensure the image is valid
                    image_label = QLabel()
                    image_label.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
                    layout.addWidget(image_label)
                else:
                    layout.addWidget(QLabel("Invalid image link."))
            else:
                layout.addWidget(QLabel("No image available."))

            layout.addWidget(QLabel(f"Full Name: {details[0]}"))
            layout.addWidget(QLabel(f"Years of Life: {details[1]}"))
            layout.addWidget(QLabel(f"Cemetery: {details[2]}"))
            layout.addWidget(QLabel(f"Coordinates: ({details[3]}, {details[4]})"))

            # Query descendants
            cursor.execute("""
            SELECT Descendant.FullName, Descendant.ContactNumber
            FROM Descendant
            JOIN Person_Descendant ON Descendant.id = Person_Descendant.Descendant_id
            JOIN Person ON Person_Descendant.Person_id = Person.id
            WHERE Person.id = ?
            """, (person_id,))
            descendants = cursor.fetchall()

            layout.addWidget(QLabel("Descendants:"))
            if descendants:
                for descendant in descendants:
                    layout.addWidget(QLabel(f"- {descendant[0]} (Contact: {descendant[1]})"))
            else:
                layout.addWidget(QLabel("No descendants found."))

        else:
            layout.addWidget(QLabel("Details not found."))

        connection.close()

class PersonAddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Person")
        self.setGeometry(200, 200, 300, 300)

        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Full Name")
        self.years_input = QLineEdit()
        self.years_input.setPlaceholderText("Years of Life")

        self.cemetery_combo = QComboBox()
        self.load_cemeteries()

        self.xcords_input = QLineEdit()
        self.xcords_input.setPlaceholderText("X Coordinates")
        self.ycords_input = QLineEdit()
        self.ycords_input.setPlaceholderText("Y Coordinates")

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_person)

        layout.addWidget(QLabel("Full Name:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Years of Life:"))
        layout.addWidget(self.years_input)
        layout.addWidget(QLabel("Cemetery:"))
        layout.addWidget(self.cemetery_combo)
        layout.addWidget(QLabel("X Coordinates:"))
        layout.addWidget(self.xcords_input)
        layout.addWidget(QLabel("Y Coordinates:"))
        layout.addWidget(self.ycords_input)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def load_cemeteries(self):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute("SELECT Title FROM Cemetery")
        cemeteries = cursor.fetchall()
        connection.close()

        self.cemetery_combo.addItems([cemetery[0] for cemetery in cemeteries])

    def add_person(self):
        full_name = self.name_input.text()
        years_of_life = self.years_input.text()
        cemetery_name = self.cemetery_combo.currentText()
        x_cords = self.xcords_input.text()
        y_cords = self.ycords_input.text()

        if not full_name or not years_of_life or not cemetery_name or not x_cords or not y_cords:
            QMessageBox.warning(self, "Error", "All fields must be filled out.")
            return

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        # Find Cemetery ID
        cursor.execute("SELECT id FROM Cemetery WHERE Title = ?", (cemetery_name,))
        cemetery = cursor.fetchone()

        if cemetery is None:
            QMessageBox.warning(self, "Error", "Cemetery not found.")
            connection.close()
            return

        cemetery_id = cemetery[0]

        # Insert into GeoSpot
        cursor.execute("INSERT INTO GeoSpot (XCords, YCords, Cemetery_id) VALUES (?, ?, ?)", (x_cords, y_cords, cemetery_id))
        geo_id = cursor.lastrowid

        # Insert into Person
        cursor.execute("INSERT INTO Person (FullName, GeoSpot_id, YearsOfLife) VALUES (?, ?, ?)", (full_name, geo_id, years_of_life))
        connection.commit()
        connection.close()

        self.accept()



class AddCemeteryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Cemetery")
        self.setGeometry(200, 200, 300, 200)

        layout = QVBoxLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Cemetery Title")
        self.admin_contact_input = QLineEdit()
        self.admin_contact_input.setPlaceholderText("Admin Contact Number")
        self.guard_contact_input = QLineEdit()
        self.guard_contact_input.setPlaceholderText("Guard Contact Number")

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_cemetery)

        layout.addWidget(QLabel("Cemetery Title:"))
        layout.addWidget(self.title_input)
        layout.addWidget(QLabel("Admin Contact Number:"))
        layout.addWidget(self.admin_contact_input)
        layout.addWidget(QLabel("Guard Contact Number:"))
        layout.addWidget(self.guard_contact_input)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def add_cemetery(self):
        title = self.title_input.text()
        admin_contact = self.admin_contact_input.text()
        guard_contact = self.guard_contact_input.text()

        if not title or not admin_contact or not guard_contact:
            QMessageBox.warning(self, "Error", "All fields must be filled out.")
            return

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("INSERT INTO Cemetery (Title, AdminContactNumber, GuardContactNumber) VALUES (?, ?, ?)",
                       (title, admin_contact, guard_contact))
        connection.commit()
        connection.close()

        self.accept()

class DeletePersonDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Delete Person")
        self.setGeometry(200, 200, 300, 150)

        layout = QVBoxLayout()

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Enter Person ID")

        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_person)

        layout.addWidget(QLabel("Person ID:"))
        layout.addWidget(self.id_input)
        layout.addWidget(self.delete_button)

        self.setLayout(layout)

    def delete_person(self):
        person_id = self.id_input.text()

        if not person_id.isdigit():
            QMessageBox.warning(self, "Error", "Invalid ID format.")
            return

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM Person WHERE id = ?", (person_id,))
        connection.commit()
        connection.close()

        self.accept()

class PersonDetailsDialog(QDialog):
    def __init__(self, person_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Details for Person ID {person_id}")
        self.setGeometry(100, 100, 250, 250)

        layout = QVBoxLayout()

        # Query details
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        query = """
        SELECT Person.FullName, Person.YearsOfLife, Cemetery.Title, GeoSpot.XCords, GeoSpot.YCords, Person.ImageLink
        FROM Person
        JOIN GeoSpot ON Person.GeoSpot_id = GeoSpot.id
        JOIN Cemetery ON GeoSpot.Cemetery_id = Cemetery.id
        WHERE Person.id = ?
        """
        cursor.execute(query, (person_id,))
        details = cursor.fetchone()

        if details:
            image_link = details[5]
            pixmap = QPixmap(image_link)
            if not pixmap.isNull():  
                image_label = QLabel()
                image_label.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
                image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                layout.addWidget(image_label)
            else:
                layout.addWidget(QLabel("Изображение не найдено"))

            
            layout.addWidget(QLabel(f"Full Name: {details[0]}"))
            layout.addWidget(QLabel(f"Years of Life: {details[1]}"))
            layout.addWidget(QLabel(f"Cemetery: {details[2]}"))
            layout.addWidget(QLabel(f"Coordinates: ({details[3]}, {details[4]})"))
            # Query descendants
            cursor.execute("""
            SELECT Descendant.FullName, Descendant.ContactNumber
            FROM Descendant
            JOIN Person_Descendant ON Descendant.id = Person_Descendant.Descendant_id
            JOIN Person ON Person_Descendant.Person_id = Person.id
            WHERE Person.id = ?
            """, (person_id,))
            descendants = cursor.fetchall()

            layout.addWidget(QLabel("Descendants:"))
            if descendants:
                for descendant in descendants:
                    layout.addWidget(QLabel(f"- {descendant[0]} (Contact: {descendant[1]})"))
            else:
                layout.addWidget(QLabel("No descendants found."))

        else:
            layout.addWidget(QLabel("Details not found."))

        connection.close()

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CemeteryApp()
    window.show()
    sys.exit(app.exec())
