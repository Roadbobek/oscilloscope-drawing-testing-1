import sounddevice as sd
import numpy as np
import time

# audio parameters
SAMPLE_RATE = 44100
BASE_FREQ = 150  # the base frequency of the shape (affects audio pitch)
phase_accumulator = 0.0


def audio_callback(outdata, frames, time_info, status):
    global phase_accumulator
    if status:
        print(status)

    # create a continuous timeline array for this block of audio samples
    t = (phase_accumulator + np.arange(frames)) / SAMPLE_RATE

    # get the current system time to drive our visual animation values
    current_time = time.time()

    # Theta represents the angle traveling around the shape
    theta = 2 * np.pi * BASE_FREQ * t

    # 1. The Famous Parametric Heart Equations
    # Cubing the sine pinches the sides inward to make the top cleavage and bottom point
    x = 16 * (np.sin(theta) ** 3)

    # Combining multiple cosine frequencies creates the distinct bottom V-shape
    y = 13 * np.cos(theta) - 5 * np.cos(2 * theta) - 2 * np.cos(3 * theta) - np.cos(4 * theta)

    # 2. Centering and Scaling
    # The math above yields large numbers (~16). We multiply by 0.04 to scale it
    # down to fit nicely inside the -1.0 to 1.0 audio boundary.
    x = x * 0.04
    y = (y + 2.5) * 0.04  # Adding 2.5 centers the heart vertically

    # 3. The Heartbeat Effect (Amplitude Modulation)
    # This creates a pulsing scale factor that mimics a resting heart rate
    pulse = 0.85 + 0.15 * np.sin(current_time * 4.5)

    # Send the final pulsing coordinates to the soundcard
    outdata[:, 0] = x * pulse  # Left Channel (X-axis)
    outdata[:, 1] = y * pulse  # Right Channel (Y-axis)

    phase_accumulator += frames


# open and run the live audio stream
try:
    with sd.OutputStream(channels=2, callback=audio_callback, samplerate=SAMPLE_RATE):
        print("Python is now broadcasting vector shapes.")
        print("1. Open your desktop Oscilloscope Simulator.")
        print("2. Set the input to your system's Loopback audio.")
        print("3. Press Ctrl+C in this terminal to stop...")
        while True:
            time.sleep(0.1)
except KeyboardInterrupt:
    print("\nStream safely terminated.")