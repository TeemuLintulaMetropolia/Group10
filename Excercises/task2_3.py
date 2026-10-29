from filefifo import Filefifo

fifo = Filefifo(10, name = 'sinewave_250Hz_01.txt', repeat = False)
peaks = []
samples = []
threshold = 0

def calculate_threshold(samples):
    maxval = 0
    minval = 0
    for sample in samples:
        if maxval == 0:
            maxval = sample
            minval = sample
        if maxval < sample:
            maxval = sample
        elif minval > sample:
            minval = sample
        
    threshold = (maxval - minval) * 1.25
    print("threshold:", threshold)
    return threshold
    
class Sample:
    def __init__ (self, value, time, index):
        self.value = value
        self.time = time
        self.index = index

samplediffs = []
timediffs = []
frequency = 0
def calculatePPI(peaks):
    PPI = []
    PPI_sum = 0
    i = 0
    for peak in peaks:
        if i == 0:
            i += 1
        else:
            samplediff = peak.index - peaks[i - 1].index
            timediff = peak.time - peaks[i - 1].time
            samplediffs.append(samplediff)
            timediffs.append(timediff)
            print(f"This is PPI:{timediff}   samples between:{samplediff}")
            PPI.append(timediff)
            PPI_sum += timediff
            i += 1
            
    meanPPI = PPI_sum/len(PPI)
    print("mean PPI:", meanPPI)
    
    frequency = 1/meanPPI
    print(f"frequency: {frequency}Hz")
    
    HR = frequency * 60
    print(f"Heart rate: {HR}BPM")
    
    return frequency



while True:
    try:
        data = fifo.get()
    except:
        break
        
    samples.append(data)
threshold = calculate_threshold(samples)
i = 0
for sample in samples:
    if i != 0 and samples[i -1] < threshold and sample > threshold:
        print("peak:", sample)
        peaks.append(Sample(sample, i * 0.004, i))
    i += 1
    
frequency = calculatePPI(peaks)
print()
print("---------------------------------------------------")
print()


# oled_refresh_rate_1_of_3
# Shows why calling show() for every pixel is slow (~30 ms each).

from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)
y = 0
for i in range(4):
    i += 1
    oled.text(f"{i})int:{int(samplediffs[i -1])}-{int(timediffs[i -1]*1000)}Ms", 0, y, 1)
    y += 8

oled.text(f"freq: {frequency:.4f}Hz",0,y,1)
oled.show()
