import streamlit as st
import pandas
import matplotlib.pyplot as plt
import datetime
import numpy

start_time = datetime.datetime(2024,4,22,18,47).timestamp()
end_time = datetime.datetime(2024,4,22,19,0).timestamp()
time_step = 5
rolling_average = 1
time_range = numpy.linspace(start_time,end_time, num=int((end_time-start_time)/time_step))

# fig, ax = plt.subplots()
data = pandas.read_csv('test_cpu.csv')
data['ccd_temp'] = data['ccd_temp'].rolling(window=rolling_average).mean()
interp_data = numpy.interp(time_range, data['time'], data['ccd_temp'])
time_range = pandas.to_datetime(time_range, unit='s')
interp_data = numpy.nan_to_num(interp_data)

# ax.plot(time_range, interp_data, label='unfiltered', linewidth=1)
# plt.ylim([0,100])
# plt.xlim([time_range[0],time_range[-1]])
# plt.legend()
# plt.grid('Both')
# plt.grid(which='minor', linewidth=0.4, linestyle='--')
# plt.minorticks_on()
# plt.savefig('filt.png', dpi=400)

st.title('Data')