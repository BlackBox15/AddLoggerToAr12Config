# Скрипт для добавления функций логирования в файл конфигурации Ар12.
# Нужно открыть файл конфигурации, внести в него блок с логгером по-умолчанию, сохранить файл конфигурации

import json
import logging
import sys
from json import JSONDecodeError

from PySide6.QtWidgets import QApplication, QMainWindow, QStyleFactory

from ui_mainwindow3 import Ui_MainWindow

logging.basicConfig(filename="./AddLogger.log", level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', encoding="utf-8")

app_logger = logging.getLogger()


class NoPlcNameException(Exception):
    pass


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setAcceptDrops(True)
        self.ui.lineStartRegiter.setText("40050")
        self.ui.lineMessageQty.setText("3")
        self._messages_quantity = int(self.ui.lineMessageQty.text())
        self._start_register_field = int(self.ui.lineStartRegiter.text())

    @property
    def message_quantity(self):
        return self._messages_quantity

    @message_quantity.setter
    def message_quantity(self, value):
        self._start_register_field = value

    @property
    def start_register_field(self):
        return self._messages_quantity

    @start_register_field.setter
    def start_register_field(self, value):
        self._start_register_field = value

    def dragEnterEvent(self, event):
        mimetype = event.mimeData().hasText()
        mimeData = event.mimeData()

        if mimeData.hasUrls():
            urls = mimeData.urls()
            for url in urls:
                if url.isLocalFile() and url.toLocalFile().lower().endswith(".json"):
                    event.acceptProposedAction()
                    return

        event.ignore()

        if mimetype:
            event.acceptProposedAction()

    def dropEvent(self, event):

        # Получаем список URL перетаскиваемых объектов
        urls = event.mimeData().urls()
        # проверки URL объекта
        if len(urls) == 1 and urls[0].isLocalFile() and urls[0].toLocalFile().lower().endswith(".json"):
            file_path = urls[0].toLocalFile()

            # Открытие файла
            with open(file_path, 'r', encoding='utf-8-sig') as opened_file:
                try:
                    data = json.load(opened_file)
                    try:
                        plc_name = get_plc_name(data)
                    except NoPlcNameException:
                        plc_name = ""
                        self.ui.lblStatusText.setText("В файле конфигурации не обозначено имя ПЛК")
                        app_logger.info("В файле конфигурации не обозначено имя ПЛК")

                    if plc_name != "":
                        self.message_quantity = int(self.ui.lineMessageQty.text())
                        self.start_register_field = int(self.ui.lineStartRegiter.text())
                        new_config_dict = filling_new_config(data, plc_name, self.start_register_field,
                                                             self.message_quantity)

                        # Запись файла
                        with open(file_path, 'w', encoding='utf-8-sig') as wrote_file:
                            json.dump(new_config_dict, wrote_file, indent=2, ensure_ascii=False)
                            self.ui.lblStatusText.setText("Конфиг обновлён")
                            # QMessageBox.information(self, "Заголовок", "Конфиг обновлён")
                except JSONDecodeError:
                    app_logger.error("Ошибка при чтении/парсинге JSON")
                    self.ui.lblStatusText.setText(f"Ошибка при чтении/парсинге JSON")
                except UnicodeDecodeError:
                    app_logger.error("Ошибка по Unicode")
                    self.ui.lblStatusText.setText(f"Ошибка по Unicode")
        else:
            self.ui.lblStatusText.setText("Неподходящий тип файла")

        event.acceptProposedAction()


def get_plc_name(config_dict: dict) -> str:
    """
    Получение имени контроллера из файла конфигурации.
    :param config_dict: словарь JSON-конфигурации
    :return: имя контроллера
    """
    plc_name = "no data"
    if len(config_dict['ModulesIO'][0]['Name']) != 0:
        plc_name = config_dict['ModulesIO'][0]['Name']
    else:
        raise NoPlcNameException(plc_name)
    return plc_name


def filling_new_config(config_dict: dict, plc_name: str, start_register: int, messages_qty: int) -> dict:
    """
    Заполнение словаря JSON-конфигурации согласно передаваемым параметрам.
    :param messages_qty: количество добавляемых сообщений в Логгер
    :param start_register: начальный Modbus-регистр
    :param config_dict: старый словарь конфигурации
    :param plc_name: имя контроллера
    :return: новый словарь конфигурации
    """

    logger_events_list = list()
    logger_messages_list = list()

    for i in range(messages_qty):
        logger_one_event_dict = {
            "TimeRelayNumber": start_register + (i * 4) + 2,
            "EventRelayNumber": (start_register - 30_000) + (i * 4) + 4,
            "ArgRelayNuber": (start_register - 30_000) + (i * 4) + 5
        }
        logger_one_message_dict = {
            "Name": "message" + str(i + 1),
            "IsEnabled": True,
            "EventIndex": (i + 1),
            "LoggerName": "Logger1",
            "MessageFormat": "test for message" + str(i + 1) + " with argument = {0}"
        }
        logger_events_list.append(logger_one_event_dict)
        logger_messages_list.append(logger_one_message_dict)

    if len(config_dict['ExternalLoggers']) == 0:
        config_dict['ExternalLoggers'] = [
            {
                "Name": "Logger1",
                "IsInitialized": False,
                "IsUsing": False,
                "ModuleIOName": plc_name,
                "FutureEntryRelayNumber": start_register,
                "ExternalLoggerLines": []
            }
        ]
        config_dict['ExternalLoggers'][0]['ExternalLogger Lines'] = logger_events_list
        app_logger.info("New ExternalLoggers added.")
    else:
        app_logger.info("поле ExternalLoggers не пустое")

    if len(config_dict['ExternalLoggingMessages']) == 0:
        config_dict['ExternalLoggingMessages'] = logger_messages_list
        app_logger.info("New ExternalLoggingMessages added.")
    else:
        app_logger.info("поле ExternalLoggingMessages не пустое")

    return config_dict


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # print(QStyleFactory.keys())     # перечень возможных стилей: ['windows11', 'windowsvista', 'Windows', 'Fusion']
    app.setStyle('Fusion')          # установка стиля Fusion для корректной обработки светлой / тёмной тем оформления
    # app_logger.info(f"Текущий стиль приложения - {app.style().name()}")
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
