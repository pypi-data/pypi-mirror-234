""" Функции для терминала CAS"""
from ws_one_stable import settings as s
import re

def get_parsed_input_data(data):
    data = str(data)
    try:
        pars = re.findall(r'\d+', data)
        if pars:
            return pars[0]
    except:
        return s.fail_parse_code


def check_scale_disconnected(data):
    # Провреят, отправлен ли бит, означающий отключение Терминала
    return 0

