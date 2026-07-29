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
    with open(file_path, 'r', encoding='utf-8-sig') as opened_file:
        try:
            config_json_file = json.load(opened_file)
        except ValueError:
            logging.info("Can't load JSON-file..")
            sys.exit(1)
        logging.info(f"file {opened_file.name} is parsed")

    # Получение имени контроллера, сконфигурированном в файле конфигурации
    if config_json_file['ModulesIO'][0]['Name']:
        plc_name_from_config = config_json_file['ModulesIO'][0]['Name']
        # Проверка и заполнение ExternalLoggers
        if len(config_json_file['ExternalLoggers']) != 0:
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
        else:
            logging.info("ExternalLoggers are not empty!")
            sys.exit(1)

        # Проверка и заполнение ExternalLoggingMessages
        if len(config_json_file['ExternalLoggingMessages']) != 0:
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
        else:
            logging.info("ExternalLoggingMessages are not empty!")
            sys.exit(1)

        # Запись обновлённого файла (с сохранением форматирования)
        new_filename = "edit_" + file_path
        with open(new_filename, 'w', encoding='utf-8') as opened_file:
            json.dump(config_json_file, opened_file, ensure_ascii=False, indent=2)
    else:
        logging.info("Modules IO // Name is empty")
        sys.exit(1)


def main():
    logging.basicConfig(filename="general.log", level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')

    args = parser.parse_args()

    # Validate input file
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
    fill_external_logging_settings(args.input_file)


# Пример использования
if __name__ == "__main__":
    main()
