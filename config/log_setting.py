[loggers]
keys=root

[handlers]
keys=consoleHandler,fileHandler

[formatters]
keys=f1

[logger_root]
level=WARNING
handlers=fileHandler,consoleHandler

[handler_consoleHandler]
class=StreamHandler
formatter=f1
args=(sys.stdout,)

[handler_fileHandler]
class=FileHandler
formatter=f1
args=('/home/keisukeo/test.log',)

[formatter_f1]
format=[%(asctime)s]%(filename)s(%(lineno)d): %(message)s
datefmt=%Y-%m-%d %H:%M:%S