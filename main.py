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
    sort = 'Person.id'
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cemetery Lookup")
        self.setGeometry(100, 100, 550, 600)

        # Main Layout
        layout = QVBoxLayout()

        #Sort Buttons Layout 
        sort_layout = QHBoxLayout()
        self.add_sort_person_button = QPushButton("Сортировка по человеку")
        self.add_sort_cemetery_button = QPushButton("Сортировка по кладбищу")
        self.add_sort_years_of_birth_button = QPushButton("Сортировка по дате рождения")
        self.add_sort_years_of_death_button = QPushButton("Сортировка по дате смерти")
        self.add_sort_person_button.clicked.connect(self.SortPerson)
        self.add_sort_cemetery_button.clicked.connect(self.SortCemetery)
        self.add_sort_years_of_birth_button.clicked.connect(self.SortBirth)
        self.add_sort_years_of_death_button.clicked.connect(self.SortDeath)
        sort_layout.addWidget(self.add_sort_person_button)
        sort_layout.addWidget(self.add_sort_cemetery_button)
        sort_layout.addWidget(self.add_sort_years_of_birth_button)
        sort_layout.addWidget(self.add_sort_years_of_death_button)
        self.add_sort_person_button.setStyleSheet("background-color : gray")
        self.add_sort_cemetery_button.setStyleSheet("background-color : gray")
        self.add_sort_years_of_birth_button.setStyleSheet("background-color : gray")
        self.add_sort_years_of_death_button.setStyleSheet("background-color : gray")
        layout.addLayout(sort_layout)

        # Table Widget
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Full Name", "Cemetery", "Years of Birth", "Years of Death"])
        self.table.cellDoubleClicked.connect(self.RECopen_details)
        layout.addWidget(self.table)

        # Buttons Layout
        Buttons = QVBoxLayout()
        add_button_layout = QHBoxLayout() #upper row
        delete_button_layout = QHBoxLayout() #downer (is this even a word?) row 
        misc_button_layout = QHBoxLayout() # EVEN DOWNER row 

        # adding
        self.add_person_button = QPushButton("Добавить человека")
        self.add_cemetery_button = QPushButton("Добавить кладбище")
        self.add_descendant_button = QPushButton("Добавить родственника")
        # deleting
        self.delete_person_button = QPushButton("Удалить человека")
        self.delete_cemetery_button = QPushButton("Удалить кладбище")
        self.delete_descendant_button = QPushButton("Удалить родственника")
        # MISC
        self.search_person_button = QPushButton("Искать человека")

        #connecting 
        #connecting add
        self.add_person_button.clicked.connect(self.add_person)
        self.add_cemetery_button.clicked.connect(self.add_cemetery)
        self.add_descendant_button.clicked.connect(self.add_descendant)
        #connecting delete
        self.delete_person_button.clicked.connect(self.delete_person)
        self.delete_cemetery_button.clicked.connect(self.delete_cemetery)
        self.delete_descendant_button.clicked.connect(self.delete_descendant)
        #connecting misc 
        self.search_person_button.clicked.connect(self.search_person) 

        #laying on layout buttons 
        add_button_layout.addWidget(self.add_person_button)
        add_button_layout.addWidget(self.add_cemetery_button)
        add_button_layout.addWidget(self.add_descendant_button)
        delete_button_layout.addWidget(self.delete_person_button)
        delete_button_layout.addWidget(self.delete_cemetery_button)
        delete_button_layout.addWidget(self.delete_descendant_button)
        misc_button_layout.addWidget(self.search_person_button)

        Buttons.addLayout(add_button_layout)
        Buttons.addLayout(delete_button_layout)
        Buttons.addLayout(misc_button_layout)
        layout.addLayout(Buttons)

        # Central Widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Load Data
        self.load_data()

    def load_data(self):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        # Формируем запрос с подставленным именем столбца
        query = f"""
        SELECT Person.id, Person.FullName, Cemetery.Title, Person.YearOfBirth, Person.YearOfDeath
        FROM Person
        JOIN GeoSpot ON Person.GeoSpot_id = GeoSpot.id
        JOIN Cemetery ON GeoSpot.Cemetery_id = Cemetery.id
        ORDER BY {CemeteryApp.sort}
        """

        cursor.execute(query)
        rows = cursor.fetchall()
        connection.close()

        self.table.setRowCount(0)  # Clear table before reloading
        self.table.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

    # Sorting our coffins 
    def SortPerson(self):
        if CemeteryApp.sort != "Person.FullName ASC" and CemeteryApp.sort != "Person.FullName DESC":
            CemeteryApp.sort = "Person.FullName ASC"
            self.add_sort_person_button.setStyleSheet("background-color : green")
            self.add_sort_cemetery_button.setStyleSheet("background-color : gray")
            self.add_sort_years_of_birth_button.setStyleSheet("background-color : gray")
            self.add_sort_years_of_death_button.setStyleSheet("background-color : gray")
        elif CemeteryApp.sort == "Person.FullName ASC":
            CemeteryApp.sort = "Person.FullName DESC"
            self.add_sort_person_button.setStyleSheet("background-color : red")
            self.add_sort_cemetery_button.setStyleSheet("background-color : gray")
            self.add_sort_years_of_birth_button.setStyleSheet("background-color : gray")
            self.add_sort_years_of_death_button.setStyleSheet("background-color : gray")
        else:
            CemeteryApp.sort = "Person.id"
            self.add_sort_person_button.setStyleSheet("background-color : gray")
        self.load_data()

    def SortCemetery(self):
        if CemeteryApp.sort != "Cemetery.Title ASC" and CemeteryApp.sort != "Cemetery.Title DESC":
            CemeteryApp.sort = "Cemetery.Title ASC"
            self.add_sort_cemetery_button.setStyleSheet("background-color : green")
            self.add_sort_person_button.setStyleSheet("background-color : gray")
            self.add_sort_years_of_birth_button.setStyleSheet("background-color : gray")
            self.add_sort_years_of_death_button.setStyleSheet("background-color : gray")
        elif CemeteryApp.sort == "Cemetery.Title ASC":
            CemeteryApp.sort = "Cemetery.Title DESC"
            self.add_sort_cemetery_button.setStyleSheet("background-color : red")
            self.add_sort_person_button.setStyleSheet("background-color : gray")
            self.add_sort_years_of_birth_button.setStyleSheet("background-color : gray")
            self.add_sort_years_of_death_button.setStyleSheet("background-color : gray")
        else:
            CemeteryApp.sort = "Person.id"
            self.add_sort_cemetery_button.setStyleSheet("background-color : gray")
        self.load_data()

    def SortBirth(self):
        if CemeteryApp.sort != "Person.YearOfBirth ASC" and CemeteryApp.sort != "Person.YearOfBirth DESC":
            CemeteryApp.sort = "Person.YearOfBirth ASC"
            self.add_sort_person_button.setStyleSheet("background-color : gray")
            self.add_sort_cemetery_button.setStyleSheet("background-color : gray")
            self.add_sort_years_of_birth_button.setStyleSheet("background-color : green")
            self.add_sort_years_of_death_button.setStyleSheet("background-color : gray")
        elif CemeteryApp.sort == "Person.YearOfBirth ASC":
            CemeteryApp.sort = "Person.YearOfBirth DESC"
            self.add_sort_person_button.setStyleSheet("background-color : gray")
            self.add_sort_cemetery_button.setStyleSheet("background-color : gray")
            self.add_sort_years_of_birth_button.setStyleSheet("background-color : red")
            self.add_sort_years_of_death_button.setStyleSheet("background-color : gray")
        else:
            CemeteryApp.sort = "Person.id"
            self.add_sort_years_of_birth_button.setStyleSheet("background-color : gray")
        self.load_data()

    def SortDeath(self):
        if CemeteryApp.sort != "Person.YearOfDeath ASC" and CemeteryApp.sort != "Person.YearOfDeath DESC":
            CemeteryApp.sort = "Person.YearOfDeath ASC"
            self.add_sort_person_button.setStyleSheet("background-color : gray")
            self.add_sort_cemetery_button.setStyleSheet("background-color : gray")
            self.add_sort_years_of_birth_button.setStyleSheet("background-color : gray")
            self.add_sort_years_of_death_button.setStyleSheet("background-color : green")
        elif CemeteryApp.sort == "Person.YearOfDeath ASC":
            CemeteryApp.sort = "Person.YearOfDeath DESC"
            self.add_sort_person_button.setStyleSheet("background-color : gray")
            self.add_sort_cemetery_button.setStyleSheet("background-color : gray")
            self.add_sort_years_of_birth_button.setStyleSheet("background-color : gray")
            self.add_sort_years_of_death_button.setStyleSheet("background-color : red")
        else:
            CemeteryApp.sort = "Person.id"
            self.add_sort_years_of_death_button.setStyleSheet("background-color : gray")
        self.load_data()

    # Adding 
    def add_person(self):
        dialog = PersonAddDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_data()

    def add_cemetery(self):
        dialog = AddCemeteryDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_data()

    def add_descendant(self):
        dialog = AddDescendantDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_data()

    # Deleting
    def delete_person(self):
        dialog = DeletePersonDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_data()

    def delete_cemetery(self):
        dialog = DeleteCemeteryDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_data()

    def delete_descendant(self):
        dialog = DeleteDescendantDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_data()

    # Looking
    def RECopen_details(self, row, column):
        self.open_details(row, column)
        self.load_data()

    def open_details(self, row, column):
        person_id = self.table.item(row, 0).text()
        dialog = PersonDetailsDialog(person_id, self)
        dialog.exec()

    # MISC 
    def load_cemeteries(self):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute("SELECT Title FROM Cemetery")
        cemeteries = cursor.fetchall()
        connection.close()

        self.cemetery_combo.addItems([cemetery[0] for cemetery in cemeteries])

    def search_person(self):
        dialog = PersonSearchDialog(self)
        dialog.exec()
