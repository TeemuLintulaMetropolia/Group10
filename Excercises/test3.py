from filefifo import Filefifo
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

SAMPLE_PERIOD_S = 0.004   # 250 Hz sampling: 1 sample every 4 ms
WAIT_WINDOW = 1000        # wait this many samples before starting calculations
THRESHOLD_UPDATE = 250    # recalculate the threshold every this many samples
MIN_PEAK_GAP = 75         # ignore peaks closer than 75 samples
PPI_WINDOW = 100          # keep only the most recent intervals


def run_program():
    fifo = Filefifo(10, name='hr_capture01_250Hz.txt', repeat=False)

    window = []                  # recent samples, used for the threshold only
    threshold = None
    sample_index = 0
    previous_value = None
    last_peak_index = None
    last_peak_time = None
    interval_samples = []
    interval_times = []

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
            print("threshold:", threshold)

        if threshold is not None and previous_value is not None:
            if previous_value < threshold and value >= threshold:
                if last_peak_index is None or sample_index - last_peak_index >= MIN_PEAK_GAP:
                    peak_time = sample_index * SAMPLE_PERIOD_S
                    print("peak:", value, str(peak_time) + "s")

                    if last_peak_index is not None:
                        gap_samples = sample_index - last_peak_index
                        gap_time = peak_time - last_peak_time
                        interval_samples.append(gap_samples)
                        interval_times.append(gap_time)
                        print(f"This is PPI:{gap_time}   samples between:{gap_samples}")

                        if len(interval_times) > PPI_WINDOW:
                            interval_times.pop(0)
                            interval_samples.pop(0)

                    last_peak_index = sample_index
                    last_peak_time = peak_time

        previous_value = value
        sample_index += 1

    print()
    print("---------------------------------------------------")
    print()

    frequency = None
    if len(interval_times) > 0:
        mean_period = sum(interval_times) / len(interval_times)
        frequency = 1 / mean_period
        print("mean PPI:", mean_period)
        print(f"frequency: {frequency}Hz")
        print(f"Heart rate: {frequency * 60}BPM")
    else:
        print("Not enough peaks to calculate a frequency")

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
