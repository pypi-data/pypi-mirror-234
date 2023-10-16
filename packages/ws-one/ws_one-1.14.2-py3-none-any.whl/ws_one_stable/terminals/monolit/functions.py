""" Функции для терминала CAS"""
from ws_one_stable import settings as s

def get_parsed_input_data(data):
    try:
        data = data.decode()
        if len(data) == 7:
            return data[:-5]
    except:
        return s.fail_parse_code

def check_scale_disconnected(data):
    # Провреят, отправлен ли бит, означающий отключение Терминала
    return 0
