# -*- coding: utf-8 -*-
# !/usr/bin/python


def getLogger(module_name):
    import logging
    # from logging.handlers import TimedRotatingFileHandler
    print(module_name)
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=module_name+'.log',
                        filemode='a')

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    console.setFormatter(formatter)
    mylog = logging.getLogger(module_name)
    mylog.addHandler(console)

    return mylog




# if __name__ == "__main__":
# logger.debug('test get_seconds() ' + get_seconds())
# logger.debug('test get_string() ' + get_string('weixin', 'appID'))
# logger.debug('test get_string() ' + get_string('weixin', 'appSecret'))
# logger.debug(get_key_list('account'))
# logger.debug(get_value_list('account'))
