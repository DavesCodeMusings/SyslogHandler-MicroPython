import logging
import socket


class SyslogHandler(logging.Handler):
    """
    A logging handler to send MicroPython generated messages to a network-based syslog server.

    Args:
        address (tupple): ip address (string) and port number (integer) of syslog server
        facility (integer): RFC 5424 facility code. Defaults to LOG_USER (1) user-level messages
        socktype (socket.SOCK_DGRAM): currently only UDP datagrams are supported
    """

    # A single RFC 5424 facility code.
    # Since we're not an operating system, other codes do not apply.
    LOG_USER = 1

    # Subset of RFC 5424 severity codes applicable to MicroPython logging.
    LOG_CRIT = 2
    LOG_ERR = 3
    LOG_WARNING = 4
    LOG_NOTICE = 5
    LOG_INFO = 6
    LOG_DEBUG = 7

    # Map MicroPython logging level names to RFC 5424 severities.
    severity_names = {
        "CRITICAL": LOG_CRIT,
        "ERROR": LOG_ERR,
        "WARNING": LOG_WARNING,
        "INFO": LOG_INFO,
        "DEBUG": LOG_DEBUG,
        "NOTSET": LOG_NOTICE,
    }

    # Map MicroPython logging level constants to RFC 5424 severities.
    severity_codes = {
        logging.CRITICAL: LOG_CRIT,
        logging.ERROR: LOG_ERR,
        logging.WARNING: LOG_WARNING,
        logging.INFO: LOG_INFO,
        logging.DEBUG: LOG_DEBUG,
        logging.NOTSET: LOG_NOTICE,
    }

    def __init__(
        self, address=("localhost", 514), facility=LOG_USER, socktype=socket.SOCK_DGRAM
    ):
        self.socket = socket.socket(socket.AF_INET, socktype)
        self.facility = facility
        if type(address) is tuple:
            self.sockaddr = socket.getaddrinfo(address[0], address[1])[0][-1]
        else:
            raise (ValueError, "Address must be a tuple (host, port)")

    def encode_priority(self, facility, severity):
        """
        Create an RFC 5424-compliant priority value that combines facility and severity.
        """
        if isinstance(severity, int):
            severity = self.severity_codes[severity]
        elif isinstance(severity, str):
            severity = self.severity_names[severity]
        return (facility << 3) | severity

    def emit(self, record):
        """
        Send UTF-8 encoded priority value and message string to the syslog server.
        """
        priority = "<%d>" % self.encode_priority(self.facility, record.levelno)
        priority = priority.encode("utf-8")
        message = record.message.encode("utf-8")
        self.socket.sendto(priority + message, self.sockaddr)
