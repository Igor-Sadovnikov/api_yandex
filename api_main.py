import sys
import requests
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QPixmap
from ui_file import Ui_MainWindow


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
    def show_map(self):
        coords = self.lineEdit.text()
        server_address = 'https://static-maps.yandex.ru/v1?'
        api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        ll_spn = f'll={coords}&spn=0.002,0.002'
        map_request = f"{server_address}{ll_spn}&apikey={api_key}"
        # map_request = f'http://static-maps.yandex.ru/1.x/?ll={coords}&spn=0.3,0.3&l=map'
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())