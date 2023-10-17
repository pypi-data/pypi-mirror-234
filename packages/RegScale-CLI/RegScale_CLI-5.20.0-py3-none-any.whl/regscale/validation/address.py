import re


def validate_mac_address(mac_address: str) -> bool:
    """
    Simple validation of a mac address input
    :param str mac_address: mac address
    :return: Whether mac address is valid or not
    :rtype: bool
    """
    if not mac_address:
        return False
    return bool(
        re.match(
            "[0-9a-f]{2}(:?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$",
            mac_address.lower(),
        )
    )
