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

logger = logging.getLogger()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setAcceptDrops(True)
        self.ui.lineStartRegiter.setText("40050")
        self.ui.lineMessageQty.setText("3")
        self.msgQty = int(self.ui.lineMessageQty.text())
        self.startRegister = int(self.ui.lineStartRegiter.text())
        self.ui.lineMessageQty.returnPressed.connect(self.msg_qty_value)
        self.ui.lineStartRegiter.returnPressed.connect(self.start_register_value)

    def msg_qty_value(self):
        # self.ui.lblStatusText.setText(event.mimeData().text())
        self.msgQty = int(self.ui.lineMessageQty.text())

    def start_register_value(self):
        self.startRegister = int(self.ui.lineStartRegiter.text())

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
            # if event.mimeData().hasFormat("text/plain"):
            event.acceptProposedAction()

    def dropEvent(self, event):
        # self.ui.lblStatusText.setText(event.mimeData().text())

        # Получаем список URL перетаскиваемых объектов
        urls = event.mimeData().urls()
        # проверки URL объекта
        if len(urls) == 1 and urls[0].isLocalFile() and urls[0].toLocalFile().lower().endswith(".json"):
            file_path = urls[0].toLocalFile()
            with open(file_path, 'r', encoding='utf-8-sig') as opened_file:
                try:
                    data = json.load(opened_file)
                except JSONDecodeError as e:
                    self.ui.lblStatusText.setText(f"Ошибка при чтении/парсинге JSON")
                except UnicodeDecodeError as e:
                    self.ui.lblStatusText.setText(f"Ошибка по Unicode")
            plc_name = get_plc_name(data)

            self.ui.lblStatusText.setText(plc_name)
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
    if len(config_dict['ModulesIO']) != 0:
        plc_name = config_dict['ModulesIO'][0]['Name']

    return plc_name


def write_new_config(config_dict: dict, plc_name: str) -> dict:
    """
    :param config_dict: старый словарь конфигурации
    :param plc_name: имя контроллера
    :return: новый словарь конфигурации
    """
    if len(config_dict['ExternalLoggers']) == 0:
        config_dict['ExternalLoggers'] = [
            {
                "Name": "test_logger",
                "IsInitialized": True,
                "IsUsing": True,
                "ModuleIOName": plc_name,
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
        logging.info("New ExternalLoggers added.")
    else:
        logging.info("ExternalLoggers are not empty!")

    # Проверка и заполнение ExternalLoggingMessages
    if len(config_dict['ExternalLoggingMessages']) == 0:
        config_dict['ExternalLoggingMessages'] = [
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
        logging.info("New ExternalLoggingMessages added.")
    else:
        logging.info("ExternalLoggingMessages are not empty!")
    pass

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
            logging.info("Can't load JSON-file..")
            showerror("Error", "Can't load JSON-file!")
            sys.exit(1)
        logging.info(f"file {opened_file.name} is parsed")

    # Получение имени контроллера, сконфигурированном в файле конфигурации
    if config_json_file['ModulesIO'][0]['Name']:
        plc_name_from_config = config_json_file['ModulesIO'][0]['Name']
        logging.info(f"plc_name_from_config: {plc_name_from_config}")

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
            logging.info("New ExternalLoggers added.")
        else:
            logging.info("ExternalLoggers are not empty!")

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
            logging.info("New ExternalLoggingMessages added.")
        else:
            logging.info("ExternalLoggingMessages are not empty!")

        # Запись обновлённого файла (с сохранением форматирования)
        new_filename = file_path + "_edit"
        with open(new_filename, '+w', encoding='utf-8') as opened_file:
            json.dump(config_json_file, opened_file, ensure_ascii=False, indent=2)
            logging.info("New config file saved")
            showinfo("ExternalLoggers", "New config file saved!")
    else:
        logging.info("Modules IO // Name is empty")
        sys.exit(1)


def main():
    # Конфигурирование логгера
    logging.basicConfig(filename="general.log", level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')

    args = parser.parse_args()

    # Проверка открываемого файла
    if str(args.input_file) == 'None':
        print("Input file is empty!")
        logger.info("Input file is empty!")
        sys.exit(1)

    if not os.path.exists(args.input_file):
        print(f"Error: File '{args.input_file}' does not exist.")
        sys.exit(1)

    if not os.path.isfile(args.input_file):
        print(f"Error: '{args.input_file}' is not a file.")
        sys.exit(1)

    logger.info(f"Input file: {args.input_file}")
    fill_new_config(args.input_file)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
    # main()
