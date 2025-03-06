import pyvisa
import matplotlib.pyplot as plt
import numpy as np
import time

def plot_frequency_response(frequencies, amplitudes, filename):
    plt.figure(figsize=(10, 8))
    
    # Amplitude vs frequency (linear scale)
    plt.subplot(211)
    plt.semilogx(frequencies, amplitudes, '-o')
    plt.grid(True, which="both", ls="--")
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude (V)')
    plt.title('Frequency Response - Linear Scale')
    
    # Amplitude in dB
    plt.subplot(212)
    max_amp = max(amplitudes) if amplitudes and max(amplitudes) > 0 else 1
    db_values = [20 * np.log10(max(a, 1e-6) / max_amp) for a in amplitudes]
    plt.semilogx(frequencies, db_values, '-o')
    plt.grid(True, which="both", ls="--")
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude (dB)')
    plt.title('Frequency Response - dB Scale')
    plt.ylim([-40, 5])
    
    plt.tight_layout()
    plt.savefig(filename.replace('.csv', '.png'))
    plt.show()

# Create a Resource Manager
rm = pyvisa.ResourceManager()

scope_address = 'TCPIP0::129.65.138.235::inst0::INSTR'
wavegen_address = ''

try:
    scope = rm.open_resource(scope_address)
    wavegen = rm.open_resource(wavegen_address)

    # Set timeout
    scope.timeout = 5000  # milliseconds
    wavegen.timeout = 5000
   
    #initialize scope
    scope.write(":CHANNEL1:DISPLAY ON")
    scope.write(":AUToset")
    scope.write(":CHANNEL1:COUPLING AC")

    #init wavegen
    wavegen.write(":SOURce1:FUNCtion:SHAPe SIN")
    wavegen.write(":SOURce1:VOLTage:AMPLitude 2.0")
    wavegen.write(":SOURce1:VOLTage:OFFSet 0")
    wavegen.write(":OUTPut1:STATe OFF")

    # Frequency sweep parameters
    start_freq = 1      # 1 Hz
    stop_freq = 20000   # 20 kHz
    points = 20

    frequencies = np.logspace(np.log10(start_freq), np.log10(stop_freq), points)
    print(f"Starting point-by-point sweep from {start_freq} Hz to {stop_freq} Hz with {points} points")

    amplitudes = []

    # Perform point-by-point sweep
    for i, freq in enumerate(frequencies):
        print(f"Testing at {freq}")
        # Set frequency
        # Turn on Wave Gen output
        wavegen.write(f":SOURce1:FREQuency:FIXed {freq}")
        wavegen.write(":OUTPut1:STATe ON")

        time.sleep(0.5)  # Allow settling time
        
        # Take measurement
        scope.write(":AUToset")
        time.sleep(0.5)
        
        try:
            measurement = scope.query(':MEASure:VAMP?')
            amp_value = float(measurement.strip())
            amplitudes.append(amp_value)
        except Exception as e:
            print(f"Error at {freq} Hz: {e}")
            amplitudes.append(0)

    # Close the connection
    scope.close()
    wavegen.close()
  
except pyvisa.Error as e:
   print(f"Error: {e}")
