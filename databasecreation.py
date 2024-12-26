import sqlite3 as s
import os

file_path = 'CemeteryLookUp.db'

# Удаление старой базы данных (если существует)
os.remove(file_path)

connection = s.connect(file_path)

cur = connection.cursor()

scr = '''
-- Таблица с названиями кладбищ, контактами администрации и охраны
CREATE TABLE Cemetery(
id INTEGER PRIMARY KEY AUTOINCREMENT,
Title VARCHAR(60),
AdminContactNumber VARCHAR(14),
GuardContactNumber VARCHAR(14));

-- Геопозиции захоронений (координаты) с id кладбища
CREATE TABLE GeoSpot(
id INTEGER PRIMARY KEY AUTOINCREMENT,
XCords FLOAT,
YCords FLOAT,
Cemetery_id INT,
FOREIGN KEY (Cemetery_id) REFERENCES Cemetery(id) 
    ON UPDATE CASCADE
    ON DELETE CASCADE);

-- Имена захороненных с id захоронений, годом рождения и годом смерти
CREATE TABLE Person(
id INTEGER PRIMARY KEY AUTOINCREMENT,
FullName VARCHAR(45),
GeoSpot_id INT,
YearOfBirth INT,
YearOfDeath INT,
ImageLink TEXT,
FOREIGN KEY (GeoSpot_id) REFERENCES GeoSpot(id) 
    ON UPDATE CASCADE
    ON DELETE CASCADE);

-- Имена близких родственников с контактными номерами
CREATE TABLE Descendant(
id INTEGER PRIMARY KEY AUTOINCREMENT,
FullName VARCHAR(45),
ContactNumber VARCHAR(14));

-- Таблица связи m2m между захороненными и родственниками
CREATE TABLE Person_Descendant(
Person_id INT,
Descendant_id INT,
PRIMARY KEY (Person_id, Descendant_id),
FOREIGN KEY (Person_id) REFERENCES Person(id)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
FOREIGN KEY (Descendant_id) REFERENCES Descendant(id)
    ON UPDATE CASCADE
    ON DELETE NO ACTION);

-- Вставка данных
INSERT INTO Cemetery (id, Title, AdminContactNumber, GuardContactNumber) VALUES
(1, 'Покой Эльдии', '+79027027590', '+79009145657'),
(2, 'Памяти Героям', '+79027027590', '+79009145657'),
(3, 'Питерское городское кладбище', '+79027027590', '+79009145657'),
(4, 'Павильон Вечного Покоя', '+79027027590', '+79009145657');

INSERT INTO GeoSpot (id, XCords, YCords, Cemetery_id) VALUES
(1, 16.9, 56.5, 1),
(2, 16.5, 57.9, 1),
(3, 16.2, 57.1, 1),
(4, 17.2, 58.9, 1),
(5, 20.3, 50.1, 1),
(6, 21.2, 47.1, 1),
(7, 123.3, 145.5, 2),
(8, 124.6, 144.6, 2),
(9, 122.0, 146.4, 2),
(10, 126.7, 147.2, 2),
(11, 120.7, 140.8, 2),
(12, 12.3, 1.5, 3),
(13, 12.6, 2.6, 3),
(14, 13.0, 1.0, 3),
(15, 12.0, 2.2, 3),
(16, 13.7, 2.8, 3),
(17, 14.5, 2.9, 3),
(18, 70.3, 43.5, 4),
(19, 70.6, 44.6, 4),
(20, 71.0, 43.0, 4),
(21, 70.0, 44.2, 4),
(22, 73.7, 42.8, 4),
(23, 71.5, 44.9, 4),
(24, 74.5, 43.9, 4),
(25, 75.0, 41.9, 4),
(26, 70.2, 43.9, 4),
(27, 73.3, 42.6, 4),
(28, 74.3, 42.2, 4),
(29, 74.7, 44.9, 4),
(30, 74.5, 46.7, 4),
(31, 70.8, 41.8, 4);

INSERT INTO Person (id, FullName, GeoSpot_id, YearOfBirth, YearOfDeath, ImageLink) VALUES
(1, 'Эрен Йегер', 1, 835, 854, 'images/img1.png'),
(2, 'Саша Браус', 2, 835, 854, 'images/img2.png'),
(3, 'Эрвин Смит', 3, 809, 851, 'images/img3.png'),
(4, 'Марко Ботт', 4, 835, 850, 'images/img4.png'),
(5, 'Ханджи Зоэ', 5, 809, 854, 'images/img5.png'),
(6, 'Гриша Йегер', 6, 805, 840, 'images/img6.png'),
(7, 'Е Байи', 7, 914, 1021, 'images/img7.png'),
(8, 'Гу Сян', 8, 999, 1020, 'images/img8.png'),
(9, 'Цао Вэньин', 8, 997, 1020, 'images/img9.png'),
(10, 'Гао Чунг', 9, 956, 1019, 'images/img10.png'),
(11, 'Ло Фумэнг', 10, 988, 1020, 'images/img11.png'),
(12, 'Жун Сюань', 11, 943, 978, 'images/img12.png'),
(13, 'Юлия Пчёлкина', 12, 1987, 2012, 'images/img13.png'),
(14, 'Фёдор Прокопенко', 13, 1953, 2012, 'images/img14.png'),
(15, 'Сергей Разумовский', 14, 1992, 2021, 'images/img15.png'),
(16, 'Александра Филипенко', 15, 1987, 2012, 'images/img16.png'),
(17, 'Алексей Капустин', 16, 1986, 2012, 'images/img17.png'),
(18, 'Вениамин Рубинштейн', 17, 1967, 2020, 'images/img18.png'),
(19, 'Силко', 18, 945, 993, 'images/img19.png'),
(20, 'Вандер', 19, 945, 996, 'images/img20.png'),
(21, 'Скай Янг', 20, 960, 990, 'images/img21.png'),
(22, 'Иша', 21, 982, 991, 'images/img22.png'),
(23, 'Виктор', 22, 960, 996, 'images/img23.png'),
(24, 'Джейс Талис', 23, 960, 996, 'images/img24.png'),
(25, 'Кассандра Кирамман', 24, 953, 993, 'images/img25.png'),
(26, 'Тормэн Хоскел', 25, 933, 993, 'images/img26.png'),
(27, 'Ириус Болбек', 26, 912, 993, 'images/img27.png'),
(28, 'Сэйло', 27, 963, 996, 'images/img28.png'),
(29, 'Амбесса Медард', 28, 941, 996, 'images/img29.png'),
(30, 'Бензо', 29, 946, 987, 'images/img30.png'),
(31, 'Мэдди Нолан', 30, 960, 990, 'images/img31.png'),
(32, 'Лорис', 31, 945, 996, 'images/img32.png');

INSERT INTO Descendant (id, FullName, ContactNumber) VALUES
(1, 'Микаса Аккерман', '+79675641275'),
(2, 'Конни Спрингер', '+79567317843'),
(3, 'Леви Аккерман', '+79461563401'),
(4, 'Жан Кирштейн', '+79461259080'),
(5, 'Вэнь Кэсин', '+79567462389'),
(6, 'Гао Сяолянь', '+9875641324'),
(7, 'Мадам Жун', '+79566634563'),
(8, 'Джоу Цзышу', '+79876579897'),
(9, 'Игорь Гром', '+79658451209'),
(10, 'Елена Прокопенко', '+79238516443'),
(11, 'Олег Волков', '+79251853008'),
(12, 'Григорий Филипенко', '+79645761276'),
(13, 'Анастасия Капустина', '+79356091281'),
(14, 'Самуил Рубинштейн', '+79564351900'),
(15, 'Джинкс Паудер', '+79653741634'),
(16, 'Вайолет', '+79328761009'),
(17, 'Химера Талис', '+79534813983'),
(18, 'Кэйтлин Кирамман', '+79341523883'),
(19, 'Мэл Медард', '+79543651234'),
(20, 'Экко', '+79986700131'),
(21, 'Сайнджет', '+79908716410');

INSERT INTO Person_Descendant (Person_id, Descendant_id) VALUES
(1, 1), 
(2, 2),
(3, 3),
(4, 4),
(5, 3),
(6, 1),
(7, 8),
(8, 5),
(10, 6), 
(11, 5), 
(12, 7),
(13, 9),
(14, 10),
(15, 11), 
(16, 12), 
(17, 13),
(18, 14),
(19, 15),
(20, 15),
(20, 16), 
(22, 15), 
(23, 21),
(24, 17),
(25, 18),
(29, 19),
(30, 20);

-- Триггер для автоматического удаления связанных данных
CREATE TRIGGER DeleteGeoSpotAndPerson
AFTER DELETE ON Cemetery
FOR EACH ROW
BEGIN
    DELETE FROM GeoSpot WHERE Cemetery_id = OLD.id;
    DELETE FROM Person WHERE GeoSpot_id IN (
        SELECT id FROM GeoSpot WHERE Cemetery_id = OLD.id
    );
END;

-- Добавление ссылки на картинку
CREATE TRIGGER InsertImageLink
AFTER INSERT ON Person
FOR EACH ROW
BEGIN
    UPDATE Person
    SET ImageLink = "images/img" || NEW.id || ".png"
    WHERE id = NEW.id;
END;
'''

cur.executescript(scr)

print("База данных сброшена!")

connection.close()
