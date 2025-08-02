import logging
from syslog_handler import SyslogHandler

syslog_server_addr = "192.168.1.101"
syslog_server_port = 514

logging.basicConfig(level=logging.INFO)
logging.getLogger().addHandler(SyslogHandler((syslog_server_addr, syslog_server_port)))

logging.info("Test message Info")
logging.error("Test message Error")
logging.warning("Test message Warning")
logging.debug("Test message Debug")  # This won't get logged when level=logging.INFO
