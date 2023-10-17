import logging
import pytest
from iec62056 import IEC62056Client, IEC62056Meter


TEST_PORT="COM11"
TEST_BAUDRATE=19200
METER_ADDRESS="4862729"
TRANSPORT="serial"


class TestIEC62056Client:

    @pytest.fixture
    def client(self) -> IEC62056Client:
        return IEC62056Client(
            port=TEST_PORT,
            baudrate=TEST_BAUDRATE,
            device_address=METER_ADDRESS,
            transport=TRANSPORT
        )
    
    def test_reading_index(self, client: IEC62056Client):
        registers = client.read_registers(["1.8.0", "2.8.0"])
        logging.info(f"Registers: {registers}")
        assert len(registers) == 2

    def test_reading_all(self, client: IEC62056Client):
        registers = client.read_all(timeout=5)
        assert len(registers) > 20
        for register in registers:
            logging.debug(f"{register}")