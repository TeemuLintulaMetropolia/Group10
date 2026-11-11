    def calculatePPI(peaks, prev_HR):
        PPI = []
        PPI_sum = 0
        current_peak = peaks[-1]
        previous_peak = peaks[-2]
        samplediff = current_peak.index - previous_peak.index
        timediff = current_peak.time - previous_peak.time
        samplediffs.append(samplediff)
        timediffs.append(timediff)
        print(f"This is PPI:{timediff}   samples between:{samplediff}")
        PPI.append(timediff)
        PPI_sum += timediff
        meanPPI = PPI_sum/len(PPI)
        #print("mean PPI:", meanPPI)
        
        frequency = 1/meanPPI
        #print(f"frequency: {frequency}Hz")
        
        cur_HR = frequency * 60
        prev_HR = prev_HR
        if cur_HR != prev_HR:
            print(f"Heart rate: {round(cur_HR)}BPM")
            prev_HR = cur_HR
            #print(f"This is the Peak: {current_peak.value}\nThis is the time the peak happened: {current_peak.time}\nThis the sample number: {current_peak.index}")
            print()
            print("---------------------------------------------------")
            print()
        
        
        return frequency
while True:
        try:
            value = fifo.get()
        except:
            break
        samples.append(data)
        total_samples += 1
        if len(samples) > wait_window:
            samples.pop(0)
        if len(samples) >= wait_window:
            threshold = calculate_threshold(samples)
            current = samples[-1]
            previous = samples[-2]
            if previous < threshold and current > threshold:
                if len(peaks) == 0 or (total_samples - peaks[-1].index) > min_peak_gap:
                    print("peak:", current)
                    peak_time = total_samples * 0.004
                    peak_index = total_samples
                    peaks.append(Sample(current, peak_time, peak_index))
        if len(peaks) >= ppi_window:
            frequency = calculatePPI(peaks,prev_HR)
