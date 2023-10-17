import numpy as np
from rtlsdr import RtlSdr
import pyModeS as pms

# Set the RTL-SDR device parameters
center_freq = 1090e6
sample_rate = 2.4e6
gain = 40

# Create an RtlSdr object
sdr = RtlSdr()

# Set the sample rate, center frequency, and gain
sdr.sample_rate = sample_rate
sdr.center_freq = center_freq
sdr.gain = gain

# Capture samples
samples = sdr.read_samples(256 * 1024)

# Close the RTL-SDR device
sdr.close()

# Demodulate the samples
iq_data = np.array(samples).astype("complex64")
iq_data /= 2 ** 15
iq_data = iq_data.reshape((-1, 2))
iq_data = iq_data[:, 0] + 1j * iq_data[:, 1]

# Decode ADS-B messages
messages = []
for i in range(len(iq_data)):
    bits = pms.deinterleave(pms.decode_burst(iq_data[i]))
    msg = pms.adsb.icao_address(bits)
    if msg is not None:
        messages.append(msg)

# Print the decoded messages
for msg in messages:
    print(msg)
