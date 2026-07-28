# Скрипт для добавления функций логирования в файл конфигурации Ар12.
import argparse
# Нужно открыть файл конфигурации, внести в него блок с логгером по-умолчанию, сохранить файл конфигурации
import json
import os
import sys


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
            "FutureEntryRelayNumber": 40050,    # адрес регистра LogIndex, его формат dword, поэтому адресация вида 40ххх
            "ExternalLoggerLines": [
                {                               # структура данных 1-го события
                    "TimeRelayNumber": 40052,   # адрес регистра времени 1-го события, формат dword
                    "EventRelayNumber": 10054,  # адрес регистра порядкового номера события (id), формат word
                    "ArgRelayNuber": 10055      # адрес регистра аргумента, формат величины - word, не используется
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

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('input_file')

    parser.add_argument('-s', '--start',
        type=int,
        default=10000
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true'
    )

    args = parser.parse_args()

    # Validate input file
    if not os.path.exists(args.input_file):
        print(f"Error: File '{args.input_file}' does not exist.")
        sys.exit(1)

    if not os.path.isfile(args.input_file):
        print(f"Error: '{args.input_file}' is not a file.")
        sys.exit(1)

    fill_external_logging_settings("settings.json")


    # success, message, count = process_register_comments(args.input_file, args.start)

# Пример использования
if __name__ == "__main__":
    main()
