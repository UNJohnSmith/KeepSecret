
import logging, logging.handlers
import sys
from os.path import basename, split, splitext, dirname, join



FORMATTER = logging.Formatter('''%(asctime)s | %(levelname)-8s | file: %(filename)-25s | line: %(lineno)d\n%(message)s\n''')
loggerset = set([-1])

class MyLogger(logging.Logger):
    def new_handler(logger, filepath=None, handlername=None, rotating='FILE'):

        if filepath is None and handlername is None:
            path = sys.argv[0]
            parpath, name = split(path)
            pre, _ = splitext(name)
            filepath = join(parpath, '%s.log' % pre)
            handlername = 'handler_%s' % pre
        elif filepath is not None and handlername is not None:
            pass
        else:
            raise RuntimeError

        if rotating is False:
            vars()[handlername] = logging.FileHandler(filepath)
        elif rotating == 'FILE':
            vars()[handlername] = logging.handlers.RotatingFileHandler(filepath, maxBytes=128 * 1024)
        elif rotating == 'TIME':
            vars()[handlername] = logging.handlers.TimedRotatingFileHandler(time_path, when='D', interval=30)
        else:
            raise RuntimeError
        vars()[handlername].setLevel(logging.DEBUG)
        vars()[handlername].setFormatter(FORMATTER)
        logger.addHandler(vars()[handlername])


def newlogger():

    logger_index = max(loggerset) + 1
    loggerset.add(logger_index)

    logger_name = 'l_%d' % logger_index
    logger = MyLogger(name=logger_name)
    logger.setLevel(logging.DEBUG)


    handler_stdout = logging.StreamHandler(stream=sys.stdout)
    handler_stdout.setLevel(logging.DEBUG)
    handler_stdout.setFormatter(FORMATTER)
    logger.addHandler(handler_stdout)
    logger.handler_stdout = handler_stdout

    return logger



if __name__ == '__main__':
    log.debug('DEBUG')
    log.info('INFO')



























