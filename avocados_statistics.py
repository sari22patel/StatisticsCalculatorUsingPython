#Name: Sarita Patel
#Date:7th oct 2018

from statistics import *
import csv
from math import sqrt, ceil, floor
import sys
file_path = "data/avocado.csv"

def read_data(path, var):
    """
    This function takes input filepath and variable name and returns a list of values for the variable in the file.

    Parameters:
    path = file path
    var = variable name
    """
    avocados_dict = {}
    csv_reader = csv.reader(open(path)) # Use csv.reader function to iterate over the csv file
    header = next(csv_reader) #Getting the column header in a list

    data_rows = []
    for row in csv_reader:
        data_rows.append(row) # Reading data rows in a list

    i = 0
    for h in header:
        avocados_dict[h] = [r[i] for r in data_rows] # storing all values for a variable in a list and assigning to the key for this variable in the dictionary
        i+=1

    variable_values = list(map(float, avocados_dict[var])) #extracting the list of values for the variable
    return variable_values

def readAndComputeMean_SM(variable_name):
    """
    This function takes input a variable name and returns the mean for values of this variable from the file. The mean is computed using the statistics module.

    Parameters:
    var = variable name
    """
    variable_values = read_data(file_path, variable_name)
    return round(mean(variable_values), 2)

def readAndComputeSD_SM(variable_name):
    """
    This function takes input a variable name and returns the standard deviation for values of this variable from the file. The standard deviation is computed using the statistics module.

    Parameters:
    var = variable name
    """
    variable_values = read_data(file_path, variable_name)
    return round(stdev(variable_values), 2)

def readAndComputeMedian_SM(variable_name):
    """
    This function takes input a variable name and returns the median value of this variable from the file. The median is computed using the statistics module.

    Parameters:
    var = variable name
    """
    variable_values = read_data(file_path, variable_name)
    return round(median(variable_values), 2)

def readAndComputeMean_HG(variable_name):
    """
    This function takes input a variable name and returns the mean for values of this variable from the file. The mean is computed using the home grown logic.

    Parameters:
    var = variable name
    """
    variable_values = read_data(file_path, variable_name)
    return round(sum(variable_values)/len(variable_values), 2)

def readAndComputeSD_HG(variable_name):
    """
    This function takes input a variable name and returns the standard deviation for values of this variable from the file. The standard deviation is computed using the home grown logic.

    Parameters:
    var = variable name
    """
    variable_values = read_data(file_path, variable_name)
    variable_mean = readAndComputeMean_HG(variable_name)
    return round(sqrt(sum(map(lambda x: (x-variable_mean)**2, variable_values))/(len(variable_values)-1)), 2)

def readAndComputeMedian_HG(variable_name):
    """
    This function takes input a variable name and returns the median value of this variable from the file. The median is computed using the home grown logic.

    Parameters:
    var = variable name
    """
    variable_values = read_data(file_path, variable_name)
    sort_var_values = list(sorted(variable_values))
    len_list = len(sort_var_values)
    if len_list%2 == 1:
        return sort_var_values[int(len_list/2)]
    else:
        return round(((sort_var_values[int(len_list/2)-1] + sort_var_values[int(len_list/2)])/2), 2)

def readAndComputeMean_MML(variable_name):
    """
    This function takes input a variable name and returns the mean for values of this variable from the file. The mean is computed using the memoryless logic.

    Parameters:
    var = variable name
    """
    csv_reader = csv.reader(open(file_path))
    header = next(csv_reader)
    var_index = header.index(variable_name)
    len_var_val = 0
    sum=0
    for row in csv_reader:
        sum+=float(row[var_index])
        len_var_val+=1

    return round((sum/len_var_val),2)

def readAndComputeSD_MML(variable_name):
    """
    This function takes input a variable name and returns the standard deviation for values of this variable from the file. The standard deviation is computed using the memoryless logic.

    Parameters:
    var = variable name
    """
    var_mean = readAndComputeMean_MML(variable_name)
    csv_reader = csv.reader(open(file_path))
    header = next(csv_reader)
    var_index = header.index(variable_name)
    len_var_val = 0
    sum=0
    for row in csv_reader:
        sum+=(float(row[var_index])-var_mean)**2
        len_var_val+=1

    return round(sqrt(sum/(len_var_val-1)), 2)

