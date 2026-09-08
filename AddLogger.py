# Скрипт для добавления функций логирования в файл конфигурации Ар12.
# Нужно открыть файл конфигурации, внести в него блок с логгером по-умолчанию, сохранить файл конфигурации

import json
import logging
import sys
from json import JSONDecodeError

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox

from ui_mainwindow3_1 import Ui_MainWindow

logging.basicConfig(filename="./AddLogger.log", level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', encoding="utf-8")

app_logger = logging.getLogger()

DEFAULT_PORT = 505
DEFAULT_EVENTS_QTY = 10
DEFAULT_BUFFER_LENGTH = 10
DEFAULT_START_REGISTER = 40050
CURRENT_VERSION_FOR_WINDOW_TITLE = 0.1


class NoPlcNameException(Exception):
    pass


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setAcceptDrops(True)
        window_title = self.windowTitle()
        self.setWindowTitle(window_title + ' ' + str(CURRENT_VERSION_FOR_WINDOW_TITLE))
        # edit text default values
        self.ui.linePortValue.setText(str(DEFAULT_PORT))
        self.ui.lineMessageQty.setText(str(DEFAULT_EVENTS_QTY))
        self.ui.lineBufferLength.setText(str(DEFAULT_BUFFER_LENGTH))
        self.ui.lineStartRegister.setText(str(DEFAULT_START_REGISTER))
        # fields
        self.port_value = DEFAULT_PORT
        self.msg_qty = DEFAULT_START_REGISTER
        self.buffer_length = DEFAULT_BUFFER_LENGTH
        self.start_register_field = DEFAULT_START_REGISTER

    # ===================
    #   port value
    #   getter, setter
    # ===================
    @property
    def port_value(self):
        return self._port_value

    @port_value.setter
    def port_value(self, value):
        if 0 <= value <= 65535:
            self._port_value = value

    # ===================
    #   buffer length
    #   getter, setter
    # ===================
    @property
    def buffer_length(self):
        return self._buffer_length

    @buffer_length.setter
    def buffer_length(self, value):
        if value > 0:
            self._buffer_length = value

    @property
    def msg_qty(self):
        return self._msg_qty

    @msg_qty.setter
    def msg_qty(self, value):
        self._msg_qty = value

    @property
    def start_register_field(self):
        return self._start_register_field

    @start_register_field.setter
    def start_register_field(self, value):
        self._start_register_field = value

    # ===================
    #   проверка пути файла
    # ===================
    def dragEnterEvent(self, event):
        """
        Функция вызывается при "заносе" внутрь границ окна объекта
        :param event:
        :return:
        """
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

    #   выполнение логики при "сбросе"
    def dropEvent(self, event):
        """
        Функция вызывается при "сбросе" объекта внутри границ окна
        :param event:
        :return:
        """
        json_data: dict
        urls = event.mimeData().urls()  # Получаем список URL перетаскиваемых объектов

        if (  # проверки URL объекта
                len(urls) == 1
                and urls[0].isLocalFile()
                and urls[0].toLocalFile().lower().endswith(".json")
        ):
            dropped_file_path = urls[0].toLocalFile()

            with open(dropped_file_path, 'r',
                      encoding='utf-8-sig') as opened_file:  # Открытие файла, utf-8-sig -- игнорирует наличие BOM в JSON-файле
                try:
                    json_data = json.load(opened_file)
                except JSONDecodeError:
                    app_logger.error("Ошибка при чтении/парсинге JSON")
                    self.ui.lblStatusText.setText(f"Ошибка при чтении/парсинге JSON")
                except UnicodeDecodeError:
                    app_logger.error("Ошибка по Unicode")
                    self.ui.lblStatusText.setText(f"Ошибка по Unicode")

            try:
                plc_name = get_plc_name(json_data)
                # todo: сделать проверку доступности 505-го порта, создать 505-й порт в конфигурации
            except NoPlcNameException:
                plc_name = ""
                self.ui.lblStatusText.setText("В файле конфигурации не обозначено имя ПЛК")
                app_logger.info("В файле конфигурации не обозначено имя ПЛК")

            if plc_name != "":
                # self.message_quantity = int(self.ui.lineMessageQty.text())
                self.msg_qty = int(self.ui.lineMessageQty.text())
                # self.message_quantity(self, int(self.ui.lineMessageQty.text()))

                self.start_register_field = int(self.ui.lineStartRegister.text())
                app_logger.info("Событие дроп, новых сообщений: %d " % self.msg_qty)
                app_logger.info("Событие дроп, стартовый регистр: %d " % self.start_register_field)

                new_config_dict = filling_new_config(
                    json_data, plc_name,
                    self.start_register_field,
                    self._msg_qty)

                # options = QFileDialog.options()
                # options |= QFileDialog.Option.DontUseNativeDialog  # необязательно, для единообразия
                # # Убедимся, что флаг DontConfirmOverwrite выключен:
                # options &= ~QFileDialog.Option.DontConfirmOverwrite

                target_path, _ = QFileDialog.getSaveFileName(
                    self,
                    "Сохранить файл как...",
                    dropped_file_path,  # начальная директория (можно указать)
                    "Все файлы (*.*)",  # фильтр
                    # options=options
                )

                if target_path:
                    try:
                        with open(target_path, 'w', encoding='utf-8-sig') as wrote_file:
                            json.dump(new_config_dict, wrote_file, indent=2, ensure_ascii=False)
                            self.ui.lblStatusText.setText("Конфиг обновлён")
                            # QMessageBox.information(self, "Заголовок", "Конфиг обновлён")
                        QMessageBox.information(self, "Готово", f"Результат сохранён в:\n{target_path}")
                    except Exception as e:
                        QMessageBox.critical(self, "Ошибка записи", f"Не удалось сохранить:\n{str(e)}")
        else:
            QMessageBox.information(self, "Предупреждение", f"Неподходящий тип файла!")
            self.ui.lblStatusText.setText("Неподходящий тип файла")

        event.acceptProposedAction()


def get_plc_name(config_dict: dict) -> str:
    """
    Получение имени контроллера из файла конфигурации.
    :param config_dict: Словарь JSON-конфигурации
    :return: имя контроллера
    """
    plc_name = "no data"
    if len(config_dict['ModulesIO'][0]['Name']) != 0:
        plc_name = config_dict['ModulesIO'][0]['Name']
        print(json.dumps(config_dict['ModulesIO'][0], indent=4, sort_keys=True, ensure_ascii=False))
    else:
        raise NoPlcNameException(plc_name)
    return plc_name


def filling_new_config(config_dict: dict, plc_name: str, start_register: int, messages_qty: int) -> dict:
    """
    Заполнение словаря JSON-конфигурации согласно передаваемым параметрам.
    :param messages_qty: Количество добавляемых сообщений в Логгер
    :param start_register: начальный Modbus-регистр
    :param config_dict: старый словарь конфигурации
    :param plc_name: имя контроллера
    :return: новый словарь конфигурации
    """
    app_logger.info("Заполнение обновлённого конфига, новых сообщений: %d " % messages_qty)
    app_logger.info("Заполнение обновлённого конфига, стартовый регистр: %d " % start_register)

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
    app.setStyle('Fusion')  # установка стиля Fusion для корректной обработки светлой / тёмной тем оформления
    # app_logger.info(f"Текущий стиль приложения - {app.style().name()}")
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
