from math import sqrt


def calculate_mean_PPI(ppi_list):
    mean_PPI = sum(ppi_list)/len(ppi_list)
    return mean_PPI
def calculate_mean_HR(mean_PPI):
    mean_HR = (60/mean_PPI) * 1000
    return mean_HR
def calculate_SDNN(mean_PPI, ppi_list):
    prepare_for_sum = []
    for ppi in ppi_list:
        prepare_for_sum.append((ppi-mean_PPI)**2)
    sdnn = sqrt(sum(prepare_for_sum)/(len(ppi_list)-1))
    return sdnn
def calculate_RMSSD(ppi_list):
    prepare_for_sum = []
    for index in range(len(ppi_list)-1):
        prepare_for_sum.append((ppi_list[index+1] - ppi_list[index])**2)
    rmsdd = sqrt(sum(prepare_for_sum)/(len(ppi_list)-1))
    return rmsdd


