import sys
import requests
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from ui_file import Ui_MainWindow
import re


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.spn = 0.002
        self.camera = [0.0, 0.0]
        self.current_coord = [0.0, 0.0]

    def show_map(self):
        address = self.lineEdit.text()

        if len(address) != 0:
            sp = re.findall(r"\d*\.\d*", address)
            if len(sp) != 2:
                api_key = "8013b162-6b42-4997-9691-77b7074026e0"
                server_address = 'http://geocode-maps.yandex.ru/1.x/?'
                geocoder_request = f'{server_address}apikey={api_key}&geocode={address}&format=json'
                print(geocoder_request)
                response = requests.get(geocoder_request)
                if response:
                    json_response = response.json()
                    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                    toponym_coodrinates = toponym["Point"]["pos"]
                    sp = toponym_coodrinates.split(' ')
                    sp.reverse()
                    self.current_coord = sp.copy()
                    if self.camera[0] == 0 and self.camera[1] == 0:
                        self.camera = list(map(float, sp))
                else:
                    print('Неверный запрос')
        server_address = 'http://static-maps.yandex.ru/1.x/?'
        ll_spn = f'll={str(self.camera[1])},{str(self.camera[0])}&spn={str(self.spn)},{str(self.spn)}'
        map_request = f"{server_address}{ll_spn}&pt={str(self.current_coord[1])},{str(self.current_coord[0])}&l=map"
        response = requests.get(map_request)
        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap(map_file)
        self.label.setPixmap(self.pixmap)
    
    def clear(self):
        self.lineEdit.clear()
        self.label.clear()
        self.spn = 0.002
        self.camera = [0.0, 0.0]
        self.current_coord = [0.0, 0.0]
    
    def find(self):
        self.spn = 0.002
        self.show_map()
        self.setFocus()
    
    def keyPressEvent(self, event):
        if event.key() in [Qt.Key.Key_PageUp, Qt.Key.Key_PageDown, Qt.Key.Key_Up,  Qt.Key.Key_Down, Qt.Key.Key_Left,  Qt.Key.Key_Right]:
            k = 0.1
            if event.key() == Qt.Key.Key_PageUp:
                self.spn /= 2
            elif event.key() == Qt.Key.Key_PageDown:
                self.spn = min(64, self.spn * 2)
            elif event.key() == Qt.Key.Key_Up:
                self.camera[0] += k * self.spn
            elif event.key() == Qt.Key.Key_Down:
                self.camera[0] -= k * self.spn
            elif event.key() == Qt.Key.Key_Left:
                self.camera[1] -= k * self.spn
            elif event.key() == Qt.Key.Key_Right:
                self.camera[1] += k * self.spn
            self.show_map()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())