# AMS-DIG-PROC python library

<img src="docs/source/ams-dig-proc_small.jpg" style="float: right;">

[AMS-DIG-PROC board](https://vigophotonics.com/product/ams-dig-proc/) is an digital extension board to AMS family of [infrared detection modules](https://vigophotonics.com/products/infrared-detection-modules/inassb-affordable-detection-modules/).

This board provides 7Msamples/s 16-bit data aquisition and 32-bit real time processing capabilities. Onboard processing reduces data rate on the
communication link, therefore simple 1Mbit UART is sufficient in most applications. There is also [USB adapter](https://vigophotonics.com/product/ams-dig-usb/) available, providing power supply and communication interface over a single micro-USB connector.

This repository contains python libraries and C source files to handle communication with the board.

## Python or C? Which should I use?
For Windows/Linux - Python API is recommended. It provides ctypes structs and methods to cast and calculate CRC. Also serial port management and separate reader thread is provided to prevent from blocking the main thread.

For other operating systems or bare metal embedded aplications - C is recommended since it does not introduce any dependencies or specific requirements.
It is designed to be portable and as simple as possible.


## Python installation
```bash
pip install ams-dig-proc
```

## C installation
There is no special requirements or installation procedure for C.

There is a header file available (`C/Inc/protocol.h`).
It contains definitions of all structs (messages) and constants required to work with AMS-DIG-PROC board.

`C/Src/ams_dig_proc_crc.c` contains function that can be used for CRC calculations.



## Examples and documentation
There are many C and Python examples available in the [documentation](https://ams-dig-proc.readthedocs.io/en/latest/index.html)

For more informations about the board and the protocol please check the [AMS-DIG-PROC product page](https://vigophotonics.com/product/ams-dig-proc/)

