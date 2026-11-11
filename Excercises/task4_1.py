from filefifo import Filefifo
#from machine import Pin, I2C
#from ssd1306 import SSD1306_I2C

SAMPLE_PERIOD_S = 0.004   # 250 Hz sampling: 1 sample every 4 ms
WAIT_WINDOW = 1000        # number of samples used to calculate the threshold
THRESHOLD_UPDATE = 250    # recalculate the threshold every this many samples
MIN_PEAK_GAP = 75         # ignore peaks closer than 75 samples (0.3 s, about 200 BPM max)
REQUIRED_HR_VALUES = 20   # the program must output at least this many heart rate values
PPI_WINDOW = 100          # keep only the most recent intervals


def run_program():
    fifo = Filefifo(10, name='hr_capture01_250Hz.txt', repeat=False)

    window = []                 # recent samples, used for the threshold only
    threshold = None
    sample_index = 0            # position in the recording, counted from the start
    previous_value = None
    last_peak_index = None
    last_peak_time = None
    interval_samples = []       # recent gaps between beats, in samples
    interval_times = []         # recent gaps between beats, in seconds
    heart_rates = []            # one heart rate value per detected beat (after the first)

    def calculate_threshold(values):
        max_value = max(values)
        min_value = min(values)
        return ((max_value + min_value) / 2) + (max_value - min_value) * 0.2

    while True:
        try:
            value = fifo.get()
        except:
            break

        window.append(value)
        if len(window) > WAIT_WINDOW:
            window.pop(0)

        if len(window) == WAIT_WINDOW and sample_index % THRESHOLD_UPDATE == 0:
            threshold = calculate_threshold(window)

        # A beat is a rising crossing of the threshold.
        # Crossings closer than MIN_PEAK_GAP to the previous beat are ignored.
        if threshold is not None and previous_value is not None:
            if previous_value < threshold and value >= threshold:
                if last_peak_index is None or sample_index - last_peak_index >= MIN_PEAK_GAP:
                    peak_time = sample_index * SAMPLE_PERIOD_S

                    if last_peak_index is not None:
                        gap_samples = sample_index - last_peak_index
                        gap_time = peak_time - last_peak_time
                        interval_samples.append(gap_samples)
                        interval_times.append(gap_time)

                        if len(interval_times) > PPI_WINDOW:
                            interval_times.pop(0)
                            interval_samples.pop(0)

                        heart_rate = 60 / gap_time
                        heart_rates.append(heart_rate)
                        print(f"Beat {len(heart_rates)}: time {peak_time:.3f}s   "
                              f"interval {gap_time:.3f}s   HR {heart_rate:.1f} BPM")

                    last_peak_index = sample_index
                    last_peak_time = peak_time

        previous_value = value
        sample_index += 1

    print()
    print("---------------------------------------------------")
    print()

    if len(heart_rates) < REQUIRED_HR_VALUES:
        print(f"Warning: only {len(heart_rates)} heart rate values were found. "
              f"At least {REQUIRED_HR_VALUES} are required.")
    else:
        print(f"Total heart rate values: {len(heart_rates)}")

    frequency = None
    if len(interval_times) > 0:
        mean_period = sum(interval_times) / len(interval_times)
        frequency = 1 / mean_period
        print(f"Mean interval: {mean_period:.3f}s")
        print(f"Mean frequency: {frequency:.3f}Hz")
        print(f"Mean heart rate: {frequency * 60:.1f} BPM")

    # OLED summary: the most recent intervals and the mean frequency
    i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
    oled = SSD1306_I2C(128, 64, i2c)
    oled.fill(0)

    y = 0
    recent_count = min(4, len(interval_times))
    for i in range(recent_count):
        index = len(interval_times) - recent_count + i
        oled.text(f"{i + 1})int:{int(interval_samples[index])}-{int(interval_times[index] * 1000)}Ms", 0, y, 1)
        y += 8

    if frequency is not None:
        oled.text(f"freq: {frequency:.4f}Hz", 0, y, 1)
    oled.show()
    print("Display updated")


run_program()
