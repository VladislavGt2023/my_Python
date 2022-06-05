# симулятор кофемашины

import sys
from PyQt5.QtWidgets import (QApplication, QDialog, QGroupBox, QLabel, QRadioButton,
                             QTextEdit, QLCDNumber, QPushButton, QGridLayout,
                             QMessageBox, QVBoxLayout)
from PyQt5.QtGui import  QIcon, QPixmap, QMovie #  *
from PyQt5.QtCore import QTimer, QSize, QRect


class MyApp(QDialog):

    def __init__(self):
        super().__init__()
        self.mybg = '#FFE4E1' # mistyrose туманно-розовый
        self.myfg = '#0000CD' # '#7B68EE' # mediumslateblue	умеренный серо-голубой
        self.setStyleSheet(f'background: {self.mybg}; color: {self.myfg}; \
font-size: 18px;font-family: "Bookman Old Style";')
        # http://citforum.ru/nets/semenov/10/color_tab.shtml

        self.initUI()

    def initUI(self):
######################### инициализация переменных

        self.timer = QTimer(self) # определяем таймер
        self.timer.timeout.connect(self.showtime)
        self.timer.start(1000)
        self.i = 0
        self.vibor = 0 # что выбрано из напитков
        self.total_count = 0 # сколько сделано напитков
        self.total_many = 0 # на какую сумму (выторг)

        self.myStyleBox = '''
            QGroupBox {
                margin-top: 2ex;
            }
            QGroupBox:enabled {
                border: 3px solid brown;
                border-radius: 5px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 3ex;
            }
        '''
        # margin-top отступ от заголовка вниз см. описание ниже
        # http://doc.crossplatform.ru/qt/4.6.x/stylesheet-examples.html
        
        self.myhelp = [
            "Welcome to the Python® CoffeeMachine™ 3.1.1!",
            "Зачекайте поки ми підготуємо машину.",
            "Завантаження кавамашини ...",
            "Перевірка облікових даних ...",
            "Розігрів...",
            "Готуємось створювати напої ...",
            "Ще дещо за технологією ...",
            "Готові!"
            ]

        self.assort = [
                    ('Американо', 21, 'Americano3.png', ('кофе',7),('вода',90),('посуд',1)),
                    ('Американо з молоком', 26, 'AmericanoM3.png', ('кофе',7),('вода',90),('молоко',150),('посуд',1)),
                    ('Гарячий шоколад',  37, 'HotCocolate3.png', ('шоколад',100),('вершки',60),('посуд',1)),
                    ('Допіо',  29, 'Doppio3.png', ('кофе',14),('вода',56),('посуд',1)),
                    ('Еспресо',  19, 'Espresso3.png', ('кофе',7),('вода',28),('посуд',1)),
                    ('Какао',  39, 'Cacao3.png', ('какао',15),('цукор',90),('молоко',200),('посуд',1)),
                    ('Капучино', 28, 'Capuchino3.png', ('кофе',15),('вода',60),('молоко',60),('пінка',15),('посуд',1)),
                    ('Лате', 28, 'Latte3.png', ('кофе',7), ('вода',28),('молоко',250),('посуд',1)),
                    ('Лунго', 19, 'Lungo3.png', ('кофе',7), ('вода',70),('посуд',1)),
                    ('Раф кава', 34, 'Raf3.png', ('кофе',7),('вода',50),('вершки',100),('посуд',1)),
                    ('Ристрето', 19, 'Ristretto3.png', ('кофе',7),('вода',15),('посуд',1)),
                    ('Флет-вайт', 35, 'FletWhite3.png', ('кофе',14),('вода',60),('молоко',110),('посуд',1))
                    ]
        # ищем материалы в рецептах чтобы всем хватило по разу
        temp = {} # словрь
        ind = [] # список
        for i in range(len(self.assort)):
            rezept = self.assort[i][3:]
            for el in rezept:
                temp.setdefault(el[0], 0) # zp*10)
                temp[el[0]] += el[1] # zp
        self.smaterial = dict(sorted(temp.items())) # сортируем по алфавиту
        self.material = [(k, v*3) for k, v in self.smaterial.items()] # рабочий кортеж
        #self.material = [('вершки', 600), ('вода', 900), ('какао', 150), ('кофе', 70), ('молоко', 1500), ('посуд', 20), ('цукор', 900), ('шоколад', 1000)]
        # макет приложения в ТАБЛИЦЕ три GroupBpx
        grid = QGridLayout() # макет сетки, чтобы разместить рамку группы.
        grid.addWidget(self.createGroup1(), 0, 0)
        grid.addWidget(self.createGroup2(), 0, 1)
        grid.addWidget(self.createGroup3(), 0, 2)
        self.setLayout(grid)

        self.setWindowTitle('Віртуальна кавамашина пригощає напоями.')
        self.setWindowIcon(QIcon('myIcon.png'))
        self.resize(900, 500)
        self.show()

    def createGroup1(self): # ЛЕВАЯ панель
        groupbox1 = QGroupBox('А с о р т и м е н т') #предоставляет рамку с заголовком.
        groupbox1.setStyleSheet(self.myStyleBox)
        grid_ass = QGridLayout() # макет сетки, чтобы разместить рамку группы.
        self.setLayout(grid_ass)
        mysize = 16

        for i in range(len(self.assort)): # ПОКАЗАТЬ ассортимент
            lbl_n = QLabel(f'{self.assort[i][0]} ', self)
            lbl_p = QLabel(f'{self.assort[i][1]} грн. ', self)
            cmd = QPushButton('', self)
            cmd.setMinimumSize(40, 40)
            cmd.setIcon(QIcon(QPixmap(self.assort[i][2])))
            cmd.setIconSize(QSize(48, 48)) # установить размер изображения
            cmd.clicked.connect(lambda state, x=i: self.showmy(x))
            # https://stackoverflow.com/questions/35819538/using-lambda-expression-to-connect-slots-in-pyqt
            
            grid_ass.addWidget(cmd, i, 0)
            grid_ass.addWidget(lbl_n, i, 1)
            grid_ass.addWidget(lbl_p, i, 2)

        groupbox1.setLayout(grid_ass)
        return groupbox1

    def createGroup2(self): # ЦЕНТР панель
        groupbox2 = QGroupBox('Табло керування')
        groupbox2.setStyleSheet(f'background: lightgray; color: black; font-size: 16px;')
        self.lbl = QLabel('', self)
        self.lbl.setGeometry(QRect(10, 18, 301, 251))
        self.lbl.setMinimumSize(300, 250)
        self.lbl.setMaximumSize(300, 250)
        self.gif = QMovie('01_broneboynyi_kofe.gif')                     # !!!
        self.gif.setScaledSize(QSize(300, 250)) 

        self.lbl.setMovie(self.gif)
        self.gif.start()
        
        self.radio1 = QRadioButton('Вибір')
        self.radio2 = QRadioButton('Дозаправка')
        self.radio1.toggled.connect(self.onClicked)
        self.radio2.toggled.connect(self.onClicked) 
        self.text = QTextEdit() # для отображения выбора позиции из ассоритимента
        self.text.setFixedSize(300, 200)
        myStyle = 'border-style: outset; border-width: 2px; border-color: gray; font-size: 14px;'
        self.text.setStyleSheet(myStyle)
    
        self.cmdYES = QPushButton('Підтвердити вибір', self)
        self.cmdYES.setEnabled(False)
        self.cmdYES.clicked.connect(self.my_ini)
        self.ttl = QLabel(f'Порцій - {self.total_count}, на суму - {self.total_many}', self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.lbl)
        vbox.addWidget(self.radio1)
        vbox.addWidget(self.radio2)
        vbox.addWidget(self.text)
        vbox.addWidget(self.cmdYES)
        vbox.addWidget(self.ttl)

        groupbox2.setLayout(vbox)
        return groupbox2

    def createGroup3(self): # ПРАВАЯ панель
        groupbox3 = QGroupBox('І н р г а д і є н т и')
        groupbox3.setStyleSheet(self.myStyleBox)
        self.grid_ing = QGridLayout() # макет сетки, чтобы разместить рамку группы.
        self.setLayout(self.grid_ing)

        self.mydict = {} # словарь lcdNumber для обновлений
        for i in range(len(self.material)):
            self.lbl_n = QLabel(f'{self.material[i][0]} ', self)
            self.lcd = QLCDNumber()
            self.lcd.setDigitCount(4)
            self.lcd.display(self.material[i][1])
            self.lcd.setMinimumSize(150, 60)
            self.mydict.setdefault(self.material[i][0], self.lcd)

            self.grid_ing.addWidget(self.lbl_n, i, 0)
            self.grid_ing.addWidget(self.lcd, i, 1)

        groupbox3.setLayout(self.grid_ing)
        return groupbox3

    def dozapravka(self):# Берем МАТЕРИАЛ и обновляем ЗАПАС mydict--lcdNumber
        for el in self.material:
            self.ob = self.mydict.get(el[0])
            zn = el[1]
            self.mydict.setdefault(el[0], zn)
            self.ob.display(zn)

    def  onClicked(self): # делаем активной кнопку "ПОДТВЕРДИТЬ ВЫБОР" и меняем ее цвет
        self.cmdYES.setStyleSheet('background: sienna; color: white; font-size: 22px;')
        self.cmdYES.setEnabled(True)

    def showtime(self): # показать процесс ВКЛЮЧЕНИЯ машины ПОСТРОЧНО с задержкой
        if self.i < len(self.myhelp):
            self.text.append(self.myhelp[self.i])
        else:
            self.timer.stop()
        self.i += 1

    def showmy(self, num): # какой напиток выбран
        self.vibor = num
        self.text.clear()
        self.text.append(f'\n\nВибрано -  {self.assort[self.vibor][0]}')

    def analiz(self): # АНАЛИЗ ВОЗМОЖНОСТИ ПРИГОТОВЛЕНИЯ
        self.text.clear()
        rezept = self.assort[self.vibor][3:]
        # контроль наличия запаса материалов
        ind = None
        for el in rezept:
            self.ob = self.mydict.get(el[0])
            zp = self.ob.value() # запас
            pt = el[1] # потрібно
            if pt > zp:
                ind = True
                self.text.append(f'{el[0]} - у дефіциті, потрібно {pt} а є {zp}')
        if ind:
            self.text.append('\nМатеріала не вистачає')
            return
        # зменшуэмо запас матерілів якщо готуємо напій
        self.text.append(f'виготовлення -  {self.assort[self.vibor][0]} \n')
        for el in rezept:
            self.ob = self.mydict.get(el[0])
            zn = self.ob.value() - el[1]
            self.mydict.setdefault(el[0], zn)
            self.ob.display(zn)
            self.text.append(f' - {el[0]} використано -> {el[1]}')

        self.text.append(f'\nЗаберіть свій - {self.assort[self.vibor][0]}')
        self.total_count += 1
        self.total_many += self.assort[self.vibor][1]
        self.ttl.setText(f'Порцій - {self.total_count}, на суму - {self.total_many}')

    def my_ini(self): # ИЛИ ДОЗАПРАВКА ЛИБО приготовление НАПИТКА
        if self.radio2.isChecked():
            self.dozapravka()
            return
        soob = self.assort[self.vibor][0]
        self.otw = QMessageBox.information(self, 'Процесс створення',
                'Ви дійсно будете готувати каву\n' + soob, 
                                QMessageBox.Yes | QMessageBox.No)
        if self.otw == QMessageBox.Yes:
            self.analiz()
#########################

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())

