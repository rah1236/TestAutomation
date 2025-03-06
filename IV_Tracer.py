import pyvisa
import time
import matplotlib.pyplot as plt

psu_address = ''
dmm_address = ''

def main():
    rm = pyvisa.ResourceManager('@py')

    psu = rm.open_resource(psu_address)
    dmm = rm.open_resource(dmm_address)


    currents_dmm = []
    voltages_dmm = []

    currents_src = []
    voltages_src = []

    instantaneous_voltage = 0
    current = 3

    final_voltage = 500
    voltage_step = 10
 
    for voltage in range(0,final_voltage,voltage_step):
        #Set source voltage
        psu.write(f"SOUR1:VOLT {voltage/100}")
        #set source current limit
        psu.write(f"SOUR1:CURR {current}")
        #enable source
        psu.write('OUTP:STAT CH1,ON')
        #Delay to settle
        time.sleep(0.125)
        currents_dmm.append(float(dmm.query("MEAS:CURR:DC?")))
        voltages_dmm.append(float(dmm.query("MEAS:VOLT:DC?")))
        print(f"voltage: {voltage}")


    psu.write('OUTP:STAT CH1,OFF')

    import matplotlib.pyplot as plt

    # Create the figure and axis for two subplots (1 row, 2 columns)
    plt.figure(figsize=(14, 6))

    # Plot the first I-V curve (dmm data)
    plt.subplot(1, 2, 1)  # 1 row, 2 columns, first subplot
    plt.plot(voltages_dmm, currents_dmm, 'b-', marker='o', markersize=4)
    plt.xlabel('Voltage (V)')
    plt.ylabel('Current (A)')
    plt.title('I-V Characteristic Curve (DMM)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xlim(left=min(min(voltages_dmm), 0))
    plt.ylim(bottom=min(min(currents_dmm), 0))

    # Plot the second I-V curve (source data)
    plt.subplot(1, 2, 2)  # 1 row, 2 columns, second subplot
    plt.plot(voltages_src, currents_src, 'r-', marker='x', markersize=4)
    plt.xlabel('Voltage (V)')
    plt.ylabel('Current (A)')
    plt.title('I-V Characteristic Curve (Source)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xlim(left=min(min(voltages_src), 0))
    plt.ylim(bottom=min(min(currents_src), 0))

    # Add tight layout to prevent label clipping
    plt.tight_layout()

    # Save the plot as a PNG image
    plt.savefig('iv_comparison.png', dpi=300, bbox_inches='tight')

    # Optional: clear the plot from memory
    plt.close()


    psu.write('OUTP:STAT CH1,OFF')
if __name__ == "__main__":
    main()