# LOOKING
class PersonDetailsDialog(QDialog):
    def __init__(self, person_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Правим детали человека под ID {person_id}")
        self.setGeometry(200, 100, 400, 600)
        self.person_id = person_id

        layout = QVBoxLayout()
        self.inputs = {}
        self.descendant_widgets = []

        # Query details
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        query = """
        SELECT Person.FullName, Person.YearOfBirth, Person.YearOfDeath, Cemetery.Title, GeoSpot.XCords, GeoSpot.YCords, Person.ImageLink
        FROM Person
        JOIN GeoSpot ON Person.GeoSpot_id = GeoSpot.id
        JOIN Cemetery ON GeoSpot.Cemetery_id = Cemetery.id
        WHERE Person.id = ?
        """
        cursor.execute(query, (person_id,))
        details = cursor.fetchone()

        if details:
            # Display image
            image_link = details[6]
            if image_link:
                pixmap = QPixmap(image_link)
                if not pixmap.isNull():
                    image_label = QLabel()
                    image_label.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
                    image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    layout.addWidget(image_label)
                else:
                    layout.addWidget(QLabel("Картинки нет, добавьте папку картинку с нужным названием."))
            else:
                layout.addWidget(QLabel("Проблема с базой данных!"))

            # Input fields
            labels = ["Полное имя", "Год рождения", "Год смерти", "Кладбище", "Координаты по X", "Координаты по Y"]

            for label, value in zip(labels, details[:6]):
                row_layout = QHBoxLayout()
                label_widget = QLabel(label + ":")
                input_widget = QLineEdit(str(value))
                self.inputs[label] = input_widget

                row_layout.addWidget(label_widget)
                row_layout.addWidget(input_widget)
                layout.addLayout(row_layout)

        # Load descendants
        descendant_query = """
        SELECT Descendant.id, Descendant.FullName, Descendant.ContactNumber
        FROM Descendant
        JOIN Person_Descendant ON Descendant.id = Person_Descendant.Descendant_id
        WHERE Person_Descendant.Person_id = ?
        """
        cursor.execute(descendant_query, (person_id,))
        descendants = cursor.fetchall()

        layout.addWidget(QLabel("Родственники:"))
        self.descendants_layout = QVBoxLayout()
        layout.addLayout(self.descendants_layout)

        for descendant in descendants:
            descendant_combo = QComboBox()
            descendant_combo.addItems(self.load_descendants())
            descendant_combo.setCurrentText(f"{descendant[0]}: {descendant[1]}, {descendant[2]}")
            self.descendants_layout.addWidget(descendant_combo)
            self.descendant_widgets.append(descendant_combo)

        connection.close()

        # Add and Remove Descendant Buttons
        self.add_descendant_button = QPushButton("Добавить родственника")
        self.add_descendant_button.clicked.connect(self.add_descendant)

        self.remove_descendant_button = QPushButton("Удалить родственника")
        self.remove_descendant_button.clicked.connect(self.remove_last_descendant)

        layout.addWidget(self.add_descendant_button)
        layout.addWidget(self.remove_descendant_button)

        # Save Button
        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.save_details)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def load_descendants(self):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute("SELECT id, FullName, ContactNumber  FROM Descendant")
        descendants = cursor.fetchall()
        connection.close()

        return [f"{descendant[0]}: {descendant[1]} {descendant[2]}" for descendant in descendants]

    def add_descendant(self):
        descendant_combo = QComboBox()
        descendant_combo.addItems(self.load_descendants())
        self.descendants_layout.addWidget(descendant_combo)
        self.descendant_widgets.append(descendant_combo)

    def remove_last_descendant(self):
        if self.descendant_widgets:
            last_descendant = self.descendant_widgets.pop()
            self.descendants_layout.removeWidget(last_descendant)
            last_descendant.deleteLater()

    def save_details(self):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        try:
            # Update Person details
            full_name = self.inputs["Полное имя"].text()
            year_of_birth = self.inputs["Год рождения"].text()
            year_of_death = self.inputs["Год смерти"].text()
            x_coords = self.inputs["Координаты по X"].text()
            y_coords = self.inputs["Координаты по Y"].text()

            # Get Cemetery ID
            cemetery_name = self.inputs["Кладбище"].text()
            cursor.execute("SELECT id FROM Cemetery WHERE Title = ?", (cemetery_name,))
            cemetery = cursor.fetchone()

            if cemetery is None:
                QMessageBox.warning(self, "ОШИБКА!", "Кладбища не найдены")
                return

            cemetery_id = cemetery[0]

            # Update GeoSpot
            cursor.execute("""
                UPDATE GeoSpot 
                SET XCords = ?, YCords = ?, Cemetery_id = ?
                WHERE id = (SELECT GeoSpot_id FROM Person WHERE id = ?)
            """, (x_coords, y_coords, cemetery_id, self.person_id))

            # Update Person
            cursor.execute("""
                UPDATE Person 
                SET FullName = ?, YearOfBirth = ?, YearOfDeath = ?
                WHERE id = ?
            """, (full_name, year_of_birth, year_of_death, self.person_id))

            # Update descendants
            cursor.execute("DELETE FROM Person_Descendant WHERE Person_id = ?", (self.person_id,))
            for descendant_combo in self.descendant_widgets:
                descendant_id = descendant_combo.currentText().split(":")[0]
                if descendant_id.isdigit():
                    cursor.execute("INSERT INTO Person_Descendant (Person_id, Descendant_id) VALUES (?, ?)", (self.person_id, int(descendant_id)))

            connection.commit()
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Что-то пошло не так: {e}")
        finally:
            connection.close()

