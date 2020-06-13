# dashboard_generator.py

# URL is for input file "sales-201903.csv"

import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


while True:
    file_name = input("Please input file name: ")
    
    if file_name == "sales-201903.csv":
        break
    else:
        print("Apologies, this file does not exist. Please enter another selection.")


# USD Formatting Function

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)  # > $12,000.71

url = 'https://raw.githubusercontent.com/prof-rossetti/intro-to-python/master/data/monthly-sales/sales-201903.csv'

csv_filename = file_name
csv_data = pd.read_csv(url)

