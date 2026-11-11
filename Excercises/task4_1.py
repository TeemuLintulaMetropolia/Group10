from filefifo import Filefifo
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time

SAMPLE_PERIOD_S = 0.004  # 250 Hz sampling: 1 sample every 4 ms


def run_program():
    samplediffs = []
    timediffs = []
    sample_fifo = Filefifo(10, name='hr_capture02_250Hz.txt', repeat=False)
    all_samples = []
    peaks = []
    previous_value = 0
    previous_slope = 0

    class Sample:
        def __init__(self, value, time, index):
            self.value = value
            self.time = time
            self.index = index

    def calculate_slope(x1, x2, y1, y2):
        return (y2 - y1) / (x2 - x1)

    def calculate_threshold(samples):
        max_value = max(samples)
        min_value = min(samples)
        threshold = ((max_value + min_value) / 2) + min_value * 0.2
        print("threshold:", threshold)
        return threshold

    def calculate_frequency_from_peaks(peaks):
        i = 0
        for peak in peaks:
            if i == 0:
                i += 1
            else:
                sample_gap = peak.index - peaks[i - 1].index
                time_gap = peak.time - peaks[i - 1].time
                samplediffs.append(sample_gap)
                timediffs.append(time_gap)
                print(f"This is PPI:{time_gap}   samples between:{sample_gap}")
                i += 1

        mean_period = sum(timediffs) / len(timediffs)
        print("mean PPI:", mean_period)

        frequency = 1 / mean_period
        print(f"frequency: {frequency}Hz")

        heart_rate = frequency * 60
        print(f"Heart rate: {heart_rate}BPM")

        return frequency

    # Read every sample from the file
    while True:
        try:
            all_samples.append(sample_fifo.get())
        except:
            break

    # Calculate the threshold once, from all the samples
    threshold = calculate_threshold(all_samples)

    # Detect peaks in a second pass
    # (a peak is where the slope changes from positive or zero to negative,
    # and only while the signal is above the threshold)
    for sample_index in range(1, len(all_samples)):
        value = all_samples[sample_index]
        previous_value = all_samples[sample_index - 1]
        if previous_value >= threshold:
            slope = calculate_slope(sample_index - 1, sample_index, previous_value, value)
            if previous_slope >= 0 and slope < 0:
                peak = Sample(previous_value, (sample_index - 1) * SAMPLE_PERIOD_S, sample_index - 1)
                peaks.append(peak)
                print("peak:", str(peak.value), str(peak.time) + "s")
            previous_slope = slope

    print()
    print("---------------------------------------------------")
    print()

    frequency = calculate_frequency_from_peaks(peaks)

    # Display setup: draw the summary, then call show() once
    i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
    oled = SSD1306_I2C(128, 64, i2c)
    oled.fill(0)

    y = 0
    for i in range(min(4, len(samplediffs))):
        oled.text(f"{i + 1})int:{int(samplediffs[i])}-{int(timediffs[i] * 1000)}Ms", 0, y, 1)
        y += 8

    if frequency is not None:
        oled.text(f"freq: {frequency:.4f}Hz", 0, y, 1)
    oled.show()
    print("Display updated")

    # Keep the summary on screen for a few seconds before the graph starts
    time.sleep(5)

    min_value = min(all_samples)
    max_value = max(all_samples)
    value_range = max_value - min_value

    print(all_samples)
    print(min_value)
    print(max_value)

    display_index = 0
    while True:
        try:
            percent = int(((all_samples[display_index] - min_value) / value_range) * 100)
            bar_length = int(percent * 1.04)  # 1.04 scales 100% to the 104 remaining pixels

            # The trailing space clears leftover characters when the number gets shorter
            if percent != 100:
                label = f"{percent} "
            else:
                label = str(percent)

            if display_index >= 8:
                # Screen is full: scroll up one text row and draw the new line at the bottom
                oled.scroll(0, 8)
                oled.fill_rect(0, 0, 128, 8, 0)
                oled.text(label, 0, 0, 1)
                oled.fill_rect(24, 0, bar_length, 4, 1)
            else:
                row_y = 56 - display_index * 8
                oled.text(label, 0, row_y, 1)
                oled.fill_rect(24, row_y, bar_length, 4, 1)

            display_index += 1
            oled.show()
        except IndexError:
            # Reached the end of the samples
            break
        except Exception as e:
            print("Display error:", e)
            break


run_program()