# ADDING
class PersonAddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавляем нового человека")
        self.setGeometry(200, 200, 400, 400)

        layout = QVBoxLayout()
        self.descendant_widgets = []

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Полное имя")
        self.years_of_birth_input = QLineEdit()
        self.years_of_birth_input.setPlaceholderText("Год рождения")
        self.years_of_death_input = QLineEdit()
        self.years_of_death_input.setPlaceholderText("Год смерти")

        self.cemetery_combo = QComboBox()
        self.load_cemeteries()

        self.xcords_input = QLineEdit()
        self.xcords_input.setPlaceholderText("Координаты по X")
        self.ycords_input = QLineEdit()
        self.ycords_input.setPlaceholderText("Координаты по Y")

        self.add_descendant_button = QPushButton("Добавить родственника")
        self.add_descendant_button.clicked.connect(self.add_descendant)

        self.remove_descendant_button = QPushButton("Удалить последнего добавленного родственника")
        self.remove_descendant_button.clicked.connect(self.remove_last_descendant)

        self.add_button = QPushButton("Добавить человека")
        self.add_button.clicked.connect(self.add_person)

        layout.addWidget(QLabel("Полное имя:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Год рождения:"))
        layout.addWidget(self.years_of_birth_input)
        layout.addWidget(QLabel("Год смерти:"))
        layout.addWidget(self.years_of_death_input)
        layout.addWidget(QLabel("Кладбище:"))
        layout.addWidget(self.cemetery_combo)
        layout.addWidget(QLabel("Координаты по X:"))
        layout.addWidget(self.xcords_input)
        layout.addWidget(QLabel("Координаты по Y:"))
        layout.addWidget(self.ycords_input)

        layout.addWidget(QLabel("Родственники:"))
        self.descendants_layout = QVBoxLayout()
        layout.addLayout(self.descendants_layout)
        layout.addWidget(self.add_descendant_button)
        layout.addWidget(self.remove_descendant_button)

        layout.addWidget(self.add_button)
        self.setLayout(layout)

    def load_cemeteries(self):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute("SELECT Title FROM Cemetery")
        cemeteries = cursor.fetchall()
        connection.close()

        self.cemetery_combo.addItems([cemetery[0] for cemetery in cemeteries])

    def load_descendants(self):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute("SELECT id, FullName FROM Descendant")
        descendants = cursor.fetchall()
        connection.close()

        return [f"{descendant[0]}: {descendant[1]}" for descendant in descendants]

    def add_descendant(self):
        descendant_combo = QComboBox()
        descendant_combo.addItems(self.load_descendants())
        self.descendants_layout.addWidget(descendant_combo)
        self.descendant_widgets.append(descendant_combo)

    def remove_last_descendant(self):
        if self.descendant_widgets:
            last_descendant = self.descendant_widgets.pop()
            self.descendants_layout.removeWidget(last_descendant)
            last_descendant.deleteLater()

    def add_person(self):
        full_name = self.name_input.text()
        years_of_birth = self.years_of_birth_input.text()
        years_of_death = self.years_of_death_input.text()
        cemetery_name = self.cemetery_combo.currentText()
        x_cords = self.xcords_input.text()
        y_cords = self.ycords_input.text()

        if not full_name or not years_of_birth or not years_of_death or not cemetery_name or not x_cords or not y_cords:
            QMessageBox.warning(self, "Ошибка!", "Все поля должны быть заполнены!")
            return

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        # Find Cemetery ID
        cursor.execute("SELECT id FROM Cemetery WHERE Title = ?", (cemetery_name,))
        cemetery = cursor.fetchone()

        if cemetery is None:
            QMessageBox.warning(self, "Ошибка!", "Кладбище не найдено!")
            connection.close()
            return

        cemetery_id = cemetery[0]

        # Insert into GeoSpot
        cursor.execute("INSERT INTO GeoSpot (XCords, YCords, Cemetery_id) VALUES (?, ?, ?)", (x_cords, y_cords, cemetery_id))
        geo_id = cursor.lastrowid

        # Insert into Person
        cursor.execute("INSERT INTO Person (FullName, GeoSpot_id, YearOfBirth, YearOfDeath) VALUES (?, ?, ?, ?)", (full_name, geo_id, years_of_birth, years_of_death))
        person_id = cursor.lastrowid

        # Link descendants
        for descendant_combo in self.descendant_widgets:
            descendant_id = descendant_combo.currentText().split(":")[0]
            if descendant_id.isdigit():
                cursor.execute("INSERT INTO Person_Descendant (Person_id, Descendant_id) VALUES (?, ?)", (person_id, int(descendant_id)))

        connection.commit()
        connection.close()

        self.accept()

