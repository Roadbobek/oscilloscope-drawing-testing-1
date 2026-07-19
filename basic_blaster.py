import sounddevice as sd
import numpy as np
import time

# audio parameters
SAMPLE_RATE = 44100
BASE_FREQ = 130  # the base frequency of the shape (affects audio pitch)
SPEED_MULTIPLIER = 1.0
phase_accumulator = 0.0


def audio_callback(outdata, frames, time_info, status):
    global phase_accumulator
    if status:
        print(status)

    # create a continuous timeline array for this block of audio samples
    t = (phase_accumulator + np.arange(frames)) / SAMPLE_RATE

    # get the current system time to drive our visual animation values
    current_time = time.time()

    # mathematical vector generation (x and y coordinates)
    # left channel = x axis (horizontal)
    # right channel = y axis (vertical)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # rotating 3:4 woven ribbon

    x = 0.7 * np.sin(3 * 2 * np.pi * BASE_FREQ * t)
    y = 0.7 * np.cos(4 * 2 * np.pi * BASE_FREQ * t + (current_time * SPEED_MULTIPLIER))

    #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #

    # x = 0.7 * np.sin(3 * BASE_FREQ * t)
    # y = 0.7 * np.cos(4 * BASE_FREQ * t + current_time)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # feed the vectors directly into the stereo soundcard buffer
    outdata[:, 0] = x  # x to left channel (0)
    outdata[:, 1] = y  # y to right Channel (1)

    # keep the phase seamless across continuous audio blocks to prevent crackling
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