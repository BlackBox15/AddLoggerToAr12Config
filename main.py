# Скрипт для добавления функций логирования в файл конфигурации Ар12.
# Нужно открыть файл конфигурации, внести в него блок с логгером по-умолчанию, сохранить файл конфигурации

import argparse
import json
import logging
import os
import sys

logger = logging.getLogger()


def fill_external_logging_settings(file_path):
    """
    Заполняет секции ExternalLoggers и ExternalLoggingMessages в JSON-файле настроек.
    """
    # Чтение текущего содержимого

    with open(file_path, 'r', encoding='utf-8') as opened_file:
        config = json.load(opened_file)
    logging.info("File is opened")

    # Заполнение ExternalLoggers
    config['ExternalLoggers'] = [
        {
            "Name": "test_logger",
            "IsInitialized": True,
            "IsUsing": True,
            "ModuleIOName": "PlcEmul",
            "FutureEntryRelayNumber": 40050,  # адрес регистра LogIndex, его формат dword, поэтому адресация вида 40ххх
            "ExternalLoggerLines": [
                {  # структура данных 1-го события
                    "TimeRelayNumber": 40052,  # адрес регистра времени 1-го события, формат dword
                    "EventRelayNumber": 10054,  # адрес регистра порядкового номера события (id), формат word
                    "ArgRelayNuber": 10055  # адрес регистра аргумента, формат величины - word, не используется
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
    new_filename = "edit_" + file_path
    with open(file_path, 'w', encoding='utf-8') as opened_file:
        json.dump(config, opened_file, ensure_ascii=False, indent=2)


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger.info("main is starting")
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')

    # parser.add_argument('-s', '--start',
    #                     type=int,
    #                     default=10000
    #                     )
    #
    # parser.add_argument(
    #     '-v', '--verbose',
    #     action='store_true'
    # )

    logger.info("args parsed")
    args = parser.parse_args()

    # Validate input file
    if not os.path.exists(args.input_file):
        print(f"Error: File '{args.input_file}' does not exist.")
        sys.exit(1)

    if not os.path.isfile(args.input_file):
        print(f"Error: '{args.input_file}' is not a file.")
        sys.exit(1)

    logger.info(f"Input file: {args.input_file}")
    fill_external_logging_settings(args.input_file)

    # success, message, count = process_register_comments(args.input_file, args.start)


# Пример использования
if __name__ == "__main__":
    main()
