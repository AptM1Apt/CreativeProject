import sqlite3 as s 

connection = s.connect('CemeteryLookUp.db')

cur = connection.cursor()

scr = '''
--Таблица с названиями кладбищ, контактами администрации и охраны
create table Cemetery(
id INTEGER PRIMARY KEY AUTOINCREMENT,
Title varchar(60),
AdminContactNumber varchar(14),
GuardContactNumber varchar(14));

--Геопозиции захоронений (координаты) с id кладбища
create table GeoSpot(
id INTEGER PRIMARY KEY AUTOINCREMENT,
XCords float,
YCords float,
Cemetery_id int,
foreign key (Cemetery_id) references Cemetery(id) 
 on update cascade
    on delete no action);

--Имена захороненных с id захоронений и годами жизни
create table Person(
id INTEGER PRIMARY KEY AUTOINCREMENT,
FullName varchar(45),
GeoSpot_id int,
YearsOfLife varchar(20),
foreign key (GeoSpot_id) references GeoSpot(id) 
 on update cascade
 on delete no action);

--Имена близких родственников с контактными номерами
create table Descendant(
id INTEGER PRIMARY KEY AUTOINCREMENT,
FullName varchar(45),
ContactNumber varchar(14));

--Таблица связи m2m между захороненными и родственниками
create table Person_Descendant(
Person_id int,
Descendant_id int,
primary key (Person_id, Descendant_id),
foreign key (Person_id) references Person(id)
 on update cascade
 on delete no action,
foreign key (Descendant_id) references Descendant(id)
 on update cascade
 on delete no action);

--AoT
insert into cemetery (id, Title, AdminContactNumber, GuardContactNumber) values
(1, 'Покой Эльдии', '+79027027590', '+79009145657');

insert into geospot (id, XCords, YCords, Cemetery_id) values
(1, 16.9, 56.5, 1),
(2, 16.5, 57.9, 1),
(3, 16.2, 57.1, 1),
(4, 17.2, 58.9, 1),
(5, 20.3, 50.1, 1),
(6, 21.2, 47.1, 1);

insert into person (id, FullName, GeoSpot_id, YearsOfLife) values
(1, 'Эрен Йегер', 1, '835 - 854'),
(2, 'Саша Браус', 2, '835 - 854'),
(3, 'Эрвин Смит', 3, '809 - 851'),
(4, 'Марко Ботт', 4, '835 - 850'),
(5, 'Ханджи Зоэ', 5, '809 - 854'),
(6, 'Гриша Йегер', 6, '805 - 840');

insert into descendant(id, FullName, ContactNumber) values 
(1, 'Микаса Аккерман', '+79675641275'),
(2, 'Конни Спрингер', '+79567317843'),
(3, 'Леви Аккерман', '+79461563401'),
(4, 'Жан Кирштейн', '+79461259080');

insert into person_descendant(Person_id, Descendant_id) values
(1, 1), 
(2, 2),
(3, 3),
(4, 4),
(5, 3),
(6, 1);

--Word of Honor
insert into cemetery (id, Title, AdminContactNumber, GuardContactNumber) values
 (2, 'Памяти Героям', '+79027027590', '+79009145657');
    
insert into geospot (id, XCords, YCords, Cemetery_id) values
 (7, 123.3, 145.5, 2),
    (8, 124.6, 144.6, 2),
    (9, 122.0, 146.4, 2),
    (10, 126.7, 147.2, 2),
    (11, 120.7, 140.8, 2);
    
insert into person (id, FullName, GeoSpot_id, YearsOfLife) values
 (7, 'Е Байи', 7, '914-1021'),
    (8, 'Гу Сян', 8, '999-1020'),
    (9, 'Цао Вэньин', 8, '997-1020'),
    (10, 'Гао Чунг', 9, '956-1019'),
    (11, 'Ло Фумэнг', 10, '988-1020'),
    (12, 'Жун Сюань', 11, '943-978');
    
insert into descendant (id, FullName, ContactNumber) values
 (5, 'Вэнь Кэсин', '+79567462389'),
    (6, 'Гао Сяолянь', '+9875641324'),
    (7, 'Мадам Жун', '+79566634563'),
    (8, 'Джоу Цзышу', '+79876579897');
    
insert into person_descendant (Person_id, Descendant_id) values
 (7, 8),
    (8, 5),
    (10, 6), 
    (11, 5), 
    (12, 7);
--Майор Гром
insert into cemetery (id, Title, AdminContactNumber, GuardContactNumber) values
 (3, 'Питерское городское кладбище', '+79027027590', '+79009145657');
    
insert into geospot (id, XCords, YCords, Cemetery_id) values
 (12, 12.3, 1.5, 3),
    (13, 12.6, 2.6, 3),
    (14, 13.0, 1.0, 3),
    (15, 12.0, 2.2, 3),
    (16, 13.7, 2.8, 3),
    (17, 14.5, 2.9, 3);
    
insert into person (id, FullName, GeoSpot_id, YearsOfLife) values
 (13, 'Юлия Пчёлкина', 12, '1987 - 2012'),
    (14, 'Фёдор Прокопенко', 13, '1953 - 2012'),
    (15, 'Сергей Разумовский', 14, '1992-2021'),
    (16, 'Александра Филипенко', 15, '1987-2012'),
    (17, 'Алексей Капустин', 16, '1986-2012'),
    (18, 'Вениамин Рубинштейн', 17, '1967-2020');
    
insert into descendant (id, FullName, ContactNumber) values
 (9, 'Игорь Гром', '+79658451209'),
    (10, 'Елена Прокопенко', '+79238516443'),
    (11, 'Олег Волков', '+79251853008'),
    (12, 'Григорий Филипенко', '+79645761276'),
    (13, 'Анастасия Капустина', '+79356091281'), 
    (14, 'Самуил Рубинштейн', '+79564351900');
    
insert into person_descendant (Person_id, Descendant_id) values
 (13, 9),
    (14, 10),
    (15, 11), 
    (16, 12), 
    (17, 13),
    (18, 14);
    
--Arcane
insert into cemetery (id, Title, AdminContactNumber, GuardContactNumber) values
 (4, 'Павильон Вечного Покоя', '+79027027590', '+79009145657');
    
insert into geospot (id, XCords, YCords, Cemetery_id) values
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
    
insert into person (id, FullName, GeoSpot_id, YearsOfLife) values
 (19, 'Силко', 18, '945 - 993'),
    (20, 'Вандер', 19, '945 - 996'),
    (21, 'Скай Янг', 20, '960 - 990'),
    (22, 'Иша', 21, '982 - 991'),
    (23, 'Виктор', 22, '960 - 996'),
    (24, 'Джейс Талис', 23, '960 - 996'),
    (25, 'Кассандра Кирамман', 24, '953 - 993'),
    (26, 'Тормэн Хоскел', 25, '933 - 993'),
    (27, 'Ириус Болбек', 26, '912 - 993'),
    (28, 'Сэйло', 27, '963 - 996'),
    (29, 'Амбесса Медард', 28, '941 - 996'),
    (30, 'Бензо', 29, '946 - 987'),
    (31, 'Мэдди Нолан', 30, '960 - 990'), 
    (32, 'Лорис', 31, '945 - 996');
    
insert into descendant (id, FullName, ContactNumber) values
 (15, 'Джинкс Паудер', '+79653741634'),
    (16, 'Вайолет', '+79328761009'),
    (17, 'Химера Талис', '+79534813983'),
    (18, 'Кэйтлин Кирамман', '+79341523883'),
    (19, 'Мэл Медард', '+79543651234'), 
    (20, 'Экко', '+79986700131'),
    (21, 'Сайнджет', '+79908716410');
    
insert into person_descendant (Person_id, Descendant_id) values
 (19, 15),
    (20, 15),
    (20, 16), 
    (22, 15), 
    (23, 21),
    (24, 17),
    (25, 18),
    (29, 19),
    (30, 20);

-- Добавляем столбец ImageLink
ALTER TABLE Person
ADD COLUMN ImageLink VARCHAR(255);

-- Заполняем NULL значения в столбце ImageLink по указанному алгоритму
UPDATE Person
SET ImageLink = "images/img" || id || ".png"
WHERE ImageLink IS NULL;

-- Создаем триггер для автоматического заполнения ImageLink
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

print("And we are done!")

connection.close()