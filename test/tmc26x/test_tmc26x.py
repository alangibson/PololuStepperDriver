import logging, unittest
from steppyr.drivers.tmc26x.spi import SPI
from steppyr.drivers.tmc26x import TMC26XDriver, ChopperControllRegister

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

def dump_registers(tmc26x, exclude_zero=False):
  for register_class, register in tmc26x._registers.items():
    for name, representation in register.bits.items():
      value = register.get(representation)
      if exclude_zero and not value:
        continue
      log.debug('    %s %s', name, value)

class TestSuite(unittest.TestCase):
  def test_1(self):
    # Given
    spi_dev = SPI(None, None)
    tmc26x = TMC26XDriver(spi=spi_dev, dir_pin=0, step_pin=0, current=300, resistor=150)
    # When
    tmc26x.activate()
    # Then
    dump_registers(tmc26x)

  def test_load_registers_from_ini(self):
    driver = TMC26XDriver(spi=None, dir_pin=0, step_pin=0)
    driver.load_registers_from_ini('test/tmc26x/data/20170210_02.56.32_TMC26x_Settings.ini')
    dump_registers(driver, exclude_zero=False)
    self.assertEqual(driver._registers[ChopperControllRegister].data, 0x91935 & 0b11111111111111111)

if __name__ == '__main__':
  unittest.main()
