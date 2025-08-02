# SyslogHandler-MicroPython
Forget the print statement, send your debug messages to a network-based syslog server instead!

[![Build SyslogHandler-MicroPython](https://github.com/DavesCodeMusings/SyslogHandler-MicroPython/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/DavesCodeMusings/SyslogHandler-MicroPython/actions/workflows/build.yml)

## What is it?
SyslogHandler is a MicroPython class to extend the functionality of the MicroPython logging module. It lets you set up a custom handler to send messages to a network based syslog server. All of the other logging module features apply, such as filtering by severity and sending output to the console.

## Why should I care?
If you create Internet of Things (IoT) devices and sensors with MicroPython, it's not always convenient to use USB-attached console debugging. Extending the logging module with syslog capability lets you track device health from a remote, centralized server.

## How can I use it?
First, you'll need to install the MicroPython logging module. With mpremote, it's a simple command.

```
mpremote connect PORT mip install logging
```

Next, install this module.

```
mpremote connect PORT mip install github:DavesCodeMusings/SyslogHandler-MicroPython
```

Finally, add the imports to your code and configure the logging handler.

```
import logging
from syslog_handler import SyslogHandler

syslog_server_addr = "192.168.1.101"  # Change this to your syslog server's IP address
syslog_server_port = 514

logging.basicConfig(level=logging.INFO)
logging.getLogger().addHandler(SyslogHandler((syslog_server_addr, syslog_server_port)))
```

A more detailed example can be found in [main.py](src/main.py).

## Troubleshooting
There are plenty of things that can go wrong when logging to a remote server from an IoT device. Here are a few things to check.

* Is your syslog server accepting connections? Try `echo "Testing 1 2 3" | nc 127.0.0.1 514` on the machine hosting the syslog server.
* Is your IoT network firewalled? Be sure to allow port 514/UDP through.
* Is your logging.basicConfig(level) set too high? Default is WARNING and above unless you explicitly set something else.
* Is your MicroPython device connected to the network? Take a look at [boot.py](src/boot.py) for hints on how to get that done.

## Syslog server
The folks at linuxserver.io have a [syslog-ng container](https://docs.linuxserver.io/images/docker-syslog-ng/) that's easy to get up and running on your centralized logging host. The following Docker Compose will help.

```
---
services:
  syslog-ng:
    image: lscr.io/linuxserver/syslog-ng:latest
    container_name: syslog-ng
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Etc/UTC
    volumes:
      - ./config:/config
      - ./logs:/var/log
    ports:
      - 514:514/udp
      - 514:514/tcp  # SyslogHandler-MicroPython only uses UDP, but other clients may use tcp
    restart: unless-stopped
```

This syslog-ng.conf file will do basic logging to a file that rotates daily.

```
@version:4.8
# source for RFC5424 logs
source s_udp_514 {
  network(transport("udp") port(514));
};

source s_tcp_514 {
  network(transport("tcp") port(514));
};

destination d_mesg {
  file("/var/log/$YEAR$MONTH$DAY.log");
};

log {
  source(s_udp_514);
  destination(d_mesg);
};

log {
  source(s_tcp_514);
  destination(d_mesg);
};
```

## Bugs and such
Did you find something that's not working? Use GitHub issues to report it. Please include:

* The behavior you saw and what caused it
* What it should have done instead
* Theories on what might fix the problem

I am a part-time development team of one, so any helpful details you can give are appreciated.
