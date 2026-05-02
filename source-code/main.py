#version 1.5

import keyboard as kb
import sys,os,csv
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import random as r

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS',os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

def get_file_path():
    dir = os.path.join(os.getenv("APPDATA"),"MyApp")
    os.makedirs(dir, exist_ok=True)
    file_path = os.path.join(dir, "fav.csv")
    return file_path

print(get_file_path())

style = """
QMainWindow {
    background-color: #2D2D2D;
}
QDialog {
    background-color: #2D2D2D;
}
QSlider::handle:horizontal {
    width: 20px;
    height: 20px;
    margin: -7px 0;
    border-radius: 10px;
}
QSlider#slider_r::sub-page:horizontal {
    background-color: #FF5050;
    border-radius: 3px;
}
QSlider#slider_g::sub-page:horizontal {
    background-color: #50FF50;
    border-radius: 3px;
}
QSlider#slider_b::sub-page:horizontal {
    background-color: #6464FF;
    border-radius: 3px;
}
QSlider#slider_r::handle:horizontal {
    background-color: #ED1C24;
}
QSlider#slider_g::handle:horizontal {
    background-color: #22B14C;
}
QSlider#slider_b::handle:horizontal {
    background-color: #4148CC;
}
QSlider::groove:horizontal {
    height: 6px;
    background: #4B4B4B;
    border-radius: 3px;
}
QLineEdit#text_r {
    font-size: 15px;
    font-family: consolas;
    font-weight: bold;
    background-color: #555555;
    color: #C8C8C8;
    margin: 2px;
    border-radius: 5px;
}
QLineEdit#text_g {
    font-size: 15px;
    font-family: consolas;
    font-weight: bold;
    background-color: #555555;
    color: #C8C8C8;
    margin: 2px;
    border-radius: 5px;
}
QLineEdit#text_b {
    font-size: 15px;
    font-family: consolas;
    font-weight: bold;
    background-color: #555555;
    color: #C8C8C8;
    margin: 2px;
    border-radius: 5px;
}
QLabel#label_colour {
    background-color: #000000;
    height: 30px;
    width: 30px;
    margin: 10px;
    border-radius: 5px;
}
QLabel#label_hexcode {
    background-color: #555555;
    font-size: 20px;
    font-family: consolas;
    font-weight: bold;
    color: #C8C8C8;
    border-radius: 5px;
    padding: 5px 10px;
}
QPushButton {
    border-radius: 5px;
    background-color: #555555;
    font-family: consolas;
    font-weight: bold;
    font-size: 15px;
    color: #C8C8C8;
    padding: 2px 7px;
}
QPushButton:hover {
    background-color: #4B4B4B;
}
QPushButton:pressed {
    background-color: #414141;
}
QPushButton:checked {
    background-color: #414141;
}
QLabel#label_version {
    color: #555555;
    font-family: consolas;
    font-weight: bold;
    font-size: 15px
}
QLineEdit#text_name {
    font-size: 15px;
    font-family: consolas;
    font-weight: bold;
    background-color: #555555;
    color: #C8C8C8;
    margin: 2px;
    border-radius: 5px;
}
QLabel#label_instruction {
    color: #EBEBEB;
    font-family: consolas;
    font-weight: bold;
    font-size: 15px;
}
QLabel#title {
    color: #EBEBEB;
    font-family: consolas;
    font-weight: bold;
    font-size: 25px;
    background-color: #6E6E6E;
    padding-top: 5px;
    padding-bottom: 5px;
    border-radius: 5px;
}
QWidget#list {
    background-color: #373737;
    border-radius: 10px;
}
QLabel#hex {
    font-size: 20px;
    font-family: consolas;
    color: #EBEBEB;
}
QLabel#name {
    font-size: 15px;
    font-family: consolas;
    font-weight: bold;
    color: #C8C8C8;
}
QLabel#no_fav {
    color: #C8C8C8;
    font-family: consolas;
    font-size: 15px;
    margin-top: 15px;
}
QWidget#wid {
    background-color: #2D2D2D;
}
QScrollArea {
    border: none;
}
"""

