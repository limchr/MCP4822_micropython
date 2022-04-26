from mcp4822 import MCP4822

spi_channel = 2
ldac_pin = 22
cs_pin = 21
sck_pin = 18
mosi_pin = 23
resolution = 12

mcp = MCP4822(spi_channel,sck_pin,mosi_pin,cs_pin,ldac_pin,resolution)


# writes 0.3*(internal reference voltage * gain multiplier) 
# to channel A (default gain multiplier is 2)
mcp.write_ratio('A', 0.3)

# sets channel A to fixed voltage of 1.89 volts (default gain multiplier 
# is 2 for a maximum voltage of 4.096V)
mcp.write_voltage('A', 1.89)

# disable channel B, since we only need channel one
mcp.deactivate_channel('B')