class AddDescendantDialog(QDialog):
    def __init__(self, parent =None):
        super().__init__(parent)
        self.setWindowTitle("Добавить нового родственника")
        self.setGeometry(200, 200, 300, 200)

        layout = QVBoxLayout()

        self.FullName_input = QLineEdit()
        self.FullName_input.setPlaceholderText("Полное имя родственника")
        self.ContactNumber_input = QLineEdit()
        self.ContactNumber_input.setPlaceholderText("Контактный телефон родственника")

        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_descendant)

        layout.addWidget(QLabel("Полное имя родственника:"))
        layout.addWidget(self.FullName_input)
        layout.addWidget(QLabel("Контактный номер родственника:"))
        layout.addWidget(self.ContactNumber_input)
        layout.addWidget(self.add_button)

        self.setLayout(layout)
    
    def add_descendant(self):
        FullName = self.FullName_input.text()
        ContactNumber = self.ContactNumber_input.text()

        if not FullName or not ContactNumber:
            QMessageBox.warning(self, "Ошибка!", "Все поля должны быть заполнены!")
            return
        
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("INSERT INTO Descendant (FullName, ContactNumber) VALUES (?, ?)",
                       (FullName, ContactNumber))
        connection.commit()
        connection.close()

        self.accept()

class AddCemeteryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить новое кладбище")
        self.setGeometry(200, 200, 300, 200)

        layout = QVBoxLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Название кладбища")
        self.admin_contact_input = QLineEdit()
        self.admin_contact_input.setPlaceholderText("Контактный номер Начальника")
        self.guard_contact_input = QLineEdit()
        self.guard_contact_input.setPlaceholderText("Контактный номер Сторожа")

        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_cemetery)

        layout.addWidget(QLabel("Название кладбища:"))
        layout.addWidget(self.title_input)
        layout.addWidget(QLabel("Контактный номер Начальника:"))
        layout.addWidget(self.admin_contact_input)
        layout.addWidget(QLabel("Контактный номер Сторожа:"))
        layout.addWidget(self.guard_contact_input)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def add_cemetery(self):
        title = self.title_input.text()
        admin_contact = self.admin_contact_input.text()
        guard_contact = self.guard_contact_input.text()

        if not title or not admin_contact or not guard_contact:
            QMessageBox.warning(self, "Ошибка!", "Все поля должны быть заполнены!")
            return

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("INSERT INTO Cemetery (Title, AdminContactNumber, GuardContactNumber) VALUES (?, ?, ?)",
                       (title, admin_contact, guard_contact))
        connection.commit()
        connection.close()

        self.accept()

