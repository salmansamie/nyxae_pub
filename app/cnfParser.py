#!~/PycharmProjects/__VENV__/venv_nyxae/bin/python

import os
import configparser

__author__ = "salmansamie"


class CNFparser:

    config = configparser.ConfigParser()
    config.read(os.path.join('config', 'config.ini'))

    # Overriding configurations
    @staticmethod
    def config_parsed():
        server_ip = CNFparser.config['DEFAULT']['Default.SERVER_IP']
        server_port = int(CNFparser.config['DEFAULT']['Default.SERVER_PORT'])

        allowed_ext = (CNFparser.config['DEFAULT']['Default.AllowedExt']).split('\n')
        upload_path = CNFparser.config['DEFAULT']['Default.UploadPath']

        return [server_ip, server_port, allowed_ext, upload_path]

    # Returns timer dictionary for the drop-down menu
    @staticmethod
    def timer_KeyVal():
        Parse_keys = (CNFparser.config['DEFAULT'])
        TimeKV = dict()
        for key in Parse_keys:
            if key.startswith('default.storagetimer'):
                newKey = key.split('_', 1)[1]
                TimeKV[newKey] = int(CNFparser.config['DEFAULT'][key])
        return [TimeKV, [x.split('_', 1)[0] for x in TimeKV.keys()]]

    # Returns MySQL User, DB
    @staticmethod
    def mysql_db_user():
        MySQL_SERVER = CNFparser.config['DEFAULT']['Default.MySQL_SERVER']
        MySQL_USER = CNFparser.config['DEFAULT']['Default.MySQL_USER']
        MySQL_DB = CNFparser.config['DEFAULT']['Default.MySQL_DB']
        MySQL_Charset = CNFparser.config['DEFAULT']['Default.MySQL_Charset']
        return [MySQL_SERVER, MySQL_USER, MySQL_DB, MySQL_Charset]


# print(CNFparser.timer_KeyVal()[0])
# {'5 min': 300, '15 min': 900, '45 min': 2700, '3 hrs': 10800, '6 hrs': 24300}

# print(CNFparser.timer_KeyVal()[1])
# ['5 min', '15 min', '45 min', '3 hrs', '6 hrs']
