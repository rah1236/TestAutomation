import pyvisa
import time
import matplotlib.pyplot as plt
import numpy as np

# THIS IS AN EXAMPLE OF THE POPULATED CODE BASE FOR IV_curve_template.py
# This example uses a Rigol DP832 for a power supply, and an Agilent 34461A for a multimeter

# Replace these with your actual instrument addresses
psu_resource_name = 'USB0::0x1AB1::0x0E11::DP8C172001883::INSTR' 
dmm_resource_name = 'USB0::0x0957::0x1A07::MY53202914::INSTR'  

# Create resource manager and connect to instruments
rm = pyvisa.ResourceManager()

psu = rm.open_resource(psu_resource_name)
psu.timeout = 5000  # timeout in milliseconds
psu.write('*RST')   # reset the device to bring it to a known state

dmm = rm.open_resource(dmm_resource_name)
dmm.timeout = 5000  # timeout in milliseconds
dmm.write('*RST')   # reset the device to bring it to a known state

# Data storage
measured_currents_list = []
measured_voltages_list = []

# Test parameters
current_limit = 0.5  # Amps
final_voltage = 5  # Volts
voltage_step = 0.2   # Volts

# Pre-Sweep setup
# This code needs to do the following:
#   Set the intial voltage and the current limit
#   Write an output to the PSU
#   Be sure to set a current limit for your output! 
#     If your current limit is too high you could damage a device
# INSERT YOUR CODE HERE
###############################################################
psu.write(f"SOUR1:VOLT:LEV:IMM:AMPL 0") #Set the voltage to 0V 
psu.write(f"SOUR1:CURR:LEV:IMM:AMPL 0.5") #Set the current max output to the current limit
psu.write("OUTP:STAT ON") #Turn on the PSU
###############################################################

# Voltage sweep
# This for loop must do the following on each iteration:
#   Set the output voltage using the 'voltage' int variable that iterates up by the amount 'voltage_step'
#   Measure the series current into the DUT
#   Measure the voltage across the DUT
#   Append both measurements to the 'measured_currents_list' and 'measured_voltages_list'
for voltage in np.arange(0, final_voltage + voltage_step, voltage_step):
    voltage = round(voltage, 2)
    
    # INSERT YOUR CODE HERE
    ###############################################################
    psu.write(f"SOUR1:VOLT:LEV:IMM:AMPL {voltage}") #Set the voltage 


    measured_voltage = -1 * float(dmm.query('MEAS:VOLT:DC? AUTO')) #measure and record voltage
    measured_current = float(dmm.query('MEAS:CURR:DC? AUTO')) #measure and record current
    ###############################################################
    # Wait for measurement to settle
    time.sleep(0.75)
    
    # Measure with DMM
    measured_currents_list.append(measured_current)
    measured_voltages_list.append(measured_voltage)
    
    print(f"V={voltage}V, I={measured_currents_list[-1]:.4f}A")

# Turn off power supply output
# INSERT YOUR CODE HERE
###############################################################
psu.write("OUTP:STAT OFF") #Turn off the PSU
###############################################################

# Plot results
# plt.figure(figsize=(12, 5))

# DMM data plot
plt.plot(measured_voltages_list, measured_currents_list, 'b-o')
plt.xlabel('Voltage (V)')
plt.ylabel('Current (A)')
plt.title('I-V Curve (DMM)')
plt.grid(True)


# plt.tight_layout()
plt.show()
# plt.savefig('iv_comparison.png', dpi=300)

# Close connections
psu.close()
dmm.close()
rm.close()
