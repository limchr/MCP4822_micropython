from machine import SPI, Pin
import ustruct
import sys

class MCP4822:
	"""
	Utility class for operating the MCP4822 Digital Analog Converter in Micropython.
	"""

	def __init__(self,spi,cs_pin,ldac_pin,resolution=12):
		"""
		Just sets the passed variables to member variables.
		"""
		self.spi = spi
		self.cs = Pin(cs_pin,Pin.OUT)
		self.ldac = Pin(ldac_pin,Pin.OUT)
		self.resolution = resolution

	def _get_channelbit_from_id(self,ident):
		"""
		Get the bit encoding of a channel identifier A or B for sending to the IC.
		"""
		if ident == 'A':
			channel_bit = 0 # 0 for DAC_A
		elif ident == 'B':
			channel_bit = 1 # 1 for DAC_B
		else:
			print('invalid channel: '+ident)
			sys.exit(1)
		return channel_bit

	def _get_gainbit_from_id(self,ident):
		"""
		Get the bit encoding of a gain identifier 2 or 1 for sending to the IC.
		"""
		if ident == 2:
			gain_bit = 0 # 0 for 4.096V
		elif ident == 1:
			gain_bit = 1 # 1 for 2.048V
		else:
			print('invalid gain mode: '+output_gain)
			sys.exit(1)
		return gain_bit


	def _write_raw(self,send_bytes):
		"""
		Sends the raw 16 bit for configuring the IC's input/output latches.
		"""
		self.ldac.on()
		self.cs.off()
		self.spi.write(ustruct.pack('>H', send_bytes))
		self.cs.on()
		self.ldac.off()


	def activate_channel(self,channel_id):
		"""
		Activates a deactivated channel. On default, all channels are activated.
		"""
		channel_bit = self._get_channelbit_from_id(channel_id)
		command = 0
		command = (command | channel_bit<<15) # channel selection (0 for DAC_A, 1 for DAC_B)
		command = (command | 1<<12) # shutdown bit: 0 for shutdown selected channel, 1 for active operation of channel
		self._write_raw(command)


	def deactivate_channel(self,channel_id):
		"""
		If channels are not used, they can be deactivated with this method.
		"""
		channel_bit = self._get_channelbit_from_id(channel_id)
		command = 0
		command = (command | channel_bit<<15) # channel selection (0 for DAC_A, 1 for DAC_B)
		command = (command | 0<<12) # shutdown bit: 0 for shutdown selected channel, 1 for active operation of channel
		self._write_raw(command)

	def write_ratio(self, channel_id, ratio, gain_mult=2):
		"""
		Write a ratio between ground and Vdd to the selected channel.
		Parameters:
		channel_id: which of the two channels to write ('A' or 'B')
		ratio: a ratio between 0 and 1
		gain_mult: 1 for 2 volts mode or 2 for 4 volts mode
		"""
		if ratio < 0 or ratio >1:
			print('ratio must be between 0 and 1')
			sys.exit(1)
		
		channel_bit = self._get_channelbit_from_id(channel_id)
		gain_bit = self._get_gainbit_from_id(gain_mult)
		
		command = 0
		command = (command | channel_bit<<15) # channel selection (0 for DAC_A, 1 for DAC_B)
		command = (command | gain_bit<<13) # output gain selection (0 for 4.096V, 1 for 2.048V)
		command = (command | 1<<12) # shutdown bit: 0 for shutdown selected channel, 1 for active operation of channel

		# find the highest possible value for the given resolution
		max_v = 2**12
		data = round(max_v * ratio);
		# align lower resolution to the left for <12 bit resolution
		data = data << (12-self.resolution) 
		send = command+data
		self._write_raw(send)



	def write_voltage(self, channel_id, voltage, gain_mult=2):
		"""
		Write a specific voltage to a channel.
		Parameters:
		channel_id: which of the two channels to write ('A' or 'B')
		voltage: a voltage between 0 and 2.048 or 0 and 4.096 (depends on selected gain)
		gain_mult: 1 for 2 volts mode or 2 for 4 volts mode
		"""
		max_voltage = 2.048 if gain_mult == 1 else 4.096		
		if(voltage < 0 or voltage > max_voltage): 
			print('voltage exceed maximum voltage at current configuration')
			sys.exit(1)
		# construct 12 bit data
		ratio = (float(voltage)/max_voltage)
		self.write_ratio(channel_id, ratio, gain_mult)
