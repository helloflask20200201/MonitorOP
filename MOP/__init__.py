import logging
logger = logging.getLogger("MOP.Zabbix")
logger.setLevel(logging.DEBUG)

# create file handler
log_path = "F:/myproject/MonitorOP/logs/zabbix.log"
fh = logging.FileHandler(log_path)
fh.setLevel(logging.INFO)

# create formatter
fmt = "%(asctime)-15s %(levelname)s %(filename)s %(message)s"
datefmt = "%a %d %b %Y %H:%M:%S"
formatter = logging.Formatter(fmt, datefmt)
fh.setFormatter(formatter)

console = logging.StreamHandler()
#console.setLevel(logging.DEBUG)
console.setLevel(logging.INFO)
console.setFormatter(formatter)
# add handler and formatter to logger
logger.addHandler(fh)
logger.addHandler(console)