def Hexadecimal(n):
    hexa = {10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'}
    hexa_keys = list(hexa.keys())

    mod = n % 16
    floor = n // 16

    if mod in hexa_keys:
        ch2 = hexa[mod]
    elif mod not in hexa_keys:
        ch2 = str(mod)

    if floor in hexa_keys:
        ch1 = hexa[floor]
    elif floor not in hexa_keys:
        ch1 = str(floor)

    hexadecimal = ch1 + ch2
    return hexadecimal

class Preview(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Preview")
        self.setGeometry(683,384,300,300)
        self.setWindowIcon(QIcon(resource_path("logo.png")))

class SaveFav(QDialog):
    name = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add to Favourite")
        self.setFixedSize(300,150)
        self.setWindowIcon(QIcon(resource_path("logo.png")))
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        
        label_instruction = QLabel("Add this colour to your\n Favourite List",self)
        self.text_name = QLineEdit(self)
        button_submit = QPushButton("Add",self)
        button_cancel = QPushButton("Cancel",self)

        label_instruction.setObjectName("label_instruction")
        label_instruction.setAlignment(Qt.AlignCenter)
        label_instruction.setFixedSize(200,30)

        self.text_name.setObjectName("text_name")
        self.text_name.setFixedSize(250,30)
        self.text_name.setPlaceholderText("Enter Name")

        button_submit.setFixedSize(50,25)
        button_submit.setCursor(Qt.PointingHandCursor)
        button_submit.clicked.connect(self.send_name)

        button_cancel.setFixedSize(62,25)
        button_cancel.setCursor(Qt.PointingHandCursor)
        button_cancel.clicked.connect(self.close_window)

        layout = QVBoxLayout()

        buttons = QHBoxLayout()
        buttons.setAlignment(Qt.AlignCenter)
        buttons.addWidget(button_submit)
        buttons.addWidget(button_cancel)

        layout.addWidget(label_instruction,alignment=Qt.AlignCenter | Qt.AlignBottom)
        layout.addWidget(self.text_name,alignment=Qt.AlignCenter | Qt.AlignBottom)
        layout.addLayout(buttons)

        self.setLayout(layout)

        self.setStyleSheet(style)
    
    def send_name(self):
        if self.text_name.text() == "":
            self.text_name.setPlaceholderText("First Enter a Name")
            QTimer.singleShot(1500, lambda: self.text_name.setPlaceholderText("Enter Name"))
        else:
            text = self.text_name.text()
            self.name.emit(text)
            self.close()
    
    def close_window(self):
        self.close()

class confirmation(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Confirmation")
        self.setFixedSize(300,150)
        self.setWindowIcon(QIcon(resource_path("logo.png")))
        
        label_instruction = QLabel("Are you sure you want to delete\nthis colour?",self)
        button_delete = QPushButton("Delete",self)
        button_cancel = QPushButton("Cancel",self)

        label_instruction.setObjectName("label_instruction")
        label_instruction.setAlignment(Qt.AlignCenter)

        button_delete.clicked.connect(self.accept)
        button_delete.setFixedSize(62,25)
        button_delete.setCursor(Qt.PointingHandCursor)

        button_cancel.clicked.connect(self.reject)
        button_cancel.setFixedSize(62,25)
        button_cancel.setCursor(Qt.PointingHandCursor)

        layout = QVBoxLayout()
        
        buttons = QHBoxLayout()
        buttons.setAlignment(Qt.AlignCenter)
        buttons.addWidget(button_delete)
        buttons.addWidget(button_cancel)

        layout.addWidget(label_instruction)
        layout.addLayout(buttons)

        self.setLayout(layout)

        self.setStyleSheet(style)

class FavList(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(resource_path("logo.png")))
        self.setWindowTitle("Your Favourites")
        self.setGeometry(603,304,300,300)

        self.title = QLabel("Favourites",self)
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignLeft)

        self.load_fav()

    def load_fav(self):
        grid = QGridLayout()
        widget = QWidget()
        self.setCentralWidget(widget)

        fav_lists = QVBoxLayout()
        widget_lists = QWidget()
        widget_lists.setObjectName('lists')

        file = get_file_path()

        with open(file,'r',newline='') as f:
                reader = list(csv.reader(f))

        if len(reader) == 0:
            no_fav = QLabel("No colour in Favourite",self)
            no_fav.setObjectName('no_fav')

            grid.setAlignment(Qt.AlignTop)
            grid.setContentsMargins(0,0,0,0)
            grid.addWidget(self.title,0,0)
            grid.addWidget(no_fav,1,0,alignment=Qt.AlignCenter)
            widget.setLayout(grid)
        else:
            scroll = QScrollArea(self)
            scroll.setWidgetResizable(True)

            for index,row in enumerate(reader):
                label_hex = QLabel(row[1],self)
                label_name = QLabel(row[0],self)

                label_hex.setObjectName('hex')
                label_hex.setTextInteractionFlags(Qt.TextSelectableByMouse)
                label_hex.setCursor(Qt.IBeamCursor)

                label_name.setObjectName('name')

                del_btn = QPushButton(self)
                del_btn.setFixedSize(25,25)
                del_btn.setCursor(Qt.PointingHandCursor)
                del_btn.setIcon(QIcon(resource_path('delete.png')))
                del_btn.setIconSize(QSize(20,20))
                del_btn.clicked.connect(lambda checked, i=index: self.delete(i))

                fav_list = QGridLayout()
                widget_list = QWidget()
                widget_list.setObjectName('list')

                fav_list.addWidget(label_hex,0,0)
                fav_list.addWidget(label_name,1,0)
                fav_list.addWidget(del_btn,0,1)
                widget_list.setLayout(fav_list)

                fav_lists.addWidget(widget_list,alignment=Qt.AlignTop)
        
            widget_lists.setLayout(fav_lists)

            scroll.setWidget(widget_lists)
            widget_lists.setObjectName('wid')

            grid.setAlignment(Qt.AlignTop)
            grid.setContentsMargins(0,0,0,0)
            grid.addWidget(self.title,0,0)
            grid.addWidget(scroll,1,0,alignment=Qt.AlignTop)
            widget.setLayout(grid)

        self.setStyleSheet(style)

    def delete(self, row):
        dialog = confirmation()

        if dialog.exec_() == QDialog.Rejected:
            return
        
        file = get_file_path()

        with open(file,'r',newline='') as fr:
            rows = list(csv.reader(fr))

        del rows[row]

        with open(file,'w',newline='') as fw:
            write = csv.writer(fw)
            write.writerows(rows)
        
        self.load_fav()
    
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Colour Picker")
        self.setWindowIcon(QIcon(resource_path("logo.png")))
        self.setFixedSize(425,200)

        self.text_r = QLineEdit("0",self)
        self.slider_r = QSlider(Qt.Horizontal, self)

        self.text_b = QLineEdit("0",self)
        self.slider_g = QSlider(Qt.Horizontal, self)

        self.text_g = QLineEdit("0",self)
        self.slider_b = QSlider(Qt.Horizontal, self)

        self.label_colour = QLabel(self)

        self.label_hexcode = QLabel("#000000", self)

        self.button_copy = QPushButton(self)
        self.button_pin = QPushButton(self)
        self.button_random = QPushButton(self)
        self.button_preview = QPushButton(self)
        self.button_fav = QPushButton(self)
        self.button_favlist = QPushButton(self)

        self.UI()

    def UI(self):
        widget = QWidget()
        sub_widget = QWidget()
        button_widget = QWidget()
        self.setCentralWidget(widget)

        self.text_r.setAlignment(Qt.AlignCenter)
        self.text_r.setObjectName("text_r")
        self.text_r.setFixedWidth(45)
        self.text_r.setFixedHeight(30)
        self.text_r.setReadOnly(False)
        self.text_r.setValidator(QIntValidator(1,255,self))
        self.text_r.textChanged.connect(self.slider_value_r)

        self.slider_r.setMinimum(0)
        self.slider_r.setMaximum(255)
        self.slider_r.setValue(0)
        self.slider_r.setCursor(Qt.PointingHandCursor)
        self.slider_r.setObjectName("slider_r")
        self.slider_r.setMinimumWidth(200)
        self.slider_r.setMaximumWidth(200)
        self.slider_r.valueChanged.connect(self.red)
        self.slider_r.valueChanged.connect(self.hexcode)
        self.slider_r.setFocusPolicy(Qt.NoFocus)
        self.slider_r.setToolTip("Red Slider")

        self.text_g.setAlignment(Qt.AlignCenter)
        self.text_g.setObjectName("text_g")
        self.text_g.setFixedWidth(45)
        self.text_g.setFixedHeight(30)
        self.text_g.setReadOnly(False)
        self.text_g.setValidator(QIntValidator(1,255,self))
        self.text_g.textChanged.connect(self.slider_value_g)

        self.slider_g.setMinimum(0)
        self.slider_g.setMaximum(255)
        self.slider_g.setValue(0)
        self.slider_g.setCursor(Qt.PointingHandCursor)
        self.slider_g.setObjectName("slider_g")
        self.slider_g.setMinimumWidth(200)
        self.slider_g.setMaximumWidth(200)
        self.slider_g.valueChanged.connect(self.green)
        self.slider_g.valueChanged.connect(self.hexcode)
        self.slider_g.setFocusPolicy(Qt.NoFocus)
        self.slider_g.setToolTip("Green Slider")

        self.text_b.setAlignment(Qt.AlignCenter)
        self.text_b.setObjectName("text_b")
        self.text_b.setFixedWidth(45)
        self.text_b.setFixedHeight(30)
        self.text_b.setReadOnly(False)
        self.text_b.setValidator(QIntValidator(1,255,self))
        self.text_b.textChanged.connect(self.slider_value_b)

        self.slider_b.setMinimum(0)
        self.slider_b.setMaximum(255)
        self.slider_b.setValue(0)
        self.slider_b.setCursor(Qt.PointingHandCursor)
        self.slider_b.setObjectName("slider_b")
        self.slider_b.setMinimumWidth(200)
        self.slider_b.setMaximumWidth(200)
        self.slider_b.valueChanged.connect(self.blue)
        self.slider_b.valueChanged.connect(self.hexcode)
        self.slider_b.setFocusPolicy(Qt.NoFocus)
        self.slider_b.setToolTip("Blue Slider")

        self.label_colour.setObjectName("label_colour")
        self.label_colour.setFixedSize(125,125)

        self.label_hexcode.setObjectName("label_hexcode")
        self.label_hexcode.setAlignment(Qt.AlignCenter)
        self.label_hexcode.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label_hexcode.setCursor(Qt.IBeamCursor)
        self.label_hexcode.setFixedSize(125,40)

        self.button_copy.setIcon(QIcon(resource_path("copy.png")))
        self.button_copy.setIconSize(QSize(20,20))
        self.button_copy.setFixedSize(25,25)
        self.button_copy.setCursor(Qt.PointingHandCursor)
        self.button_copy.clicked.connect(self.copy)
        self.button_copy.setObjectName("button_copy")
        self.button_copy.setToolTip("Copy Hexcode")
        # self.button_copy.setText("C")

        self.button_pin.setIcon(QIcon(resource_path("pin.png")))
        self.button_pin.setIconSize(QSize(20, 20))
        self.button_pin.setFixedSize(25, 25)
        self.button_pin.setCursor(Qt.PointingHandCursor)
        self.button_pin.setCheckable(True)
        self.button_pin.toggled.connect(self.pin)
        self.button_pin.setToolTip("Pin Window")
        # self.button_pin.setText("P")

        self.button_random.setIcon(QIcon(resource_path("random.png")))
        self.button_random.setIconSize(QSize(17,17))
        self.button_random.setFixedSize(25,25)
        self.button_random.setCursor(Qt.PointingHandCursor)
        self.button_random.clicked.connect(self.random)
        self.button_random.setToolTip("Set Random colour")
        # self.button_random.setText("R")

        self.button_preview.setFixedSize(25,25)
        self.button_preview.setIcon(QIcon(resource_path("preview.png")))
        self.button_preview.setIconSize(QSize(20,20))
        self.button_preview.setCursor(Qt.PointingHandCursor)
        self.button_preview.clicked.connect(self.preview)
        self.button_preview.setToolTip("Open Preview window")
        # self.button_preview.setText("P")

        self.button_fav.setFixedSize(25,25)
        self.button_fav.setCursor(Qt.PointingHandCursor)
        self.button_fav.setToolTip("Add to Favourite")
        self.button_fav.setIcon(QIcon(resource_path('add_to_fav.png')))
        self.button_fav.setIconSize(QSize(20,20))
        # self.button_fav.setText("F")
        self.button_fav.clicked.connect(self.add_to_fav)

        self.button_favlist.setFixedSize(25,25)
        self.button_favlist.setCursor(Qt.PointingHandCursor)
        self.button_favlist.setToolTip("Your Favourites")
        self.button_favlist.setIcon(QIcon(resource_path('star.png')))
        self.button_favlist.setIconSize(QSize(20,20))
        # self.button_favlist.setText("Fl")
        self.button_favlist.clicked.connect(self.open_fav_list)

        label_version = QLabel("Version-1.8.0", self)
        label_version.setObjectName("label_version")
        label_version.setGeometry(0,184,150,20)

        grid_1 = QGridLayout()
        grid_button = QGridLayout()
        grid = QGridLayout()

        grid_1.addWidget(self.slider_r, 0, 0)
        grid_1.addWidget(self.slider_g, 1, 0)
        grid_1.addWidget(self.slider_b, 2, 0)
        grid_1.addWidget(self.text_r, 0, 1)
        grid_1.addWidget(self.text_g, 1, 1)
        grid_1.addWidget(self.text_b, 2, 1)
        sub_widget.setLayout(grid_1)

        grid_button.addWidget(self.button_copy,0,5)
        grid_button.addWidget(self.button_pin,0,4)
        grid_button.addWidget(self.button_random,0,3)
        grid_button.addWidget(self.button_preview,0,2)
        grid_button.addWidget(self.button_fav,0,1)
        grid_button.addWidget(self.button_favlist,0,0)
        button_widget.setLayout(grid_button)

        grid.addWidget(sub_widget,0,0)
        grid.addWidget(button_widget,1,0,alignment=Qt.AlignRight)
        grid.addWidget(self.label_colour,0,1)
        grid.addWidget(self.label_hexcode,1,1)
        widget.setLayout(grid)

        self.setStyleSheet(style)

        def inc():
            self.slider_r.setValue(self.slider_r.value() + 1)
            self.slider_g.setValue(self.slider_g.value() + 1)
            self.slider_b.setValue(self.slider_b.value() + 1)
        
        def dec():
            self.slider_r.setValue(self.slider_r.value() - 1)
            self.slider_g.setValue(self.slider_g.value() - 1)
            self.slider_b.setValue(self.slider_b.value() - 1)

        kb.add_hotkey('right', lambda: inc())
        kb.add_hotkey('left', lambda: dec())

    def red(self,value):
        self.text_r.setText(f"{value}")

    def green(self,value):
        self.text_g.setText(f"{value}")

    def blue(self,value):
        self.text_b.setText(f"{value}")

    def hexcode(self):
        r = self.slider_r.value()
        g = self.slider_g.value()
        b = self.slider_b.value()

        rh = Hexadecimal(r)
        gh = Hexadecimal(g)
        bh = Hexadecimal(b)

        hexa = f"#{rh}{gh}{bh}"
        self.label_hexcode.setText(hexa)
        self.label_colour.setStyleSheet(f"background-color: {hexa}")

    def copy(self):
        clipboard = QApplication.clipboard()
        text = self.label_hexcode.text()
        clipboard.setText(text)

        self.button_copy.setText("Copied")
        self.button_copy.setIcon(QIcon())
        self.button_copy.setFixedSize(65,25)
        def after():
            self.button_copy.setIcon(QIcon(resource_path("copy.png")))
            self.button_copy.setText("")
            self.button_copy.setFixedSize(25, 25)

        QTimer.singleShot(1000, lambda: after())

    def pin(self, checked):
        self.setWindowFlag(Qt.WindowStaysOnTopHint, checked)
        self.show()

    def slider_value_r(self):
        num = self.text_r.text()
        
        if num == "":
            self.slider_r.setValue(0)
        else:
            num = int(num)
            self.slider_r.setValue(num)
            
    def slider_value_r(self):
        num = self.text_r.text()
        
        if num == "":
            self.slider_r.setValue(0)
        else:
            num = int(num)
            self.slider_r.setValue(num)

    def slider_value_g(self):
        num = self.text_g.text()
        
        if num == "":
            self.slider_g.setValue(0)
        else:
            num = int(num)
            self.slider_g.setValue(num)
 
    def slider_value_b(self):
        num = self.text_b.text()
        
        if num == "":
            self.slider_b.setValue(0)
        else:
            num = int(num)
            self.slider_b.setValue(num)
    
    def random(self):
        self.slider_r.setValue(r.randint(0,255))
        self.slider_g.setValue(r.randint(0,255))
        self.slider_b.setValue(r.randint(0,255))

    def preview(self):
        self.new_window = Preview()
        self.new_window.show()

        colour = self.label_hexcode.text()

        self.new_window.setStyleSheet(f"background-color: {colour};")
    
    def add_to_fav(self):
        self.newWindow = SaveFav()
        self.newWindow.name.connect(self.receive)
        self.newWindow.show()

    def receive(self,text):
        self.data = text

        file = get_file_path()

        text = self.label_hexcode.text()
        fav = [self.data,text]

        if not os.path.exists(file):
            with open(file, "w", newline='') as f:
                writer = csv.writer(f,delimiter=',')
                writer.writerow(fav)

        with open(file, 'a', newline='') as f:
            writer = csv.writer(f,delimiter=',')
            writer.writerow(fav)
    
    def open_fav_list(self):
        self.favWindow = FavList()
        self.favWindow.show()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()