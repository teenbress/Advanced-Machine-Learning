# -*- coding: utf-8 -*-
"""
week4 Data Visualization

Created on Wed Nov 27 20:22:33 2019

@author: Qiao Yu
"""
spark.sql("SELECT * FROM washingflat").show()

'''
result = spark.sql("select voltage from washingflat where voltage is not null")
[Row(voltage=226),
 Row(voltage=231),
 Row(voltage=233)
]
'''
result = spark.sql("select voltage from washingflat where voltage is not null")
result.rdd.map(lambda row: row.voltage)
# [226, 231, 233...]
result_array = result.rdd.map(lambda row: row.voltage).sample(False, 0.1).collect()
result_array
# [237,
#  232,
#  226, ...
#]

%matplotlib inline
# The code above means display all plots created by matplotlib as images under the cell;

import matplotlib.pyplot as plt
plt.boxplot(resuly_array)
plt.show()

# time series data contain timestamps;

result = spark.sql("select voltage, ts from washingflast where voltage is not null order by ts asc")
result_rdd = result.rdd.sample(False, 0.1).map(lambda row:(row.ts, row.voltage))
result_array_ts = result_rdd.map(lambda (ts, voltage): ts).collect()
result_array_voltage = result_rdd.map(lambda (ts, voltage): voltage).collect()
# plot 
plt.plot(result_array_ts, result_array_voltage)
plt.xlabel("time")
plt.ylabel("voltage")
plt.show()

# scatter plot
# Individual data points addressed by 2 or 3 dimensions
# Classification boundaries
# clusters
# Anomalies 
result_df = spark.sql("select hardness, temperature, flowrate from washingflat where hardness is not null and temperature is not null")
result_rdd = result_df.rdd.sample(False, 0.1).map(lambda row: (row.hardness, row.temperature, row.flowrate))
result_array_hardness = result_df.rdd.map(lambda (hardness, temperature, flowrate): hardness).collect()
result_array_temperature = result_df.rdd.map(lambda (hardness, temperature, flowrate): temperature).collect()
result_array_flowrate = result_df.rdd.map(lambda (hardness, temperature, flowrate): flowrate).collect()

from mpl_toolkits.mplot3d import Axes3D

fig = plt.figture()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(result_array_hardness, result_array_temperature,result_array_flowrate, c ='r', marker = 'o')

ax.set_xlabel('hardness')
ax.set_ylabel('temperature')
ax.set_zlabel('flowrate')
plt.show()

# Histograms
# Get idea of the distribution of values
# Find regions of high and low value concerntration
plt.hist(result_array_hardness)
plt.show()

























