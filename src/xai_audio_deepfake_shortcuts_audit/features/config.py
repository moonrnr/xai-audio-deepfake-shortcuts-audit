"""Settings of the feature table: every number the features depend on.

extract_file_features takes these values as its defaults and passes them to the measure_*
functions, which have no defaults of their own. To compute the features with other settings
for one run, pass other values to extract_file_features instead of changing this file.
"""

# sample rate in Hz at which every recording is decoded and measured; all datasets of the
# project are stored at 16 kHz (notebooks 01-05)
SAMPLE_RATE_HZ = 16000

# silence threshold: at the start and the end of a recording, everything below this level
# (in dB relative to the loudest part of the recording) counts as silence
THRESHOLD_DB = -30.0

# frames used by the silence and the bandwidth: length and step in milliseconds (400 and 160
# samples at 16 kHz)
FRAME_MS = 25.0
HOP_MS = 10.0

# loudness (measure_loudness): dBFS value used for digital silence instead of minus infinity
DB_FLOOR = -120.0

# bandwidth (measure_bandwidth): how many dB below its maximum the average spectrum of the
# recording must fall to count as cut off
DROP_DB = 50.0
