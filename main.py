# Скрипт для добавления функций логирования в файл конфигурации Ар12.
# Нужно открыть файл конфигурации, внести в него блок с логгером по-умолчанию, сохранить файл конфигурации

import argparse
import json
import logging
import os
import sys
from json import JSONDecodeError
from tkinter import Tk
from tkinter.messagebox import showinfo, showerror

from PySide6.QtWidgets import QApplication, QMainWindow

from ui_mainwindow3 import Ui_MainWindow

logging.basicConfig(filename="./log/AddLogger.log", level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

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
                        # self.set_start_register()
                        # self.set_message_qty()
                        self.message_quantity = int(self.ui.lineMessageQty.text())
                        self.start_register_field = int(self.ui.lineStartRegiter.text())
                        new_config_dict = filling_new_config(data, plc_name, self.start_register_field, self.message_quantity)

                        # Запись файла
                        with open(file_path, 'w', encoding='utf-8-sig') as opened_file:
                            json.dump(new_config_dict, opened_file, indent=2, ensure_ascii=False)
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
    Получение имени контроллера из файла конфигурации
    :param config_dict:
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
    :param messages_qty:
    :param start_register:
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


def fill_new_config(file_path):
    """
    Заполняет секции ExternalLoggers и ExternalLoggingMessages в JSON-файле настроек.
    """

    root = Tk()
    root.withdraw()

    # Чтение текущего содержимого
    with open(file_path, 'r', encoding='utf-8-sig') as opened_file:
        try:
            config_json_file = json.load(opened_file)
        except ValueError:
            app_logger.info("Can't load JSON-file..")
            showerror("Error", "Can't load JSON-file!")
            sys.exit(1)
        app_logger.info(f"file {opened_file.name} is parsed")

    # Получение имени контроллера, сконфигурированном в файле конфигурации
    if config_json_file['ModulesIO'][0]['Name']:
        plc_name_from_config = config_json_file['ModulesIO'][0]['Name']
        app_logger.info(f"plc_name_from_config: {plc_name_from_config}")

        # Проверка и заполнение ExternalLoggers
        if len(config_json_file['ExternalLoggers']) == 0:
            config_json_file['ExternalLoggers'] = [
                {
                    "Name": "test_logger",
                    "IsInitialized": True,
                    "IsUsing": True,
                    "ModuleIOName": plc_name_from_config,
                    "FutureEntryRelayNumber": 40050,
                    # адрес регистра LogIndex, его формат dword, поэтому адресация вида 40ххх
                    "ExternalLoggerLines": [
                        {  # структура данных 1-го события
                            "TimeRelayNumber": 40052,  # адрес регистра времени 1-го события, формат dword
                            "EventRelayNumber": 10054,  # адрес регистра порядкового номера события (id), формат word
                            "ArgRelayNuber": 10055  # адрес регистра аргумента, формат величины - word, не используется
                        },
                        {  # структура данных 1-го события
                            "TimeRelayNumber": 40056,  # адрес регистра времени 1-го события, формат dword
                            "EventRelayNumber": 10058,  # адрес регистра порядкового номера события (id), формат word
                            "ArgRelayNuber": 10059  # адрес регистра аргумента, формат величины - word, не используется
                        }
                    ]
                }
            ]
            app_logger.info("New ExternalLoggers added.")
        else:
            app_logger.info("ExternalLoggers are not empty!")

        # Проверка и заполнение ExternalLoggingMessages
        if len(config_json_file['ExternalLoggingMessages']) == 0:
            config_json_file['ExternalLoggingMessages'] = [
                {
                    "Name": "message1",
                    "IsEnabled": True,
                    "EventIndex": 1,
                    "LoggerName": "test_logger",
                    "MessageFormat": "test for message1 with argument = {0}"
                },
                {
                    "Name": "message2",
                    "IsEnabled": True,
                    "EventIndex": 2,
                    "LoggerName": "test_logger",
                    "MessageFormat": "test for message2 with argument = {0}"
                }
            ]
            app_logger.info("New ExternalLoggingMessages added.")
        else:
            app_logger.info("ExternalLoggingMessages are not empty!")

        # Запись обновлённого файла (с сохранением форматирования)
        new_filename = file_path + "_edit"
        with open(new_filename, '+w', encoding='utf-8') as opened_file:
            json.dump(config_json_file, opened_file, ensure_ascii=False, indent=2)
            logging.info("New config file saved")
            showinfo("ExternalLoggers", "New config file saved!")
    else:
        app_logger.info("Modules IO // Name is empty")
        sys.exit(1)


def main():
    # Конфигурирование логгера

    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')

    args = parser.parse_args()

    # Проверка открываемого файла
    if str(args.input_file) == 'None':
        print("Input file is empty!")
        app_logger.info("Input file is empty!")
        sys.exit(1)

    if not os.path.exists(args.input_file):
        print(f"Error: File '{args.input_file}' does not exist.")
        sys.exit(1)

    if not os.path.isfile(args.input_file):
        print(f"Error: '{args.input_file}' is not a file.")
        sys.exit(1)

    app_logger.info(f"Input file: {args.input_file}")
    fill_new_config(args.input_file)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
    # main()
