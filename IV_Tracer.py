import pyvisa
import time
import matplotlib.pyplot as plt
import numpy as np

# VISA resource addresses - modify these based on your actual connection
# Use pyvisa.ResourceManager('@py').list_resources() to find your instruments
psu_address = 'USB0::0x2A8D::0x1102::MY12345678::INSTR'  # Replace with actual EDU36311A address
dmm_address = 'USB0::0x2A8D::0x1401::MY12345678::INSTR'  # Replace with actual EDU34450A address

def main():
    # Create resource manager using py backend
    rm = pyvisa.ResourceManager('@py')
    
    # List available resources (uncomment to debug connections)
    # print("Available resources:", rm.list_resources())
    
    # Connect to instruments
    psu = rm.open_resource(psu_address)
    dmm = rm.open_resource(dmm_address)
    
    # Initialize instrument settings
    initialize_instruments(psu, dmm)
    
    # Data storage
    currents_dmm = []
    voltages_dmm = []
    currents_src = []
    voltages_src = []
    
    # Test parameters
    current_limit = 0.5    # Current limit in Amps (reduced from 3A for safety)
    final_voltage = 5.0    # Maximum voltage in Volts (reduced from 500V for safety)
    voltage_step = 0.2     # Voltage step in Volts
    settle_time = 0.5      # Time to wait for measurements to settle
    
    # Configure PSU for sweep
    psu.write('SOUR1:VOLT 0')     # Start at 0V
    psu.write(f'SOUR1:CURR {current_limit}')  # Set current limit
    
    try:
        # Perform voltage sweep
        for voltage in np.arange(0, final_voltage + voltage_step, voltage_step):
            voltage_rounded = round(voltage, 2)  # Round to 2 decimal places for display
            
            print(f"Setting voltage: {voltage_rounded} V")
            
            # Set source voltage
            psu.write(f"SOUR1:VOLT {voltage_rounded}")
            
            # Enable output
            psu.write('OUTP1 ON')
            
            # Delay to settle
            time.sleep(settle_time)
            
            # Measure current with DMM
            current_dmm = float(dmm.query("MEAS:CURR:DC?"))
            currents_dmm.append(current_dmm)
            
            # Measure voltage with DMM
            voltage_dmm = float(dmm.query("MEAS:VOLT:DC?"))
            voltages_dmm.append(voltage_dmm)
            
            # Read source values from PSU
            current_src = float(psu.query("MEAS:CURR? CH1"))
            currents_src.append(current_src)
            voltage_src = float(psu.query("MEAS:VOLT? CH1"))
            voltages_src.append(voltage_src)
            
            print(f"  Measured: V={voltage_dmm:.4f}V, I={current_dmm:.4f}A")
            
        # Turn off output when done
        psu.write('OUTP1 OFF')
        
        # Plot and save results
        plot_results(voltages_dmm, currents_dmm, voltages_src, currents_src)
        
    except Exception as e:
        print(f"Error during measurement: {e}")
        # Safety: ensure output is off in case of error
        psu.write('OUTP1 OFF')
    
    finally:
        # Close connections
        psu.close()
        dmm.close()
        rm.close()
        print("Measurement completed.")

def initialize_instruments(psu, dmm):
    """Set up the initial configuration for both instruments"""
    # Reset instruments to default state
    psu.write('*RST')
    dmm.write('*RST')
    
    # Wait for reset to complete
    psu.query('*OPC?')
    dmm.query('*OPC?')
    
    # PSU setup - for EDU36311A
    psu.write('SOUR1:VOLT:RANG LOW')  # Low voltage range for better resolution
    psu.write('SOUR1:VOLT 0')         # Start at 0V
    psu.write('OUTP1 OFF')            # Ensure output is off initially
    
    # DMM setup - for EDU34450A
    dmm.write('CONF:VOLT:DC 10')      # Configure for DC voltage measurement, 10V range
    dmm.write('VOLT:DC:NPLC 1')       # Set integration time (1 PLC is a good balance)
    dmm.write('TRIG:SOUR IMM')        # Immediate triggering

def plot_results(voltages_dmm, currents_dmm, voltages_src, currents_src):
    """Create and save plots of the I-V characteristic curves"""
    # Create the figure and axis for two subplots (1 row, 2 columns)
    plt.figure(figsize=(14, 6))
    
    # Plot the first I-V curve (dmm data)
    plt.subplot(1, 2, 1)  # 1 row, 2 columns, first subplot
    plt.plot(voltages_dmm, currents_dmm, 'b-', marker='o', markersize=4)
    plt.xlabel('Voltage (V)')
    plt.ylabel('Current (A)')
    plt.title('I-V Characteristic Curve (DMM Measurements)')
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Set appropriate axis limits
    if voltages_dmm:  # Check if list is not empty
        plt.xlim(left=min(min(voltages_dmm), 0))
        plt.ylim(bottom=min(min(currents_dmm), 0))
    
    # Plot the second I-V curve (source data)
    plt.subplot(1, 2, 2)  # 1 row, 2 columns, second subplot
    plt.plot(voltages_src, currents_src, 'r-', marker='x', markersize=4)
    plt.xlabel('Voltage (V)')
    plt.ylabel('Current (A)')
    plt.title('I-V Characteristic Curve (Source Measurements)')
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Set appropriate axis limits
    if voltages_src:  # Check if list is not empty
        plt.xlim(left=min(min(voltages_src), 0))
        plt.ylim(bottom=min(min(currents_src), 0))
    
    # Add tight layout to prevent label clipping
    plt.tight_layout()
    
    # Save the plot as a PNG image
    plt.savefig('iv_comparison.png', dpi=300, bbox_inches='tight')
    print("Plot saved as 'iv_comparison.png'")
    
    # Optional: show the plot
    plt.show()
    
    # Clear the plot from memory
    plt.close()

if __name__ == "__main__":
    main()