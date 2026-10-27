from filefifo import Filefifo

fifo = Filefifo(10, name = 'sinewave_250Hz_03.txt', repeat = False)
y1 = 0
kprev = 0
peaks = []
class Sample:
    def __init__ (self, value, time):
        self.value = value
        self.time = time
    def data(self):
        data = f"{str(self.value)}, {str(self.time)}s"
        return data

def calculateSlop(x1, x2, y1, y2):
    k = (y2 - y1)/(x2 - x1)
    return k

def calculatePPI(peaks):
    PPI = []
    PPI_sum = 0
    i = 0
    for peak in peaks:
        if i == 0:
            i += 1
        else:
            timebet = peak.time - peaks[i - 1].time
            print(f"This is PPI:{timebet}")
            PPI.append(timebet)
            PPI_sum += timebet
            i += 1

i = 0
while True:
    try:
        data = fifo.get()
    except:
        break
    i += 1
    if i > 0:
        k = calculateSlop(i - 1, i, y1, data)
        if (kprev > 0 and k < 0):
            #We found the peak
            peak = Sample(y1, i * 0.004)
            peaks.append(peak)
        kprev = k
    y1 = data

print("Peaks:", peaks)

calculatePPI(peaks)