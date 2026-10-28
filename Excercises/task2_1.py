from filefifo import Filefifo
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
def run_program():
    fifo = Filefifo(10, name = 'sinewave_250Hz_01.txt', repeat = False)
    y1 = 0
    kprev = 0
    peaks = []

    class Sample:
        def __init__ (self, value, time, index):
            self.value = value
            self.time = time
            self.index = index

    def calculateSlop(x1, x2, y1, y2):
        k = (y2 - y1)/(x2 - x1)
        return k

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


    i = 0
    while True:
        try:
            data = fifo.get()
        except:
            break
        if i > 0:
            k = calculateSlop(i - 1, i, y1, data)
            if (kprev >= 0 and k < 0):
                #We found the peak
                peak = Sample(y1, (i -1) * 0.004, i -1)
                peaks.append(peak)
                print("peak:", str(peak.value), str(peak.time) + "s")
            kprev = k
        y1 = data
        i += 1

    print()
    print("---------------------------------------------------")
    print()
    frequency = calculatePPI(peaks)




    i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
    oled = SSD1306_I2C(128, 64, i2c)

    y = 0
    for i in range(4):
        i += 1
        oled.text(f"{i})int:{int(samplediffs[i -1])}-{int(timediffs[i -1]*1000)}Ms", 0, y, 1)
        y += 8

    oled.text(f"freq: {frequency:.4f}Hz",0,y,1)
    oled.show()