# DELETING
class DeletePersonDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Удалить человека")
        self.setGeometry(200, 200, 300, 150)

        layout = QVBoxLayout()

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Введите ID человека")

        self.delete_button = QPushButton("Удалить")
        self.delete_button.clicked.connect(self.delete_person)

        layout.addWidget(QLabel("ID человека:"))
        layout.addWidget(self.id_input)
        layout.addWidget(self.delete_button)

        self.setLayout(layout)

    def delete_person(self):
        person_id = self.id_input.text()

        # Проверка: ID должен быть числом
        if not person_id.isdigit():
            QMessageBox.warning(self, "Ошибка!", "Вы ввели не число!")
            return

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        # Проверка существования записи с данным ID
        cursor.execute("SELECT 1 FROM Person WHERE id = ?", (person_id,))
        result = cursor.fetchone()

        if result is None:
            QMessageBox.warning(self, "Ошибка!", f"Нет человека под номером {person_id}.")
            connection.close()
            return

        # Удаление записи
        cursor.execute("DELETE FROM Person WHERE id = ?", (person_id,))
        connection.commit()
        connection.close()

        QMessageBox.information(self, "Успех!", f"Человек с номером {person_id} был удален!")
        self.accept()

class DeleteDescendantDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Удалить родственника")
        self.setGeometry(200, 200, 300, 150)

        layout = QVBoxLayout()

        self.descendant_combo = QComboBox()
        self.load_descendant()

        self.delete_button = QPushButton("Удалить")
        self.delete_button.clicked.connect(self.delete_descendant)

        layout.addWidget(QLabel("Родственник:"))
        layout.addWidget(self.descendant_combo)
        layout.addWidget(self.delete_button)

        self.setLayout(layout)

    def load_descendant(self):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute("SELECT id, FullName FROM Descendant")
        descendants = cursor.fetchall()
        connection.close()
        self.descendant_combo.addItems([" ".join(str(value) for value in descendant) for descendant in descendants])

    def delete_descendant(self):
        descendant = self.descendant_combo.currentText()
        descendant = descendant.split()
        descendant_id = descendant[0]
        if not descendant_id.isdigit():
            QMessageBox.warning(self, "Ошибка", "Неверный ID родственника.")
            return

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM Descendant WHERE id = ?", (descendant_id,))
        connection.commit()
        connection.close()

        self.accept()

class DeleteCemeteryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Удалить кладбище")
        self.setGeometry(200, 200, 300, 150)

        layout = QVBoxLayout()

        self.cemetery_combo = QComboBox()
        self.load_cemeteries()

        self.delete_button = QPushButton("Удалить")
        self.delete_button.clicked.connect(self.delete_cemetery)

        layout.addWidget(QLabel("Кладбище:"))
        layout.addWidget(self.cemetery_combo)
        layout.addWidget(self.delete_button)

        self.setLayout(layout)

    def load_cemeteries(self):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute("SELECT id, Title FROM Cemetery")
        cemeteries = cursor.fetchall()
        connection.close()
        self.cemetery_combo.addItems([" ".join(str(value) for value in cemetery) for cemetery in cemeteries])

    def delete_cemetery(self):
        cemetery = self.cemetery_combo.currentText()
        cemetery = cemetery.split()
        cemetery_id = cemetery[0]
        if not cemetery_id.isdigit():
            QMessageBox.warning(self, "Ошибка!", "Неверный ID кладбища.")
            return

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM cemetery WHERE id = ?", (cemetery_id,))
        connection.commit()
        connection.close()

        self.accept()

# MISC
class PersonSearchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Найти человека")
        self.setGeometry(200, 200, 400, 100)

        layout = QVBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введите ID или Полное Имя человека")

        self.search_button = QPushButton("Найти")
        self.search_button.clicked.connect(self.search_person)

        layout.addWidget(QLabel("Найти человека по ID или Полному Имени"))
        layout.addWidget(self.search_input)
        layout.addWidget(self.search_button)

        self.setLayout(layout)

    def search_person(self):
        search_term = self.search_input.text()

        if not search_term:
            QMessageBox.warning(self, "Ошибка!", "Введите что-то в поисковую строку!")
            return

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        try:
            if search_term.isdigit():
                query = "SELECT id FROM Person WHERE id = ?"
                cursor.execute(query, (search_term,))
            else:
                query = "SELECT id FROM Person WHERE FullName LIKE ?"
                cursor.execute(query, (f"%{search_term}%",))

            result = cursor.fetchone()
            if result:
                person_id = result[0]
                dialog = PersonDetailsDialog(person_id, self)
                dialog.exec()
            else:
                QMessageBox.information(self, "Ошибка", "Никто не был найден по вашему запросу.")
        finally:
            connection.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CemeteryApp()
    window.show()
    sys.exit(app.exec())
