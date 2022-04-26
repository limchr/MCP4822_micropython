# MCP4822_micropython
Utility class for operating the MCP4822 Digital Analog Converter (and also other versions MCP48x2) in Micropython.

## Basic usage

```python
from machine import SPI, Pin
import time

from mcp4822 import MCP4822


# spi channel
spi_channel = 2
# spi clock gpio pin
sck_pin = 18
# spi mosi gpio pin (miso is not needed)
mosi_pin = 23
# ldac gpio pin (digital output)
ldac_pin = 22
# cs gpio pin (digital output)
cs_pin = 21

# resolution (12 bit for MCP4822, 10 and 8 bit for other chips in the family)
resolution = 12

# initialization of spi interface
spi = SPI(spi_channel, baudrate=1000000, polarity=0, phase=0, bits=16, 
firstbit=SPI.MSB, sck=Pin(sck_pin,Pin.OUT), mosi=Pin(mosi_pin,Pin.OUT), miso=None)

# initialization of utility class
mcp = MCP4822(spi,cs_pin,ldac_pin,resolution)


# writes 0.3*(internal reference voltage * gain multiplier) 
# to channel A (default gain multiplier is 2, can be set as 3. argument)
mcp.write_ratio('A', 0.3)

# sets channel A to fixed voltage of 1.89 volts (default gain multiplier 
# is 2 for a maximum voltage of 4.096V)
mcp.write_voltage('A', 1.89)

# disable unused channel B
mcp.deactivate_channel('B')

# slowly increasing the voltage from 0 to 4.096 volts
for i in range(4096):
	mcp.write_voltage('A',float(i)/1000,2)
	time.sleep_ms(10)

```
