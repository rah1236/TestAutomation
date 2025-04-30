import pyvisa
import time
import matplotlib.pyplot as plt

# Replace these with your actual instrument addresses
psu_resource_name = 'USB0::0x0957::0x1A07::MY53202914::INSTR'   
dmm_resource_name = 'USB0::0x0957::0x1A07::MY53202914::INSTR'  
smu_resource_name = 'USB0::0x0957::0x1A07::MY53202914::INSTR'

# Create resource manager and connect to instruments
rm = pyvisa.ResourceManager()

# Connect to power supply
psu = rm.open_resource(psu_resource_name)
psu.timeout = 5000  # timeout in milliseconds
psu.write('*RST')   # reset the device to bring it to a known state

# Connect to digital multimeter
dmm = rm.open_resource(dmm_resource_name)
dmm.timeout = 5000  # timeout in milliseconds
dmm.write('*RST')   # reset the device to bring it to a known state

# Connect to source measure unit
smu = rm.open_resource(smu_resource_name)
smu.timeout = 5000  # timeout in milliseconds
smu.write('*RST')   # reset the device to bring it to a known state


# Test parameters for output curves
vce_start = 0.0    # Starting voltage (V)
vce_end = 10.0     # Ending voltage (V)
vce_step = 0.2     # Step size (V)
v_be = 0.7

# Different base currents to test (in microamps)
ib_values_microamps = [0, 10, 50, 100]  
collector_current_limit = 0.500  # Collector current limit (500mA)

# Create dictionaries to store our measurement curves
ic_curves = {}  # Will store current curves for different IB values
vce_actual = {}  # Will store actual measured VCE values

try:

    print("Measuring BJT output characteristic curves...")
    print("This measures how collector current changes with collector-emitter voltage")
    print("for different base current values")
    print("-----------------------------------------------------------------------")

    # Enable both channels
    smu.write("SOUR:CURR:LEV:IMM:AMP 0.0") # Set the smu to 0 current output
    smu.write("SOUR:VOLT:LEV:IMM:AMP 0.0") # Set the smu to 0 voltage output
    smu.write("OUTP:STAT ON") # Turn on the smu

    psu.write("SOUR:CURR:LEV:IMM:AMP 0.0 @1") # Set the channel 1 of the psu to 0 current output
    psu.write("SOUR:VOLT:LEV:IMM:AMP 0.0 @1") # Set the channel 1 of the psu to 0 voltage output
    psu.write("OUTP:STAT ON @1") # Turn on channel 1 of the psu    

    # Generate the list of VCE values to test
    vce_test_values = []

    # Section 1
    # The list 'vce_test_values' is provided, but isn't populated. 
    # You will need to write some code below that fills the list with 
    # the Collector-Emitter Voltages you will want to test.
    # INSERT YOUR CODE HERE
    ###############################################################




    ###############################################################
    

    # Sweep through base currents
    # This is a nested for loop that starts by assigning a base current, before sweeping through a set of 
    # collector-emitter voltages.
    # Measure collector current for each base current
    for ib_microamps in ib_values_microamps:
        # Convert microamps to amps for the power supply
        ib_amps = ib_microamps * 1E-6 
        
        # Lists to store collector currents and actual VCE for this base current
        ic_currents = []
        vce_voltages = []
        
        print(f"\nMeasuring curve for IB = {ib_microamps}µA")
        
        # Section 2
        # Set up the base current
        if ib_microamps == 0:
            # For IB=0, just set base to 0V
            # INSERT YOUR CODE HERE
            ###############################################################

            ###############################################################
        else:
            # For non-zero IB, set VBE to about 0.7V and limit current to desired IB
            # INSERT YOUR CODE HERE
            ###############################################################


            ###############################################################

        # Set up channel 2 for collector
        psu.write(f"SOUR:CURR:LEV:IMM:AMP {collector_current_limit} @1")
        
        # Section 3
        # Sweep through VCE values
        # This for loop uses the 'vce_test_values' you generated prior, and sweeps through them.
        # You will need to apply the new collector-emitter voltage, and measure the collector current, 
        # as well as collector emitter voltage.
        # The measured data will need to be stored in a list called ic_currents, and vce_voltages.
        for vce in vce_test_values:
            # Set collector-emitter voltage
            ###############################################################

            ###############################################################
            
            # Wait for measurement to settle
            ###############################################################

            ###############################################################
            
            # Measure actual VCE voltage 
            ###############################################################

            ###############################################################
            
            # Append the collector emitter voltage to vce_voltages
            ###############################################################

            ###############################################################

            # Measure collector current 
            ###############################################################

            ###############################################################
            
            # Append the collector current to ic_currents
            ###############################################################

            ###############################################################
            
            # Print all of this information for debugging!
            print(f"Set VCE = {vce:.1f}V, Measured VCE = {actual_vce:.3f}V, IC = {collector_current:.2f}mA")
        
        # Store these measurements in our dictionaries
        ic_curves[ib_microamps] = ic_currents
        vce_actual[ib_microamps] = vce_voltages
        # Short delay before data for a new base current is measured
        time.sleep(0.5)

    # Turn off power supply outputs
    smu.write("OUTP:STAT OFF")    # Turn off the smu
    psu.write("OUTP:STAT OFF @1") # Turn off channel 1 of the psu
    
    # Plot the results using measured voltage values
    plt.figure(figsize=(12, 8))

    # Plot each curve
    for ib_microamps in ib_values_microamps:
        # Convert collector currents to milliamps for plotting
        ic_milliamps_list = [ic * 1e3 for ic in ic_curves[ib_microamps]]
        
        # Plot the curve using actual measured VCE values
        plt.plot(vce_actual[ib_microamps], ic_milliamps_list, '-o', 
                linewidth=2, markersize=6, label=f'IB = {ib_microamps}µA')

    plt.xlabel('Collector-Emitter Voltage VCE (V)', fontsize=14)
    plt.ylabel('Collector Current IC (mA)', fontsize=14)
    plt.title('BJT Output Characteristics (IC vs VCE)', fontsize=16)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.5)

    plt.savefig('bjt_output_characteristics.png', dpi=300)
    plt.show()

    # Close the connections
    psu.close()
    dmm.close()
    smu.close()

    print("\nMeasurement complete!")
    print("Results saved to 'bjt_output_characteristics.png'")

except KeyboardInterrupt:

    smu.write("OUTP:STAT OFF")    # Turn off the smu
    psu.write("OUTP:STAT OFF @1") # Turn off channel 1 of the psu

    # Close the connections
    psu.close()
    dmm.close()
    smu.close()

