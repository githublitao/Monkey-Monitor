import logging

__author__ = 'Administrator'
import configparser
import os
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def monkey_config(init_file):
    logging.info('读取配置文件')
    config = configparser.ConfigParser()
    config.read(init_file)
    app = {}
    app["package_name"] = config['DEFAULT']['package_name']
    # app["activity"] = config['DEFAULT']['activity']
    app["net"] = config['DEFAULT']['net']
    app["cmd"] = config['DEFAULT']['cmd'] + ">"
    return app


# if __name__ == '__main__':
#     print(monkeyConfig('../monkey.ini'))