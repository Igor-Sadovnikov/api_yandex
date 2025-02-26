import sys
import requests
from PyQt6.QtWidgets import QApplication, QMainWindow, QStyleFactory
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QPalette, QColor
from ui_08_02 import Ui_MainWindow
import re


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # загружаем интерфейс

        self.spn = 32  # масштаб

        self.camera = [0.0, 0.0]  # координаты камеры
        self.current_coord = []  # координаты метки

        self.theme = 'dark'  # тема

        self.lightTheme = QPalette(QColor("#cfcfcf"))  # светлая тема
        self.darkTheme = QPalette(QColor("#424242"))  # темная тема
        self.setPalette(self.darkTheme)

        self.findButton.clicked.connect(self.find)
        self.clearButton.clicked.connect(self.clear)
        self.themeButtonGroup.buttonClicked.connect(self.changeTheme)  # выбор темы
        self.lineEdit.returnPressed.connect(self.find)  # поиск

        QTimer.singleShot(100, self.show_map)

    def show_map(self):
        # получаем данные введенные пользователем
        address = self.lineEdit.text()

        # проверяем что пользователь что-то ввел
        if len(address) != 0:
            # ищем координаты по паттерну
            sp = re.findall(r"\d*\.\d*", address)

            # если это новый запрос
            if not self.current_coord:
                # если пользователь ввел координаты
                if len(sp) == 2:
                    self.current_coord = sp.copy()  # координатам текущей метки присваиваем полученные координаты
                    self.camera = list(map(float, sp))  # координатам камеры присваиваем полученные координаты

                    # адрес запроса
                    part1 = f'https://static-maps.yandex.ru/v1?lang=ru_RU&ll={str(self.camera[1])},{str(self.camera[0])}&'
                    part2 = f'spn={str(self.spn)},{str(self.spn)}&theme={self.theme}&pt={str(self.current_coord[1])},{str(self.current_coord[0])}'
                    part3 = '&apikey=927d9050-0770-4c07-ad38-1a40debfdd3e'
                    map_request = part1 + part2 + part3

                    # делаем запрос
                    response = requests.get(map_request)
                    if not response:
                        print("Ошибка выполнения запроса:")
                        print("Http статус:", response.status_code, "(", response.reason, ")")

                    # сохраняем изображение из запроса в файле
                    map_file = "map.png"
                    with open(map_file, "wb") as file:
                        file.write(response.content)
                    # отображаем изображение на экране
                    self.pixmap = QPixmap(map_file)
                    self.label.setPixmap(self.pixmap.scaled((self.label.size())))
                    api_key = "8013b162-6b42-4997-9691-77b7074026e0"
                    server_address = 'http://geocode-maps.yandex.ru/1.x/?'
                    geocoder_request = f'{server_address}apikey={api_key}&geocode={str(self.camera[1])},{str(self.camera[0])}&format=json'
                    # делаем запрос
                    response = requests.get(geocoder_request)
                    # если удачно
                    if response:
                        # парсим запрос
                        json_response = response.json()

                        # получаем нужные нам данные
                        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0][
                            "GeoObject"]  # гео.объект
                        toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
                        toponym_coodrinates = toponym["Point"]["pos"]  # координаты гео.объекта
                        self.show_adress.setText(toponym_address)
                else:
                    # адрес запроса
                    api_key = "8013b162-6b42-4997-9691-77b7074026e0"
                    server_address = 'http://geocode-maps.yandex.ru/1.x/?'
                    geocoder_request = f'{server_address}apikey={api_key}&geocode={address}&format=json'

                    # делаем запрос
                    response = requests.get(geocoder_request)
                    # если удачно
                    if response:
                        # парсим запрос
                        json_response = response.json()

                        # получаем нужные нам данные
                        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0][
                            "GeoObject"]  # гео.объект
                        toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
                        toponym_coodrinates = toponym["Point"]["pos"]  # координаты гео.объекта
                        self.show_adress.setText(toponym_address)
                        sp = toponym_coodrinates.split(' ')  # разделяем полученные координаты на два значения
                        sp.reverse()  # меняем местами longitude и latitude

                        # если это новый запрос
                        if not self.current_coord:
                            self.current_coord = sp.copy()  # координатам текущей метки присваиваем полученные координаты
                            self.camera = list(map(float, sp))  # координатам камеры присваиваем полученные координаты

                        # адрес запроса
                        part1 = f'https://static-maps.yandex.ru/v1?lang=ru_RU&ll={str(self.camera[1])},{str(self.camera[0])}&'
                        part2 = f'spn={str(self.spn)},{str(self.spn)}&theme={self.theme}&pt={str(self.current_coord[1])},{str(self.current_coord[0])}'
                        part3 = '&apikey=927d9050-0770-4c07-ad38-1a40debfdd3e'
                        map_request = part1 + part2 + part3

                        # делаем запрос
                        response = requests.get(map_request)
                        if not response:
                            print("Ошибка выполнения запроса:")
                            print("Http статус:", response.status_code, "(", response.reason, ")")

                        # сохраняем изображение из запроса в файле
                        map_file = "map.png"
                        with open(map_file, "wb") as file:
                            file.write(response.content)
                        # отображаем изображение на экране
                        self.pixmap = QPixmap(map_file)
                        self.label.setPixmap(self.pixmap.scaled((self.label.size())))
                    else:
                        print('Неверный запрос')
            else:
                # адрес запроса
                part1 = f'https://static-maps.yandex.ru/v1?lang=ru_RU&ll={str(self.camera[1])},{str(self.camera[0])}&'
                part2 = f'spn={str(self.spn)},{str(self.spn)}&theme={self.theme}&pt={str(self.current_coord[1])},{str(self.current_coord[0])}'
                part3 = '&apikey=927d9050-0770-4c07-ad38-1a40debfdd3e'
                map_request = part1 + part2 + part3

                # делаем запрос
                response = requests.get(map_request)
                if not response:
                    print("Ошибка выполнения запроса:")
                    print("Http статус:", response.status_code, "(", response.reason, ")")

                # сохраняем изображение из запроса в файле
                map_file = "map.png"
                with open(map_file, "wb") as file:
                    file.write(response.content)
                # отображаем изображение на экране
                self.pixmap = QPixmap(map_file)
                self.label.setPixmap(self.pixmap.scaled((self.label.size())))
        else:
            # адрес запроса
            part1 = f'https://static-maps.yandex.ru/v1?lang=ru_RU&ll={str(self.camera[1])},{str(self.camera[0])}&'
            part2 = f'spn={str(self.spn)},{str(self.spn)}&theme={self.theme}'
            part3 = '&apikey=927d9050-0770-4c07-ad38-1a40debfdd3e'
            map_request = part1 + part2 + part3

            # делаем запрос
            response = requests.get(map_request)
            if not response:
                print("Ошибка выполнения запроса:")
                print("Http статус:", response.status_code, "(", response.reason, ")")

            # сохраняем изображение из запроса в файле
            map_file = "map.png"
            with open(map_file, "wb") as file:
                file.write(response.content)
            # отображаем изображение на экране
            self.pixmap = QPixmap(map_file)
            self.label.setPixmap(self.pixmap.scaled((self.label.size())))

    def changeTheme(self):
        if self.themeButtonGroup.checkedButton().text() == 'Темная':
            if self.theme != 'dark':  # если произошла смена темы
                self.theme = 'dark'
                self.setPalette(self.darkTheme)
                self.show_map()
        else:
            if self.theme != 'light':  # если произошла смена темы
                self.theme = 'light'
                self.setPalette(self.lightTheme)
                self.show_map()

    def clear(self):
        self.lineEdit.clear()
        self.show_adress.clear()
        self.setFocus()

        self.current_coord = []

        self.show_map()

    def find(self):
        self.spn = 0.002

        self.current_coord = []

        self.show_map()
        self.setFocus()

    def keyPressEvent(self, event):
        # изменение масштаба
        if event.key() in [Qt.Key.Key_PageUp, Qt.Key.Key_PageDown]:
            if event.key() == Qt.Key.Key_PageUp:
                self.spn /= 2
            elif event.key() == Qt.Key.Key_PageDown:
                self.spn = min(64, self.spn * 2)
            self.show_map()
        # перемещение камеры
        elif event.key() in [Qt.Key.Key_Up, Qt.Key.Key_Down, Qt.Key.Key_Left, Qt.Key.Key_Right]:
            k = 0.1  # коэффициент перемещения
            match event.key():
                case Qt.Key.Key_Up:  # вверх
                    self.camera[0] = min(85, self.camera[0] + k * self.spn)
                case Qt.Key.Key_Down:  # вниз
                    self.camera[0] = max(-85, self.camera[0] - k * self.spn)
                case Qt.Key.Key_Left:  # влево
                    self.camera[1] -= 2 * k * self.spn
                    # обработка выхода за пределы карты
                    if self.camera[1] <= -180:
                        self.camera[1] = 360 + self.camera[1]  # перемещаем камеру на точку с другой стороны
                case Qt.Key.Key_Right:  # вправо
                    self.camera[1] += 2 * k * self.spn
                    # обработка выхода за пределы карты
                    if self.camera[1] >= 180:
                        self.camera[1] = -180 + (self.camera[1] - 180)  # перемещаем камеру на точку с другой стороны
            self.show_map()

    def resizeEvent(self, event):
        self.label.setPixmap(self.label.pixmap().scaled((self.label.size())))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    styles = QStyleFactory.keys()
    # if "windows11" in styles:
    #     app.setStyle('windows11')
    if "Fusion" in styles:
        app.setStyle('Fusion')
    # elif "Windows" in styles:
    #     app.setStyle('Windows')
    # elif "windowsvista" in styles:
    #     app.setStyle('windowsvista')
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())