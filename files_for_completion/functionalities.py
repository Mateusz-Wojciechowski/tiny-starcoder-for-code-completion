from PySide6.QtGui import QStandardItem
from regexes import log_date_regex
from datetime import datetime
from PySide6.QtCore import Qt
from constants import date_format, loading_date_format


def load_logs(path, model, pred_fun=lambda item1, item2, item3: True, date_lower=None, date_upper=None):
    model.clear()
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            item = QStandardItem(line)
            date_match = log_date_regex.search(line)
            if date_match:
                date_str = date_match.group(1)
                date_obj = datetime.strptime(date_str, loading_date_format).date()
                if pred_fun(date_lower, date_obj, date_upper):
                    item.setData(date_obj, Qt.UserRole + 1)
                    model.appendRow(item)


def read_one_line(line):
    tokens = line.split()
    domain = tokens[0]
    date_str = (tokens[3] + " " + tokens[4])[1:-1]
    date = datetime.strptime(date_str, date_format)

    if tokens[5] != '""':
        path = tokens[5] + " " + tokens[6] + " " + tokens[7]
    else:
        path = tokens[5]

    log_code = int(tokens[-2])
    bytes_amount = int(tokens[-1]) if tokens[-1] != "-" else 0
    log_data = domain, date, path, log_code, bytes_amount

    return log_data


def pred(date_lower, date, date_upper):
    return date_lower <= date <= date_upper
