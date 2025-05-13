import pyvisa
import matplotlib.pyplot as plt
import numpy as np
import time

def plot_frequency_response(frequencies, amplitudes, phases, filename):
    plt.figure(figsize=(10, 8))
    
    # Amplitude vs frequency (linear scale)
    plt.subplot(211)
    plt.semilogx(frequencies, phases, '-o')
    plt.grid(True, which="both", ls="--")
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Phase (Deg)')
    plt.title('Phase Response - Degree Scale')
    
    # Amplitude in dB
    plt.subplot(212)
    max_amp = max(amplitudes) if amplitudes and max(amplitudes) > 0 else 1
    db_values = [20 * np.log10(a) for a in amplitudes]
    plt.semilogx(frequencies, db_values, '-o')
    plt.grid(True, which="both", ls="--")
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude (dB)')
    plt.title('Magnitude Response - dB Scale')
    plt.ylim([-40, 5])
    
    plt.tight_layout()
    plt.savefig(filename.replace('.csv', '.png'))
    plt.show()

# Create a Resource Manager
rm = pyvisa.ResourceManager()

scope_address  = 'USB0::0x0957::0x1799::MY51136625::INSTR'
wavegen_address = 'USB0::0x1AB1::0x0642::DG1ZA220900451::INSTR'

try:
    scope = rm.open_resource(scope_address)
    wavegen = rm.open_resource(wavegen_address)

    # Set timeout
    scope.timeout = 5000  # milliseconds
    wavegen.timeout = 5000
   
    #initialize scope
    scope.write(":CHANNEL1:DISPLAY ON")
    scope.write(":CHANNEL2:DISPLAY ON")
    scope.write(":AUT")

    # SECTION A
    # In this section, be sure to:
        # Make the wave function to be a sinewave
        # Make the peak to peak amplitude 2Volts
        # Make sure that the amplitude offset is 0Volts
        # That the output is off before you start your test
    # WRITE YOUR CODE HERE
    #############################################################
    wavegen.write(":SOURce1:FUNCtion:SHAPe SIN")
    wavegen.write(":SOURce1:VOLTage:AMPLitude 2.0")
    wavegen.write(":SOURce1:VOLTage:OFFSet 0")
    wavegen.write(":OUTPut1:STATe OFF")    
    #############################################################

    # Frequency sweep parameters
    start_freq = 100     # 1 KHz
    stop_freq = 200000   # 200 kHz
    points = 25

    frequencies = np.logspace(np.log10(start_freq), np.log10(stop_freq), points)
    print(f"Starting point-by-point sweep from {start_freq} Hz to {stop_freq} Hz with {points} points")

    amplitudes = []
    phases = []
    
    # Perform point-by-point sweep
    for i, freq in enumerate(frequencies):
        print(f"Testing at {freq}")

        # SECTION B
        # In this section, be sure to:
            # Set the function generator frequency to that assigned in the 'freq' variable
            # Enable the function generator output
        # WRITE YOUR CODE HERE
        #############################################################
        wavegen.write(f":SOURce1:FREQuency:FIXed {freq}")
        wavegen.write(":OUTPut1:STATe ON")
        #############################################################

        time.sleep(1)  # Allow settling time
        
        # SECTION C
        # In this section be sure to:
            # Set the scope to be scaled correctly in the vertical and horizontal axis
            # *HINT* the ":AUT" command behaves a lot like the "Auto Scale" button on the front panel of the scope
            # Set Channel 1 and 2 of the scope to be AC coupled
        # WRITE YOUR CODE HERE
        #############################################################
        scope.write(":AUT")
        scope.write(":CHANNEL1:COUPling AC")
        scope.write(":CHANNEL2:COUPling AC")
        #############################################################
        
        time.sleep(1.5)
        
        #take measurement
        try:
            
            # Section D 
            # In this section be sure to:
                # Measure the amplitude at the input to the network and store it as a float in 'measurement_in'
                # Do the same as above but for 'measurement out'
                # Measure the phase between the two channels (input and output)
            # WRITE YOUR CODE HERE
            #############################################################
            measurement_in = float(scope.query(':MEASure:VAMP? CHAN1'))
            measurement_out = float(scope.query(':MEASure:VAMP? CHAN2'))
                               

            amplitudes.append(measurement_out/measurement_in)
            
            meas_phase = float(scope.query(':MEAS:PHAS? CHAN2,CHAN1'))

            phases.append(meas_phase)
            #############################################################

        except Exception as e:
            print(f"Error at {freq} Hz: {e}")
            amplitudes.append(0)

    plot_frequency_response(frequencies, amplitudes,phases, "Bode_Plot.png")  
    
    # Section E
    # Disable the function generator output
    # WRITE YOUR CODE HERE
    #############################################################
    wavegen.write(":OUTPut1:STATe OFF")
    #############################################################

    # Close the connection
    scope.close()
    wavegen.close()
  
except pyvisa.Error as e:
   print(f"Error: {e}")
