import sys
import requests
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from ui_07 import Ui_MainWindow
import re


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.spn = 0.002
        self.camera = []
        self.current_coord = []

    def show_map(self):
        address = self.lineEdit.text()

        if len(address) != 0:
            sp = re.findall(r"\d*\.\d*", address)

            if not self.camera:
                self.current_coord = sp.copy()
                self.camera = list(map(float, sp))
            if len(sp) != 2:
                api_key = "8013b162-6b42-4997-9691-77b7074026e0"
                server_address = 'http://geocode-maps.yandex.ru/1.x/?'
                geocoder_request = f'{server_address}apikey={api_key}&geocode={address}&format=json'
                response = requests.get(geocoder_request)
                if response:
                    json_response = response.json()
                    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                    toponym_coodrinates = toponym["Point"]["pos"]
                    sp = toponym_coodrinates.split(' ')
                    sp.reverse()
                    self.current_coord = sp.copy()
                    if not self.camera:
                        print(self.camera)
                        self.camera = list(map(float, sp))
                else:
                    print('Неверный запрос')
            if self.themeButtonGroup.checkedButton().text() == 'Темная':
                self.theme = 'dark'
            else:
                self.theme = 'light'
            part1 = f'https://static-maps.yandex.ru/v1?lang=ru_RU&ll={str(self.camera[1])},{str(self.camera[0])}&'
            part2 =  f'spn={str(self.spn)},{str(self.spn)}&theme={self.theme}&pt={str(self.current_coord[1])},{str(self.current_coord[0])}'
            part3 = '&apikey=927d9050-0770-4c07-ad38-1a40debfdd3e'
            map_request = part1 + part2 + part3
            response = requests.get(map_request)
            if not response:
                print("Ошибка выполнения запроса:")
                print("Http статус:", response.status_code, "(", response.reason, ")")
                sys.exit(1)
            map_file = "map.png"
            with open(map_file, "wb") as file:
                file.write(response.content)
            self.pixmap = QPixmap(map_file)
            self.label.setPixmap(self.pixmap.scaled((self.label.size())))
    
    def clear(self):
        self.lineEdit.clear()
        self.label.clear()
        self.spn = 0.002
        self.camera = []
        self.current_coord = []
    
    def find(self):
        self.spn = 0.002
        self.camera = []
        self.current_coord = []
        self.show_map()
        self.setFocus()
    
    def keyPressEvent(self, event):
        if event.key() in [Qt.Key.Key_PageUp, Qt.Key.Key_PageDown]:
            if event.key() == Qt.Key.Key_PageUp:
                self.spn /= 2
            elif event.key() == Qt.Key.Key_PageDown:
                self.spn = min(64, self.spn * 2)
            self.show_map()
        if event.key() in [Qt.Key.Key_Up,  Qt.Key.Key_Down, Qt.Key.Key_Left,  Qt.Key.Key_Right]:
            if self.camera:
                k = 0.1
                match event.key():
                    case Qt.Key.Key_Up:
                        self.camera[0] = min(85, self.camera[0] + k * self.spn)
                    case Qt.Key.Key_Down:
                        self.camera[0] = max(-85, self.camera[0] - k * self.spn)
                    case Qt.Key.Key_Left:
                        self.camera[1] -= 2 * k * self.spn
                        if self.camera[1] <= -180:
                            self.camera[1] = 360 + self.camera[1]
                    case Qt.Key.Key_Right:
                        self.camera[1] += 2 * k * self.spn
                        if self.camera[1] >= 180:
                            self.camera[1] = -180 + (self.camera[1] - 180)
                self.show_map()

    def resizeEvent(self, event):
        self.label.setPixmap(self.label.pixmap().scaled((self.label.size())))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())