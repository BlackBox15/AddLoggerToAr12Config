# Скрипт для добавления функций логирования в файл конфигурации Ар12.
# Нужно открыть файл конфигурации, внести в него блок с логгером по-умолчанию, сохранить файл конфигурации
import json
import logging
import sys
from json import JSONDecodeError

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QDialog, QVBoxLayout, QLabel, \
    QButtonGroup, QRadioButton, QHBoxLayout, QPushButton

from CustomExceptions import NoPlcNameException
from MyExternalMethods import ip_check
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
CURRENT_VERSION_FOR_WINDOW_TITLE = 0.5


class PlcNameChooseWindow(QDialog):
    def __init__(self, options, parent=None, title="Выберите ПЛК"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.selected_value = None

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Выберите один из вариантов:"))

        self.group = QButtonGroup(self)
        self.buttons = []
        for i, opt in enumerate(options):
            rb = QRadioButton(opt)
            self.group.addButton(rb, i)
            layout.addWidget(rb)
            self.buttons.append(rb)
            if i == 0:
                rb.setChecked(True)  # по умолчанию — первый

        # Кнопки OK / Cancel
        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Отмена")
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

    def get_selected(self):
        """Возвращает текст выбранной радио-кнопки или None."""
        btn = self.group.checkedButton()
        return btn.text()

    def reject(self):
        """Esc / Cancel / крестик -> берём дефолт и закрываемся как Accepted."""
        # self.group.button(self.default_index).setChecked(True)
        super().accept()


class MainWindow(QMainWindow):
    _user_input_errors = {'ip_address_incorrect': ''}
    _default_status_text = "-> Перетащите сюда configuration.json"

    def __init__(self):

        super(MainWindow, self).__init__()
        # поля
        self.ip_value = DEFAULT_IP_ADDRESS
        self.port_value = DEFAULT_PORT
        self.lines_value = DEFAULT_START_REGISTER
        self.messages_value = DEFAULT_BUFFER_LENGTH
        self.register_value = DEFAULT_START_REGISTER
        #
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
        self.ui.linePlcIpAddress.setText(self.ip_value)
        self.ui.linePlcIpAddress.editingFinished.connect(self.on_ip_changed)
        # spinBoxes
        self.ui.spinPort.valueChanged.connect(self.on_port_changed)
        self.ui.spinRegister.valueChanged.connect(self.on_register_changed)
        self.ui.spinMessages.valueChanged.connect(self.on_messages_changed)
        self.ui.spinBuffer.valueChanged.connect(self.on_buffer_changed)

    @property
    def check_err(self):
        return any(self._user_input_errors.values())

    @property
    def all_err(self):
        return self._user_input_errors.values()

    @property
    def ip_error(self) -> str:
        return self._user_input_errors['ip_address_incorrect']

    @ip_error.setter
    def ip_error(self, value: str):
        self._user_input_errors['ip_address_incorrect'] = value

    @property
    def get_def_status(self):
        return self._default_status_text

    @property
    def ip_value(self):
        return self._ip_value

    @ip_value.setter
    def ip_value(self, value):
        self._ip_value = value

    @property
    def port_value(self):
        return self._port_value

    @port_value.setter
    def port_value(self, value):
        self._port_value = value

    @property
    def messages_value(self):
        return self._messages_value

    @messages_value.setter
    def messages_value(self, value):
        self._messages_value = value

    @property
    def lines_value(self):
        return self._lines_value

    @lines_value.setter
    def lines_value(self, value):
        self._lines_value = value

    @property
    def register_value(self):
        return self._register_value

    @register_value.setter
    def register_value(self, value):
        self._register_value = value

    def on_ip_changed(self):
        value = self.ui.linePlcIpAddress.text()
        if ip_check(value):
            self.ip_value = value
            self.ui.linePlcIpAddress.setText(value)
        else:
            self.ui.linePlcIpAddress.setText(self.ip_value)

    def on_port_changed(self, value: int):
        self.port_value = value

    def on_register_changed(self, value: int):
        self.register_value = value

    def on_messages_changed(self, value: int):
        self.lines_value = value
        if self.messages_value < self.lines_value:
            self.messages_value = self.lines_value
            self.ui.spinBuffer.setValue(self.messages_value)

    def on_buffer_changed(self, value: int):
        self.messages_value = value
        if self.lines_value > self.messages_value:
            self.lines_value = self.messages_value
            self.ui.spinMessages.setValue(self.lines_value)

    # def ip_check(self):
    #     """
    #     Проверка корректности информации на соответствие формату IP-адреса
    #     """
    #     new_ip_address = self.ui.linePlcIpAddress.text().strip()
    #
    #     try:
    #         ip = ip_address(new_ip_address)
    #         if not isinstance(ip, IPv4Address):
    #             raise ValueError
    #         else:
    #             self.ip_value = new_ip_address
    #             self.ip_error = ''
    #             app_logger.info("IP адрес обновлён: " + new_ip_address)
    #     except ValueError:
    #         self.ip_error = "Некорректный IP адрес"
    #         app_logger.error("Некорректный IP адрес")
    #     finally:
    #         self.ui.lblStatusText.setText(self.status_check())

    def status_check(self) -> str:
        for value in self.all_err:
            if value != '':
                self.setAcceptDrops(False)
                return value
        else:
            self.setAcceptDrops(True)
            return self.get_def_status

    def dragEnterEvent(self,
                       event):
        """
        Функция вызывается при "заносе" внутрь границ окна объекта
        :param event:
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

    def dropEvent(self,
                  event):
        """
        Функция вызывается при "сбросе" объекта внутри границ окна
        :param event:
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
                    self.ui.lblStatusText.setText(
                        self.ui.lblStatusText.text() + ' ' + "Ошибка при чтении/парсинге JSON")
                    app_logger.error("Ошибка при чтении/парсинге JSON")
                except UnicodeDecodeError:
                    self.ui.lblStatusText.setText(self.ui.lblStatusText.text() + ' ' + "Ошибка по Unicode")
                    app_logger.error("Ошибка по Unicode")

            try:
                plc_name = get_plc_name(json_data, self)
                # todo: сделать проверку доступности 505-го порта, создать 505-й порт в конфигурации
            except NoPlcNameException as e:
                plc_name = e.args[0]
                self.ui.lblStatusText.setText(
                    self.ui.lblStatusText.text() + ' ' + "В файле конфигурации не обозначено имя ПЛК")
                app_logger.info("В файле конфигурации не обозначено имя ПЛК")

            if plc_name != "":
                self.register_value = self.ui.spinRegister.value()
                self.messages_value = self.ui.spinBuffer.value()
                self.lines_value = self.ui.spinMessages.value()

                app_logger.info("Событие дроп, новых сообщений: %d " % self.lines_value)
                app_logger.info("Событие дроп, стартовый регистр: %d " % self.register_value)

                # todo: перед вызовом диалога сохранения нового конфига нужно быть уверенным,
                #  что заполнение выполнено корректно
                #  как вариант, в случае ошибок при заполнении конфига можно выбрасывать специальные исключения,
                #  таким образом, вызов диалога сохранения нового конфига будет выполняться только при условии отсутствии исключений,
                #  т.е. в случае корректно-заполненного нового конфига

                new_config_dict = filling_new_config(json_data, plc_name,
                                                     self.register_value,
                                                     self._lines_value)

                target_path, _ = QFileDialog.getSaveFileName(self,
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


def put_new_plc_module(config_dict: dict,
                       port: int) -> dict:
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


def get_plc_name(config_dict: dict, parent_window) -> str:
    """
    Получение имени контроллера из файла конфигурации.
    :param config_dict: Словарь JSON-конфигурации
    :param parent_window: Ссылка на родительское окно, используется, чтобы диалоговое появлялось по центру родительского
    :return: имя контроллера
    """
    new_plc_name = "no data"
    plc_modules_qty = len(config_dict['ModulesIO'])

    if plc_modules_qty == 0:
        raise NoPlcNameException(new_plc_name)

    if plc_modules_qty == 1:
        if len(config_dict['ModulesIO'][0]['Name']) != 0:
            new_plc_name = config_dict['ModulesIO'][0]['Name'] or "no data"
        else:
            raise NoPlcNameException(new_plc_name)
    else:
        plc_names = [config_dict['ModulesIO'][i]['Name'] for i in range(plc_modules_qty)]
        dlg = PlcNameChooseWindow(plc_names, parent=parent_window, title="Уточните выбор ПЛК")

        if dlg.exec() == QDialog.DialogCode.Accepted:  # для PyQt6: dlg.exec()
            new_plc_name = dlg.get_selected()

    return new_plc_name


# todo: при заполнении в новом конфиге формируются два JSON-списка:
#  1. список регистров ретроспективного буфера
#  2. и список текстовых возможных текстовых сообщений..
#  Размеры списков, в общем случае, разные.
#  Таким образом в функцию необходимо передавать оба размера как отдельные параметры.
#  Дополнительное проверочное условие: длина буфера >= количеству текстовых сообщений.
def filling_new_config(config_dict: dict,
                       plc_name: str,
                       lines_qty: int,
                       start_register: int = 40_000,
                       messages_qty=None) -> dict:
    """
    Заполнение словаря JSON-конфигурации согласно передаваемым параметрам.
    :param messages_qty: Количество событий в ретроспективной очереди
    :param lines_qty: Количество добавляемых текстовых описаний регистрируемых событий
    :param start_register: начальный Modbus-регистр
    :param config_dict: старый словарь конфигурации
    :param plc_name: имя контроллера
    :return: новый словарь конфигурации
    """
    app_logger.info("Заполнение обновлённого конфига, новых сообщений: %d " % lines_qty)
    app_logger.info("Заполнение обновлённого конфига, стартовый регистр: %d " % start_register)

    lines_list = list()
    messages_list = list()

    if messages_qty is None:
        messages_qty = lines_qty

    for i in range(messages_qty):
        one_message_dict = {
            "Name": "message" + str(i + 1),
            "IsEnabled": True,
            "EventIndex": (i + 1),
            "LoggerName": "Logger1",
            "MessageText": "Message" + str(i + 1),
            "ArgEnabled": "false"
        }
        messages_list.append(one_message_dict)

    for i in range(lines_qty):
        one_line_dict = {
            "TimeRelayNumber": start_register + (i * 4) + 2,
            "EventRelayNumber": (start_register - 30_000) + (i * 4) + 4,
            "ArgRelayNuber": (start_register - 30_000) + (i * 4) + 5
        }
        lines_list.append(one_line_dict)

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
        config_dict['ExternalLoggers'][0]['ExternalLoggerLines'] = lines_list
        config_dict['ExternalLoggers'][0]['ExternalLoggingMessages'] = messages_list
        app_logger.info("New ExternalLoggers added.")
    else:
        QMessageBox.critical("Ошибка", "Поле ExternalLoggers - не пустое")
        app_logger.info("Поле ExternalLoggers - не пустое")

    if len(config_dict['ExternalLoggingMessages']) == 0:
        config_dict['ExternalLoggingMessages'] = messages_list
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
