"""
? Author : Delhaye Adrien
IEC 62056 (serial/tcp) module.
This module allows to exchange data using the IEC62056 protocol over a serial line.
* How to use : 
    1) create a client : client = IEC62056Client(baudrate=xxx, device_address="xxx", port="xxx")
    2) client.connect()
    3) read all or registers : client.read_all() | client.read_registers(registers = ["1.8.0", "2.8.0"])
"""

import logging
import time
from typing import List

from iec62056 import messages, transports, constants
from iec62056.client import Iec6205621Client


logger = logging.getLogger(__name__)


class IEC62056Meter:
    
    def __init__(self, address: str, port: int, device_address: str, password: str=None) -> None:
        self._address = address
        self._port = port
        self._device_address = device_address
        self._password = password

    def __repr__(self) -> str:
        return f"Meter (address: {self.device_address}, idenfication : {self.identification}, manufactureur id : {self.manufacturer_id})"

    @property
    def address(self) -> str:
        return self._address
    
    @property
    def port(self) -> int:
        return self._port
    
    @property
    def device_address(self) -> str:
        return self._device_address
    
    @property
    def password(self) -> str:
        return self._password
    
    @property
    def password(self) -> str:
        return self._password
    
    @property
    def identification(self) -> str:
        if hasattr(self, "_identification"):
            return self._identification
        return

    @identification.setter
    def identification(self, identification: str):
        self._identification = identification
    
    @property
    def manufacturer_id(self) -> str:
        if hasattr(self, "_manufacturer_id"):
            return self._manufacturer_id
        return

    @manufacturer_id.setter
    def manufacturer_id(self, manufacturer_id: str):
        self._manufacturer_id = manufacturer_id
    
    @property
    def model(self) -> str:
        if hasattr(self, "_model"):
            return self._model
        else:
            return


class IEC62056Client:
    """ Class to communicate with meter using IEC62056-21 protocol.
    Usage:
    - Create a new client specifying it's baudrate, the port, if needed the meter address (serial number, ..) and the type of client (serial, tcp (encapsulated), ..).
    - To request all dataset available use client.read_all()
    - To request a particular register use client.read_registers(list_of_registers_by_obis_code).

    Returns:
        client : A new instance of a IEC62056 client's.
    """
    BAUDRATE_CHAR = {
        300: "0",
        600: "1",
        1200: "2",
        2400: "3",
        4800: "4",
        9600: "5",
        19200: "6"
    }

    def __init__(
            self,
            port: str,
            baudrate: str=9600,
            address: str=None,
            device_address: str=None,
            transport: str="serial",
            password: str=None,
            parity: str="E",
            **kwargs):
        
        self._baudrate = baudrate
        self._port = port
        self._device_address = device_address
        self._parity = parity
        self._password = password
        self._address = address
        self._port = port

        if transport == "serial":
            self._client =Iec6205621Client.with_serial_transport(
                port=self._port,
                device_address=self._device_address
            )

            self.connect()

            if self._device_address is not None:
                self._client.transport.TRANSPORT_REQUIRES_ADDRESS = True
            self._client.transport.port.baudrate = self._baudrate

        elif transport == "tcp":
            client = Iec6205621Client.with_tcp_transport(
            address=(address, port),
            device_address=self._device_address,
            password=self._password,
            parity=self._parity
        )
        else:
            self.disconnect()
            ValueError(f"Transport : {transport} is not valid.")

    @property
    def baudrate(self) -> int:
        try:
            return self._client.transport.port.baudrate
        except AttributeError:
            return "undefined"
        
    def connect(self):
        if not self._is_connected():
            self._client.connect()

    def _is_connected(self) -> bool:
        if self._client.transport.port is not None:
            return self._client.transport.port.is_open
        return False
    
    def disconnect(self):
        self._client.disconnect()

    def read_registers(self, registers: list=[], table: str= None, timeout: int = 10) -> List[messages.DataSet]:
        """read_registers specified in the list for the requested table of the iec62056-21 meter.

        Args:
            registers (list, optional): list of registers obis code to read. Defaults to [].
            table (str, optional): table to be read. Defaults to 0 which is equivalent to a standart readout.

        Returns:
            List[messages.DataSet]: A list of Dataset element that contains the requested registers if found.
        """
        try:
            start = time.time()
            self.connect()
            self.read_client_identification()
            message = self._get_ack_message(table)
            print(f"Sending {message.to_representation()}")
            data = message.to_bytes()
            time.sleep(1)
            self._write(data)
            time.sleep(timeout)
            datasets = self._read(timeout=timeout)
            stop = time.time()
            diff = stop-start
            print(f"Read Register completed in {diff} seconds")
            return [dataset for dataset in datasets if dataset.address in registers]
        
        except Exception as err:
            logging.error(f"Could not read registers : {err}")
            return []

        finally:
            self.disconnect()

    def read_all(self, timeout: int=10, table: str = None) -> List[messages.DataSet]:
        try:
            self.read_client_identification()
            # Table specification can be used if other table than the standard one has been set.
            message = self._get_ack_message(table)
            data = message.to_bytes()
            time.sleep(1)
            self._write(data)
            time.sleep(timeout)
            return self._read(timeout=timeout)
        
        except Exception as err:
            logging.error(f"Could not read registers : {err}")
        finally:
            self.disconnect()  

    def read_client_identification(self):
        try:
            self._client.send_init_request()
            return self._client.read_identification()
        except Exception as err:
            logger.error(f"Could not get client's identification")

    def _get_ack_message(self, table: str = None) -> messages.AckOptionSelectMessage:
        if table is not None:
            message = messages.AckOptionSelectMessage(
                baud_char=self.BAUDRATE_CHAR[self._baudrate],
                mode_char=table
            )
        else:
            message = messages.AckOptionSelectMessage(
            baud_char=self.BAUDRATE_CHAR[self._baudrate],
            mode_char=Iec6205621Client.MODE_CONTROL_CHARACTER["readout"]
        )
        return message

    def _write(self, data: bytes):
        self._client.transport.port.write(data)

    def _read(self, end_char=constants.END_CHAR, timeout=5) -> List[messages.DataSet]:
        _result = []
        start = time.time()
        while True:
            try:
                line = self._client.transport.port.readline().decode()
                if end_char in line:
                    logger.info(f"END CHAR found in {line}")
                    break
                if timeout and time.time() - start > timeout:
                    logger.info(f"Stopped due to timeout")
                    break
                if "2.8" in line:
                    logging.debug(f"{line}")
                dataset = messages.DataSet.from_representation(line)
                _result.append(dataset)

            except Exception as err:
                logger.warning(f"Could not decode dataset for line : {err}")
        
        return _result

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(address : {self._device_address}, baudrate : {self._baudrate}, port: {self._port})"
    