from ipaddress import ip_address, IPv4Address


def ip_check(ip_string: str) -> bool:
    """
    Проверка корректности информации на соответствие формату IP-адреса
    """
    new_ip_address = ip_string.strip()

    try:
        ip = ip_address(new_ip_address)

        if isinstance(ip, IPv4Address):
            return True
    except ValueError:
        return False

    # try:
    #     ip = ip_address(new_ip_address)
    #     if not isinstance(ip, IPv4Address):
    #         return False
    #     else:
    #         return True
    #         self.ip_value = new_ip_address
    #         self.ip_error = ''
    #         app_logger.info("IP адрес обновлён: " + new_ip_address)
    # except ValueError:
    #     self.ip_error = "Некорректный IP адрес"
    #     app_logger.error("Некорректный IP адрес")
    # finally:
    #     self.ui.lblStatusText.setText(self.status_check())
