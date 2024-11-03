from functionalities import get_ipv4s_from_log
from predicates import Other, PasswordFail, PasswordAccepted, Error
from functionalities import get_logs
from ipaddress import IPv4Address
from datetime import datetime
from regexes import analysis_regexes
import re


class SSHLogJournal:
    def __init__(self):
        self.log_journal = []
        self.ip_dict = {}
        self.date_dict = {}

    def add_entry(self, entry):
        log_type = self.determine_log_type(entry)
        entry_object = log_type(entry)
        if entry_object.validate():
            self.log_journal.append(entry_object)
            self.append_date_dict(entry_object)
            self.append_ip_dict(entry_object)

        else:
            entry_other = Other(entry)
            self.log_journal.append(entry_other)
            self.append_ip_dict(entry_other)
            self.append_date_dict(entry_other)

    def __len__(self):
        return len(self.log_journal)

    def __contains__(self, item):
        return item in self.log_journal

    def __iter__(self):
        return iter(self.log_journal)

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.log_journal[key]
        elif isinstance(key, IPv4Address):
            return self.ip_dict.get(str(key), None)
        elif isinstance(key, datetime):
            return self.date_dict.get(str(key), None)
        else:
            raise KeyError("Key does not match")

    def get_logs_with_given_ip(self, searched_ip):
        return [log for log in self.log_journal if log.has_ip and searched_ip in get_ipv4s_from_log(log.event)]

    def append_ip_dict(self, log):
        content = log.event
        ips = get_ipv4s_from_log(content)
        for ip in ips:
            if ip in self.ip_dict:
                self.ip_dict[ip].append(log)
            else:
                self.ip_dict[ip] = [log]

    def append_date_dict(self, log):
        log_date = log.time
        if log_date in self.date_dict:
            self.date_dict[log_date].append(log)
        else:
            self.date_dict[log_date] = [log]

    @staticmethod
    def determine_log_type(entry):
        for log_type, regex in analysis_regexes.items():
            if re.match(regex, entry):
                if log_type == 'accepted password':
                    return PasswordAccepted
                elif log_type == 'failed password':
                    return PasswordFail
                elif log_type == 'error':
                    return Error
            return Other


def create_sample_journal(amount):
    # creating a sample journal
    log_journal = SSHLogJournal()
    i = 0
    for log in get_logs('SSH.log'):
        log_journal.add_entry(log)
        i += 1
        if i == amount:
            break
    return log_journal


if __name__ == '__main__':
    log_journal = create_sample_journal(20)

    ip_address = IPv4Address('173.234.31.186')
    logs_with_given_ip = log_journal[ip_address]
    for log in logs_with_given_ip:
        print(log)
