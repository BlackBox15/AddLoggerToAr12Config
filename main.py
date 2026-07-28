# Скрипт для добавления функций логирования в файл конфигурации Ар12.

# Нужно открыть файл конфигурации, внести в него блок с логгером по-умолчанию, сохранить файл конфигурации
import json

def fill_external_logging_settings(file_path):
    """
    Заполняет секции ExternalLoggers и ExternalLoggingMessages в JSON-файле настроек.
    """
    # Чтение текущего содержимого
    with open(file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # Заполнение ExternalLoggers
    config['ExternalLoggers'] = [
        {
            "Name": "test_logger",
            "IsInitialized": True,
            "IsUsing": True,
            "ModuleIOName": "PlcEmul",
            "FutureEntryRelayNumber": 40050,
            "ExternalLoggerLines": [
                {
                    "TimeRelayNumber": 40052,
                    "EventRelayNumber": 10053,
                    "ArgRelayNuber": 10054
                }
            ]
        }
    ]

    # Заполнение ExternalLoggingMessages
    config['ExternalLoggingMessages'] = [
        {
            "Name": "message1",
            "IsEnabled": True,
            "EventIndex": 1,
            "LoggerName": "test_logger",
            "MessageFormat": "test for message1 with argument = {0}"
        }
    ]

    # Запись обновлённого файла (с сохранением форматирования)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

# Пример использования
if __name__ == "__main__":
    fill_external_logging_settings("settings.json")