def readAndComputeMedian_MML(variable_name):
    """
    This function takes input a variable name and returns the median value of this variable from the file. The median is computed using the memoryless logic.

    Parameters:
    var = variable name
    """
    f = open(file_path)
    csv_reader = csv.reader(f)
    sum_before_med_idx = 0
    header = next(csv_reader)
    var_index = header.index(variable_name)
    l = [0]*10
    min_val = sys.float_info.max
    max_val = sys.float_info.min
    for row in csv_reader:
        min_val=min(float(row[var_index]), min_val)
        max_val=max(float(row[var_index]), max_val)

    iterations = 0
    while(True):
        iterations+=1
        l = [0]*10
        bin = (max_val - min_val+ 1 )/10
        f.seek(0)
        next(csv_reader)
        for row in csv_reader:
            if max_val >= float(row[var_index]) >= min_val:
                bin_index = int((float(row[var_index])-min_val)/bin)
                if bin_index<0 or bin_index>=len(l):
                    print(bin_index, row[var_index], min_val, bin*10, int((float(row[var_index])-min_val)/bin)-1)
                l[bin_index]+=1
        if iterations == 1:
            median_pos = int((sum(l)+1)/2)
            even_flag = sum(l)%2==0

        median_index = 0
        for i in range(0, len(l)):
            if (sum(l[:(i+1)]) + sum_before_med_idx) >= median_pos:
                median_index = i
                break

        sum_before_med_idx += sum(l[:(median_index)])

        # if not even_flag and sum_before_med_idx==median_pos and l[median_index]!=1:
        #     median_index = median_index-1
        #     sum_before_med_idx -= l[median_index]

        print("Min={}, Max={}, median_pos={}, median_index={}, sum = {}, bin={}, list={}".format(min_val, max_val, median_pos, median_index, sum_before_med_idx, bin, l))

        max_val = ((median_index+1)*bin) + min_val
        min_val = ((median_index)*bin) + min_val

        if (sum_before_med_idx + l[median_index]) >= (median_pos-1):
            if l[median_index] == 1 and not even_flag:
                f.seek(0)
                next(csv_reader)
                for row in csv_reader:
                    if max_val >= float(row[var_index]) >= min_val:
                            return float(row[var_index])
            if l[median_index] == 1 and even_flag:
                f.seek(0)
                next(csv_reader)
                val1 = 0
                val2 = sys.float_info.min
                for row in csv_reader:
                    if max_val >= float(row[var_index]) >= min_val:
                            val1 = float(row[var_index])
                f.seek(0)
                next(csv_reader)
                prev_max_val = ((median_index)*bin) + min_val
                prev_min_val = ((median_index-1)*bin) + min_val
                for row in csv_reader:
                    if prev_max_val >= float(row[var_index]) >= prev_min_val:
                            if float(row[var_index]) > val2:
                                val2 = float(row[var_index])

                return round(((val1 + val2)/2),2)

            elif l[median_index] == 2 and even_flag:
                f.seek(0)
                next(csv_reader)
                total=0
                for row in csv_reader:
                    if max_val >= float(row[var_index]) >= min_val:
                        total+=float(row[var_index])
                return round(total/2, 2)

if __name__ == '__main__': # Code to test the results are equal across all techniques
    variable_name = "Total Volume"
    mean_SM = readAndComputeMean_SM(variable_name)
    sd_SM  = readAndComputeSD_SM(variable_name)
    median_SM  = readAndComputeMedian_SM(variable_name)
    print("Mean = {m} Standard Deviatin = {s} Median = {md}".format(m=mean_SM, s=sd_SM, md=median_SM))

    mean_HG = readAndComputeMean_HG(variable_name)
    sd_HG  = readAndComputeSD_HG(variable_name)
    median_HG = readAndComputeMedian_HG(variable_name)
    print("Mean = {m} Standard Deviatin = {s} Median = {md}".format(m=mean_HG, s=sd_HG, md=median_HG))

    mean_MML  = readAndComputeMean_MML(variable_name)
    sd_MML  = readAndComputeSD_MML(variable_name)
    median_MML = readAndComputeMedian_MML(variable_name)
    print("Mean = {m} Standard Deviatin = {s} Median = {md}".format(m=mean_MML, s=sd_MML, md=median_MML))

    print("Mean Test: {mt}, Standard Deviation: {sdt}, Median: {mdt}".format(mt=mean_SM==mean_HG==mean_MML, sdt=sd_SM==sd_HG==sd_MML, mdt=median_SM==median_HG==median_MML))
