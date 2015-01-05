import logging


class Log:
    def __init__(self, title):
        log = logging.getLogger(title)
        handler = logging.StreamHandler()
        #~ handler.setFormatter(logging.Formatter('[%(name)s:%(levelname)s]' +
                                               #~ '@%(lineno)s %(message)s'))
        handler.setFormatter(logging.Formatter('[%(name)s:%(levelname)s] ' +
                                               '%(message)s'))
        log.addHandler(handler)
        self.log = log

    def level(self, level):
        if level == 'CRITICAL':
            self.log.setLevel(logging.CRITICAL)
        elif level == 'ERROR':
            self.log.setLevel(logging.ERROR)
        elif level == 'WARNING':
            self.log.setLevel(logging.WARNING)
        elif level == 'INFO':
            self.log.setLevel(logging.INFO)
        elif level == 'DEBUG':
            self.log.setLevel(logging.DEBUG)
        else:
            self.log.setLevel(logging.DEBUG)

    def getLevel(self):
        #~ return int(self.log.getLevelName())
        return logging.getLogger().getEffectiveLevel()

    def c(self, txt):
        self.log.critical(str(txt))

    def e(self, txt):
        self.log.error(txt)

    def w(self, txt):
        self.log.warning(txt)

    def i(self, txt):
        self.log.info(txt)

    def d(self, txt):
        self.log.debug(txt)

    def n(self, txt):
        self.log.notset(txt)
