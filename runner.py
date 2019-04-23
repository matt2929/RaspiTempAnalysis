import matplotlib.pyplot as plt
import time
import numpy as np
from graphics import *


def main():
    temp_list = get_data('/Users/matt2929/Pictures/RaspiPull/log.txt')
    temp_list, time_list = reject_outliers(temp_list)
    temp_list, time_list = consolidate(temp_list, 50)
    print(temp_list)
    draw_canvas(time_list, temp_list)


def draw_canvas(list_x, list_y):
    win = GraphWin("My Circle", 1000.0, 250.0)
    max_x = list_max(list_x)
    min_y = list_min(list_y)
    max_y = list_max(list_y)
    for i in range(len(list_x)):
        c = Circle(Point(*scale_xy(list_x[i], list_y[i], min_y, max_x, max_y, 1000.0, 250.0)), 1)
        c.draw(win)


def list_max(data):
    max_val = 0
    for i in data:
        if i > max_val:
            max_val = i
    return max_val

def list_min(data):
    min_val = 100000
    for i in data:
        if i < min_val:
            min_val = i
    return min_val

def scale_xy(x, y, min_y, max_x, max_y, bound_x, bound_y):
    return (x * bound_x) / max_x, ((y-min_y) * bound_y) / (max_y - min_y)



def consolidate(data, batch_size):
    output_x = []
    output_y = []
    count = 0
    sum_batch = 0
    for i in range(len(data)):
        sum_batch += data[i]
        if i % batch_size == 0 and i != 0:
            output_x = output_x + [sum_batch / batch_size]
            count += 1
            output_y = output_y + [count]
            sum_batch = 0
    return output_x, output_y


def median(data):
    if len(data) % 2 == 0:
        return (data[(len(data) // 2)] + data[(len(data) // 2) + 1]) / 2
    else:
        return data[(len(data) // 2)]


def reject_outliers(data):
    time_list = []
    output = []
    data_sort = data[:]
    list.sort(data_sort)
    half_way = (len(data_sort) // 2)
    first_half = data_sort[:half_way]
    second_half = data_sort[half_way:]
    first_quart = median(first_half)
    third_quart = median(second_half)
    interquartile_range = (third_quart - first_quart) * 3
    first_quart = first_quart - interquartile_range
    third_quart = third_quart + interquartile_range
    count = 1
    for i in data:
        if first_quart <= i <= third_quart:
            output = output + [i]
            time_list = time_list + [count]
        count += 1
    return output, time_list


def get_data(path):
    fp = open(path, 'r')
    temp_list = []
    line = fp.readline()
    while line:
        if "temp " in line:
            time_list = line.split(" ")[1].split("'")[0]
            temp_list = temp_list + [float(time_list)]
        line = fp.readline()
    fp.close()
    return temp_list

main()
