import pyvisa

# Create a Resource Manager
rm = pyvisa.ResourceManager()

# Connect to the device using its VISA resource string
# Replace the IP address with your device's address
visa_address = 'TCPIP0::129.65.138.235::inst0::INSTR'
# visa_address = 'TCPIP0::169.254.166.120::inst0::INSTR'
try:
   instrument = rm.open_resource(visa_address)
  
   # Set timeout (optional)
   instrument.timeout = 5000  # milliseconds
  
   # Send a command (example: *IDN? is a common identification query)
   response = instrument.query('*IDN?')
   print(f"Device response: {response}")

   # Close the connection
   instrument.close()
  
except pyvisa.Error as e:
   print(f"Error: {e}")