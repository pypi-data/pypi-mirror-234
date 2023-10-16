import logging
from threading import Thread
from time import sleep

from prusa.connect.printer import Printer, const

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    SERVER = 'http://dev.ct.xln.cz'
    # SERVER = 'http://dev.connect.prusa:8080'
    SN = 'SERIAL_NUMBER_FROM_PRINTER'
    FINGERPRINT = 'Printer fingerprint'
    TOKEN = '949024687e7a4419df6d'
    printer = Printer(type_=const.PrinterType.SL1, sn=SN, fingerprint=FINGERPRINT)
    printer.set_connection(SERVER, TOKEN)

    thread = Thread(target=printer.loop)
    thread.start()

    counter = 0
    while counter < 5:
        printer.telemetry(state=None, timestamp=None, temp_nozzle=24.1, temp_bed=23.2)
        sleep(1)
        counter += 1

    printer.stop_loop()
    thread.join()
