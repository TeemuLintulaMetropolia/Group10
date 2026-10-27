from filefifo import Filefifo

fifo = Filefifo(10, name = 'sinewave_250Hz_03.txt')
y1 = 0
k1 = 0
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
    print(k)
    return k

for i in range(100):
    if fifo.has_data():
        data = fifo.get()
    
    if i > 0:
        k = calculateSlop(i - 1, i, y1, data)
        if (k1 < 0 and k > 0) or (k1 > 0 and k < 0):
            #We found the peak
            peak = Sample(data, i * 0.004)
            peaks.append(peak.data())
        k1 = k
    y1 = data
    
print("Peaks:", peaks)

