def get_all_plc_names(config: dict):
    """
    Получение имён всех существующих модулей ПЛК в файле конфигурации
    :param config: словарь с конфигурацией
    :return:
    """
    result = []
    plc_modules_qty = len(config['ModulesIO'])
    result = [config['ModulesIO'][i]['Name'] for i in range(plc_modules_qty)]
    return result


def create_new_plc(name: str, ip: str, port: int) -> dict:
    """
    Создание нового модуля ПЛК для файла конфигурации
    :param name: имя ПЛК
    :param ip: используемый IP-адрес
    :param port: используемый порт
    :return: JSON-конфигурация
    """

    plc_module = {
        "Type": "TrekMark.Drivers.Boards.ModbusMaster.ModbusMaster",
        "IsInitialized": True,
        "Name": "{plc_name}",
        "SignalActivationDelay": 0,
        "SignalDeactivationDelay": 0,
        "Parameters": [
            {
                "Name": "Адрес Modbus Client",
                "Value": "{ip_address}",
            },
            {
                "Name": "Сетевой порт Modbus Client",
                "Value": {port}
            },
            {
                "Name": "Время ожидания сообщений",
                "Value": 4010
            },
            {
                "Name": "Использование TCP Keepalive",
                "Value": False
            },
            {
                "Name": "Период опроса регистров",
                "Value": 100
            }
        ],
        "AddressesToRead": [],
        "AddressesToWrite": [],
        "IsUsing": True
    }
    return plc_module



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
    plc_names = get_all_plc_names(config_dict['ModulesIO'])

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
                       ip_address: str,
                       port: int,
                       lines_qty: int,
                       start_register: int = 40_000,
                       messages_qty=None) -> dict:
    """
    Заполнение словаря JSON-конфигурации согласно передаваемым параметрам.
    :param ip_address:
    :param port:
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

    config_dict['ModulesIO'].append(create_new_plc(plc_name, ip_address, port))

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