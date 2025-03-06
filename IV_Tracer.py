import pyvisa
import time
import matplotlib.pyplot as plt
import numpy as np

# Replace these with your actual instrument addresses
psu_address = 'USB0::0x2A8D::0x1102::MY12345678::INSTR'  # EDU36311A
dmm_address = 'USB0::0x2A8D::0x1401::MY12345678::INSTR'  # EDU34450A

# Create resource manager and connect to instruments
rm = pyvisa.ResourceManager()
psu = rm.open_resource(psu_address)
dmm = rm.open_resource(dmm_address)

# Reset instruments
psu.write('*RST')
dmm.write('*RST')

# Data storage
currents_dmm = []
voltages_dmm = []

# Test parameters
current_limit = 0.5  # Amps
final_voltage = 5.0  # Volts
voltage_step = 0.2   # Volts

# Configure PSU
psu.write(f'CURRent {current_limit}, (@1)')
psu.write('VOLTage 0, (@1)')

# Voltage sweep
for voltage in np.arange(0, final_voltage + voltage_step, voltage_step):
    voltage = round(voltage, 2)
    
    # Set voltage and enable output
    psu.write(f"VOLTage {voltage}, (@1)")
    psu.write('OUTPut 1, (@1)')
    
    # Wait for measurement to settle
    time.sleep(0.75)
    
    # Measure with DMM
    currents_dmm.append(float(dmm.query("MEAS:CURR:DC?")))
    voltages_dmm.append(float(dmm.query("MEAS:VOLT:DC?")))
    
    print(f"V={voltage}V, I={currents_dmm[-1]:.4f}A")

# Turn off output
psu.write('OUTPut 0, (@1)')

# Plot results
plt.figure(figsize=(12, 5))

# DMM data plot
plt.subplot(1, 2, 1)
plt.plot(voltages_dmm, currents_dmm, 'b-o')
plt.xlabel('Voltage (V)')
plt.ylabel('Current (A)')
plt.title('I-V Curve (DMM)')
plt.grid(True)

# Source data plot
plt.subplot(1, 2, 2)
plt.plot(voltages_src, currents_src, 'r-x')
plt.xlabel('Voltage (V)')
plt.ylabel('Current (A)')
plt.title('I-V Curve (Source)')
plt.grid(True)

plt.tight_layout()
plt.savefig('iv_comparison.png', dpi=300)

# Close connections
psu.close()
dmm.close()
rm.close()