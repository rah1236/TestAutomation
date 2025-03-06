import pyvisa

# Create a Resource Manager
rm = pyvisa.ResourceManager()

# Connect to the device using its VISA resource string
# Replace the IP address with your device's address
visa_address = 'TCPIP0::192.168.2.2::INSTR'
try:
   instrument = rm.open_resource(visa_address)
  
   # Set timeout (optional)
   instrument.timeout = 5000  # milliseconds
  
   # Send a command (example: *IDN? is a common identification query)
   response = float(instrument.query('*IDN?'))
   print(f"Device response: {response}")

   # Close the connection
   instrument.close()
  
except pyvisa.Error as e:
   print(f"Error: {e}")