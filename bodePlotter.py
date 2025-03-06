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

scope_address  = 'TCPIP0::192.168.2.2::INSTR'
wavegen_address = 'TCPIP0::192.168.2.3::INSTR'

try:
    scope = rm.open_resource(scope_address)
    wavegen = rm.open_resource(wavegen_address)

    # Set timeout
    scope.timeout = 5000  # milliseconds
    wavegen.timeout = 5000
   
    #initialize scope
    # INSERT COMMANDS TO INIT SCOPE


    #init wavegen
    # INSERT COMMANDS TO INIT WAVE GEN


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

        # Set frequency Turn on Wave Gen output
        # INSERT COMMANDS TO SET FREQUENCY AND TURN ON WAVE GEN


        time.sleep(1)  # Allow settling time
        
        # Readjust Scope display
        scope.write(":AUToset")
        time.sleep(1.5)
        
        #take measurement
        try:
            measurement = float() #INSERT SCOPE AMPLITUDE MEASUREMENT)
            amplitudes.append(measurement)
        except Exception as e:
            print(f"Error at {freq} Hz: {e}")
            amplitudes.append(0)

    # Close the connection
    scope.close()
    wavegen.close()
  
except pyvisa.Error as e:
   print(f"Error: {e}")
