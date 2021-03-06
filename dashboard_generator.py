# dashboard_generator.py

import math
import os
import re
from datetime import datetime

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#Referencing csv file hub
data_location = os.path.join(os.path.dirname(__file__), "data")

from os import listdir
from os.path import isfile, join

files = [f for f in listdir(data_location) if isfile(join(data_location, f))]

#File selection process
while True:
    file_name = input("Please input file name: ")
    if [p for p in files if p == file_name]:
        break
    else:
        print("Apologies, this file does not exist. Please enter another selection.")

parts = re.split('-|\.',file_name)
str_date = parts[1]

#Printing Formatted Date
report_date = datetime.strptime(str_date, "%Y%m")
formatted_date = report_date.strftime("%B %Y")

# USD Formatting Function

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)  # > $12,000.71

csv_filepath = os.path.join(os.path.dirname(__file__), "data", str(file_name))

csv_filename = file_name
csv_data = pd.read_csv(csv_filepath)

# Monthly Sales Total

monthly_total = csv_data["sales price"].sum()

#Top Sellers List
#https://codereview.stackexchange.com/questions/65031/creating-a-list-containing-the-rank-of-the-elements-in-the-original-list

product_totals = csv_data.groupby(["product"]).sum()

product_totals = product_totals.sort_values("sales price", ascending=False)

top_products = []
rank = 1
for i, row in product_totals.iterrows():
    x = {"rank": rank, "name": row.name, "monthly_sales": row["sales price"]}
    top_products.append(x)
    rank = rank + 1

#Sales Info Output

print("-----------------------")
print("CRUNCHING THE DATA...")

print("-----------------------")
print("MONTH: " + str(formatted_date))

print("-----------------------")
print(f"TOTAL MONTHLY SALES: {to_usd(monthly_total)}")

print("-----------------------")
print("TOP SELLING PRODUCTS:")

#enter top products code generating list here

for x in top_products:
    print("  " + str(x["rank"]) + ") " + x["name"] +
          ": " + to_usd(x["monthly_sales"]))

print("-----------------------")
print("VISUALIZING THE DATA...")

#Data Visualization
#https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/barh.html
#https://stackoverflow.com/questions/9626298/matplotlib-chart-creating-horizontal-bar-chart

# Graph definitions w/ matplotlib
products = list(product_totals.index)
sales = list(round(product_totals['sales price'],2))
y_pos = np.arange(len(products))
x_lab = [f"${x:,.2f}" for x in range(0, (round(math.ceil(sales[0] / 1000)) * 1000) + 1000, 1000)]

#Graph Build
#https://365datascience.com/bar-chart-python-matplotlib/

fig, ax = plt.subplots()

ax.barh(y_pos, sales, xerr=0, align='center', color = 'midnightblue')
ax.set_yticks(y_pos)
ax.set_yticklabels(products)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('In-the-Month Sales (USD)', fontweight = 'bold')
ax.set_ylabel('Products', fontweight = 'bold')
ax.set_title('Top-Selling Products ' + '(' + str(formatted_date) + ')', fontweight = 'bold')

for i, monthly_sales in enumerate(sales):
    if monthly_sales > 1000:
        val = f"${monthly_sales:,.2f}"
        ax.text(monthly_sales - 600, i + .1, val, color = 'white', fontweight = 'bold')
    else:
        val = f"${monthly_sales:,.2f}"
        ax.text(monthly_sales + 3, i + .1, val, color = 'black', fontweight = 'bold')

plt.show()
