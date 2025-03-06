import pyvisa
import time
import matplotlib.pyplot as plt

# Dictionary of known manufacturers and their model number positions in IDN string
MANUFACTURER_FORMATS = {
    'KEYSIGHT': 1,
    'AGILENT': 1,
    'HEWLETT': 1,  # For HP/Agilent legacy devices
    'RIGOL': 1,
    'TEKTRONIX': 1,
    'ROHDE': 1,    # For Rohde & Schwarz
    'SIGLENT': 1,
    'NATIONAL': 1, # For National Instruments
    'FLUKE': 1,
    'ANRITSU': 1,
    'GW': 1,       # For GW Instek
    'BK': 1        # For BK Precision
}

def get_model_number(idn_string):
    """Extract model number from IDN string based on manufacturer format."""
    parts = idn_string.split(',')
    if not parts:
        return idn_string
    
    # Get manufacturer from first part of IDN string
    manufacturer = parts[0].strip().upper().split()[0]
    
    try:
        # Get model number based on manufacturer's format
        model_position = MANUFACTURER_FORMATS.get(manufacturer, 1)  # Default to position 1 if unknown
        model = parts[model_position].strip()
        return model
    except (IndexError, AttributeError):
        # If parsing fails, return the full IDN string
        return idn_string

def main():
    rm = pyvisa.ResourceManager('@py')
    device_list = rm.list_resources()
    devices = {}

    for device_id in device_list:
        try:
            # Open device and add it to dict
            devices[device_id] = rm.open_resource(device_id)
            
            # Acquire Device name
            device_name = devices[device_id].query("*IDN?")[:-2]
            
            # Get model number using the helper function
            model = get_model_number(device_name)
            
            # Replace device id with model number in dict
            devices[model] = devices.pop(device_id)
            
        except Exception as e:
            print(f"Error processing device {device_id}: {str(e)}")
            continue

    print(devices.keys())

    # currents_dmm = []
    # voltages_dmm = []

    # currents_src = []
    # voltages_src = []

    # instantaneous_voltage = 0
    # current = 3

    # final_voltage = 500
    # voltage_step = 10
 
    # for voltage in range(0,final_voltage,voltage_step):
    #     #Set source voltage
    #     devices['DP832'].write(f"SOUR1:VOLT {voltage/100}")
    #     #set source current limit
    #     devices['DP832'].write(f"SOUR1:CURR {current}")
    #     #enable source
    #     devices['DP832'].write('OUTP:STAT CH1,ON')
    #     #Delay to settle
    #     time.sleep(0.125)
    #     currents_dmm.append(float(devices['DM3058E'].query("MEAS:CURR:DC?")))
    #     currents_src.append(float(devices['DP832'].query("MEAS:CURR:DC? CH1")))
    #     voltages_dmm.append(float(devices['EDU34450A'].query("MEAS:VOLT:DC?")))
    #     voltages_src.append(float(devices['DP832'].query("MEAS:VOLT:DC? CH1")))
    #     print(f"voltage: {voltage}")


    # devices['DP832'].write('OUTP:STAT CH1,OFF')

    # import matplotlib.pyplot as plt

    # # Create the figure and axis for two subplots (1 row, 2 columns)
    # plt.figure(figsize=(14, 6))

    # # Plot the first I-V curve (dmm data)
    # plt.subplot(1, 2, 1)  # 1 row, 2 columns, first subplot
    # plt.plot(voltages_dmm, currents_dmm, 'b-', marker='o', markersize=4)
    # plt.xlabel('Voltage (V)')
    # plt.ylabel('Current (A)')
    # plt.title('I-V Characteristic Curve (DMM)')
    # plt.grid(True, linestyle='--', alpha=0.7)
    # plt.xlim(left=min(min(voltages_dmm), 0))
    # plt.ylim(bottom=min(min(currents_dmm), 0))

    # # Plot the second I-V curve (source data)
    # plt.subplot(1, 2, 2)  # 1 row, 2 columns, second subplot
    # plt.plot(voltages_src, currents_src, 'r-', marker='x', markersize=4)
    # plt.xlabel('Voltage (V)')
    # plt.ylabel('Current (A)')
    # plt.title('I-V Characteristic Curve (Source)')
    # plt.grid(True, linestyle='--', alpha=0.7)
    # plt.xlim(left=min(min(voltages_src), 0))
    # plt.ylim(bottom=min(min(currents_src), 0))

    # # Add tight layout to prevent label clipping
    # plt.tight_layout()

    # # Save the plot as a PNG image
    # plt.savefig('iv_comparison.png', dpi=300, bbox_inches='tight')

    # # Optional: clear the plot from memory
    # plt.close()


    # devices['DP832'].write('OUTP:STAT CH3,OFF')
if __name__ == "__main__":
    main()




