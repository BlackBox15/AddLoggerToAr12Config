# Скрипт для добавления функций логирования в файл конфигурации Ар12.
# Нужно открыть файл конфигурации, внести в него блок с логгером по-умолчанию, сохранить файл конфигурации

import json
import logging
import sys
from ipaddress import ip_address, IPv4Address
from json import JSONDecodeError

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox

from ui_mainwindow3_1 import Ui_MainWindow

logging.basicConfig(filename="./AddLogger.log", level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', encoding="utf-8")

app_logger = logging.getLogger()

DEFAULT_IP_ADDRESS = '192.168.0.10'
DEFAULT_PORT = 505
DEFAULT_START_REGISTER = 40000
DEFAULT_EVENTS_QTY = 10
DEFAULT_BUFFER_LENGTH = 10
CURRENT_VERSION_FOR_WINDOW_TITLE = 0.4


class NoPlcNameException(Exception):
    pass

# todo: переименовать переменные, чтобы не было разночтений:
#  на Арке существуют понятия Lines и Messages,
#  где Lines -- это записи из очереди сообщений на ПЛК,
#  а Messages - это текстовые описания регистрируемых событий,
#  таким образом имеется количественное условие: размер очереди сообщений >= количеству описаний
class MainWindow(QMainWindow):
    _user_input_errors = {'ip_address_incorrect': '', 'port_incorrect': '', 'start_register_incorrect': '',
                          'message_qty_incorrect': '', 'buffer_length_incorrect': ''}
    _default_status_text = "-> Перетащите сюда configuration.json"

    def __init__(self):

        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setAcceptDrops(True)
        window_title = self.windowTitle()
        self.setWindowTitle(window_title + ' ' + str(CURRENT_VERSION_FOR_WINDOW_TITLE))
        # сокрытие инфо-иконок
        # ...названия и так ясно описывают назначения
        self.ui.lblPlcIpInfo.hide()
        self.ui.lblPortInfo.hide()
        self.ui.lblRegisterInfo.hide()
        # текстовые метки
        self.ui.linePlcIpAddress.setText(DEFAULT_IP_ADDRESS)
        self.ui.linePlcIpAddress.editingFinished.connect(self.ip_check)
        self.ui.linePortValue.setText(str(DEFAULT_PORT))
        self.ui.linePortValue.editingFinished.connect(self.port_check)
        # spinBoxes
        self.ui.spinRegister.valueChanged.connect(self.on_register_changed)
        self.ui.spinMessages.valueChanged.connect(self.on_messages_changed)
        self.ui.spinBuffer.valueChanged.connect(self.on_buffer_changed)
        # поля
        self.ip_address = DEFAULT_IP_ADDRESS
        self.port_value = DEFAULT_PORT
        self.msg_qty = DEFAULT_START_REGISTER
        self.buffer_length = DEFAULT_BUFFER_LENGTH
        self.start_register_field = DEFAULT_START_REGISTER

    @property
    def check_err(self):
        return any(self._user_input_errors.values())

    @property
    def all_err(self):
        return self._user_input_errors.values()

    @property
    def plc_err(self):
        return self._user_input_errors['plc_name']

    @plc_err.setter
    def plc_err(self, value: str):
        self._user_input_errors['plc_name'] = value

    @property
    def json_err(self):
        return self._user_input_errors['json']

    @json_err.setter
    def json_err(self, value: str):
        self._user_input_errors['json'] = value

    @property
    def ip_error(self) -> str:
        return self._user_input_errors['ip_address_incorrect']

    @ip_error.setter
    def ip_error(self, value: str):
        self._user_input_errors['ip_address_incorrect'] = value

    @property
    def port_error(self) -> str:
        return self._user_input_errors['port_incorrect']

    @port_error.setter
    def port_error(self, value: str):
        self._user_input_errors['port_incorrect'] = value

    @property
    def register_error(self) -> str:
        return self._user_input_errors['start_register_incorrect']

    @register_error.setter
    def register_error(self, value: str):
        self._user_input_errors['start_register_incorrect'] = value

    @property
    def messages_error(self) -> str:
        return self._user_input_errors['message_qty_incorrect']

    @messages_error.setter
    def messages_error(self, value: str):
        self._user_input_errors['message_qty_incorrect'] = value

    @property
    def buffer_error(self) -> str:
        return self._user_input_errors['buffer_length_incorrect']

    @buffer_error.setter
    def buffer_error(self, value: str):
        self._user_input_errors['buffer_length_incorrect'] = value

    @property
    def get_def_status(self):
        return self._default_status_text

    @property
    def ip_address(self):
        return self._ip_address

    @ip_address.setter
    def ip_address(self, value):
        self._ip_address = value

    @property
    def port_value(self):
        return self._port_value

    @port_value.setter
    def port_value(self, value):
        if 0 <= value <= 65535:
            self._port_value = value

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
        if value > 0:
            self._msg_qty = value
        else:
            self.messages_error = "Отрицательное значение"
            self.status_check()

    @property
    def start_register_field(self):
        return self._start_register_field

    @start_register_field.setter
    def start_register_field(self, value):
        self._start_register_field = value

    def on_register_changed(self, value: int):
        self.start_register_field = value

    def on_messages_changed(self, value: int):
        self.msg_qty = value
        if self.buffer_length < self.msg_qty:
            self.buffer_length = self.msg_qty
            self.ui.spinBuffer.setValue(self.buffer_length)

    def on_buffer_changed(self, value: int):
        self.buffer_length = value
        if self.msg_qty > self.buffer_length:
            self.msg_qty = self.buffer_length
            self.ui.spinMessages.setValue(self.msg_qty)

    def ip_check(self):
        """
        Проверка корректности информации на соответствие формату IP-адреса
        :return:
        """
        new_ip_address = self.ui.linePlcIpAddress.text().strip()

        try:
            ip = ip_address(new_ip_address)
            if not isinstance(ip, IPv4Address):
                raise ValueError
            else:
                self.ip_address = new_ip_address
                self.ip_error = ''
                app_logger.info("IP адрес обновлён: " + new_ip_address)
        except ValueError:
            self.ip_error = "Некорректный IP адрес"
            app_logger.error("Некорректный IP адрес")
        finally:
            self.ui.lblStatusText.setText(self.status_check())

    def port_check(self):
        """
        Проверка значения порта в поле ввода
        :return:
        """
        new_port = self.ui.linePortValue.text().strip()

        if new_port.isdigit() and (0 <= int(new_port) <= 65535):
            self.port_value = int(new_port)
            self.port_error = ''
            app_logger.info("Порт обновлён: " + new_port)
        else:
            self.port_error = "Некорректный порт"
            app_logger.error("Некорректный порт")

        self.ui.lblStatusText.setText(self.status_check())

    def status_check(self) -> str:
        for value in self.all_err:
            if value != '':
                self.setAcceptDrops(False)
                return value
        else:
            self.setAcceptDrops(True)
            return self.get_def_status

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

    def dropEvent(self, event):
        """
        Функция вызывается при "сбросе" объекта внутри границ окна
        :param event:
        :return:
        """
        json_data: dict
        urls = event.mimeData().urls()  # Получаем список URL перетаскиваемых объектов

        if (len(urls) == 1
                and urls[0].isLocalFile()
                and urls[0].toLocalFile().lower().endswith(".json")):

            dropped_file_path = urls[0].toLocalFile()

            # Открытие файла,
            # utf-8-sig -- игнорирует наличие возможной области BOM в JSON-файле
            # (размещение BOM запрещено стандартом RFC)
            with open(dropped_file_path, 'r', encoding='utf-8-sig') as opened_file:
                try:
                    json_data = json.load(opened_file)
                except JSONDecodeError:
                    self.ui.lblStatusText.setText(self.ui.lblStatusText.text() + ' ' + "Ошибка при чтении/парсинге JSON")
                    app_logger.error("Ошибка при чтении/парсинге JSON")
                except UnicodeDecodeError:
                    self.ui.lblStatusText.setText(self.ui.lblStatusText.text() + ' ' + "Ошибка по Unicode")
                    app_logger.error("Ошибка по Unicode")

            try:
                plc_name = get_plc_name(json_data)
                # todo: сделать проверку доступности 505-го порта, создать 505-й порт в конфигурации
            except NoPlcNameException:
                plc_name = ""
                self.ui.lblStatusText.setText(self.ui.lblStatusText.text() + ' ' + "В файле конфигурации не обозначено имя ПЛК")
                app_logger.info("В файле конфигурации не обозначено имя ПЛК")

            if plc_name != "":
                self.start_register_field = self.ui.spinRegister.value()
                self.buffer_length = self.ui.spinBuffer.value()
                self.msg_qty = self.ui.spinMessages.value()

                app_logger.info("Событие дроп, новых сообщений: %d " % self.msg_qty)
                app_logger.info("Событие дроп, стартовый регистр: %d " % self.start_register_field)

                new_config_dict = filling_new_config(
                    json_data, plc_name,
                    self.start_register_field,
                    self._msg_qty)

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

        event.acceptProposedAction()


def put_new_plc_module(config_dict: dict, port: int) -> dict:
    """
    Добавление нового модуля ПЛК в JSON-конфигурацию
    :param config_dict: Словарь с JSON-конфигурацей
    :param port: Используемый порт для нового модуля ПЛК
    :return: Обновлённый словарь с JSON-конфигурацией
    """
    plc_name = "Logger_plc_module"
    new_plc_module_configuration = """
    {
      "Type": "TrekMark.Drivers.Boards.ModbusMaster.ModbusMaster",
      "IsInitialized": true,
      "Name": "Logger_plc",
      "SignalActivationDelay": 0,
      "SignalDeactivationDelay": 0,
      "Parameters": [
        {
          "Name": "Адрес Modbus Client",
          "Value": "192.168.0.12"
        },
        {
          "Name": "Сетевой порт Modbus Client",
          "Value": 505
        },
        {
          "Name": "Время ожидания сообщений",
          "Value": 0
        },
        {
          "Name": "Использование TCP Keepalive",
          "Value": false
        },
        {
          "Name": "Период опроса регистров",
          "Value": 100
        }
      ],
      "AddressesToRead": [],
      "AddressesToWrite": [],
      "IsUsing": true
    }
    """
    pass


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

# todo: добавить параметр buffer length,
#  и сделать сборку 2 списков в разных циклах, поскольку,
#  в общем случае,
#  длина буфера >= количеству регистрируемых событий на ПЛК


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
