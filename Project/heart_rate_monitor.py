from machine import Pin, I2C, ADC
from fifo import Fifo
from led import Led
import time
from piotimer import Piotimer
import micropython
from ssd1306 import SSD1306_I2C
import hardware
import PPG_signal as PPG
#from machine import Pin, I2C
#from ssd1306 import SSD1306_I2C




def run():
    SAMPLE_PERIOD_S = 0.004   # 250 Hz sampling: 1 sample every 4 ms
    WAIT_WINDOW = 1000        # number of samples used to calculate the threshold
    THRESHOLD_UPDATE = 250    # recalculate the threshold every this many samples
    MIN_PEAK_GAP = 75        # ignore peaks closer than 75 samples (0.3 s, about 200 BPM max)
    REQUIRED_HR_VALUES = 20   # the program must output at least this many heart rate values
    PPI_WINDOW = 100          # keep only the most recent intervals
    LED_PIN = 22              # external LED
    LED_ON_SAMPLES = 25       # keep the LED on for 25 samples (100 ms at 250 Hz)
    
    indicator = Led(LED_PIN)
    sensor = hardware.HR_sensor(26)
    #button setup
    button = Pin(12, mode = Pin.IN, pull = Pin.PULL_UP)
    my_button = hardware.Button_handler()
    button.irq(handler = my_button.handler, trigger = Pin.IRQ_FALLING, hard = True)
    
    value = 0
    window = []                 # recent samples, used for the threshold only
    threshold = None
    sample_index = 0            # position in the recording, counted from the start
    previous_value = None
    max_value = 0
    min_value = 0
    last_peak_index = None
    last_peak_time = None
    interval_samples = []       # recent gaps between beats, in samples
    interval_times = [] 		# recent gaps between beats, in seconds
    heart_rate = 0
    heart_rates = []            # one heart rate value per detected beat (after the first)
    led_off_index = None        # sample index at which the LED should turn off
    updatePPG = False
    
    def calculate_threshold(values):
        max_value = max(values)
        min_value = min(values)
        return ((max_value + min_value) / 2) + (max_value - min_value) * 0.2, max_value, min_value
    
    PPG.calibrating()

    while True:
        while sensor.fifo.has_data():
            value = sensor.fifo.get()
            
            window.append(value)

            if len(window) == WAIT_WINDOW:
                threshold, max_value, min_value = calculate_threshold(window)
                window.clear()
                updatePPG = True
                
            # A beat is a rising crossing of the threshold.
            # Crossings closer than MIN_PEAK_GAP to the previous beat are ignored.
            if threshold is not None and previous_value is not None:
                if previous_value < threshold and value >= threshold:
                    if last_peak_index is None or sample_index - last_peak_index >= MIN_PEAK_GAP:
                        peak_time = sample_index * SAMPLE_PERIOD_S

                        indicator.on()
                        led_off_index = sample_index + LED_ON_SAMPLES

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

                        last_peak_index = sample_index
                        last_peak_time = peak_time

            # Turn the LED off once its time is up
            if led_off_index is not None and sample_index >= led_off_index:
                indicator.off()
                led_off_index = None

            sample_index += 1
        
        #Update the PPG signal
        if updatePPG:
            PPG.run(value, previous_value, max_value, min_value, heart_rate)
        
        #Button pressing logic: stops the function
        if my_button.fifo.has_data():
            my_button.fifo.get()
            if updatePPG:
                while sensor.fifo.has_data():
                    value = sensor.fifo.get()
                break
            
        frequency = None
        if len(interval_times) > 0:
            mean_period = sum(interval_times) / len(interval_times)
            frequency = 1 / mean_period
            
        previous_value = value