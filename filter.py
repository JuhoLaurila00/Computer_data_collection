import streamlit as st
import pandas
import datetime
import numpy
import plotly.graph_objects as go
import glob

time_step = 5
rolling_average = 1

dataframes = []
for file in glob.iglob('*.csv'):
    dataframes.append(pandas.read_csv(file))

options = st.container(border=False)
option_cols = options.columns(len(dataframes))
checks = pandas.DataFrame(columns=['dataframe_id', 'device', 'col_name', 'enabled'])
device_id = {0:'CPU', 1:'GPU'}

st.title('Computer data')
header = st.container(border=False)
head_cols = header.columns(2)

time_opts = head_cols[1].container(border=False)
time_cols = time_opts.columns(2)
start_date = time_cols[0].date_input('Start date')
start_h = time_cols[1].time_input('Start time')
end_date = time_cols[0].date_input('End date')
end_h = time_cols[1].time_input('End time')
start_time = datetime.datetime.combine(start_date, start_h).timestamp()
end_time = datetime.datetime.combine(end_date, end_h).timestamp()
time_range = numpy.linspace(start_time,end_time, num=int((end_time-start_time)/time_step))
datetime_range = pandas.to_datetime(time_range+10800, unit='s') #10800 for timezone offset (caveman strategy)

#GET DATA FROM DATABASE BASED ON GIVEN START AND END TIME

components = []
for index, df in enumerate(dataframes):
    components.append(device_id[index])
devices = head_cols[0].tabs(components)
for index, (device, df) in enumerate(zip(devices, dataframes)):
    with device:
        for header in df.columns:
            if header != 'time':
                check = st.checkbox(f'{device_id[index]} - {header}', key=f'{device_id[index]}{header}')
                checks.loc[len(checks)] = [index, device_id[index], header, check]
            
with st.sidebar:
    st.write('Options')
    rolling_average = st.slider('Smoothing',  min_value=1, max_value=200)
    yrange_opts = st.container(border=False)
    yrange_cols = yrange_opts.columns(2)
    yr_start = yrange_cols[0].slider('Y-range start',  min_value=0, max_value=100, step=5)
    yr_stop = yrange_cols[1].slider('Y-range stop',  min_value=0, max_value=100, step=5, value=100)

fig = go.Figure()
for index, row in checks.loc[checks['enabled']==True].iterrows():
    data = dataframes[checks.loc[index, 'dataframe_id']]
    col = checks.loc[index, 'col_name']
    dev = checks.loc[index, 'device']
    data[col] = data[col].rolling(window=rolling_average).mean()
    interp_data = numpy.interp(time_range, data['time'], data[col])
    interp_data = numpy.nan_to_num(interp_data)
    fig.add_trace(go.Scatter(x=datetime_range, y=interp_data, mode='lines', name=f'{dev}-{col}'))
yrange = [yr_start,yr_stop]
fig.update_layout(
    xaxis=dict(range=[datetime_range[0],datetime_range[-1]], showgrid=True),
    yaxis=dict(range=yrange, showgrid=True, dtick=10, minor=dict(dtick=5, showgrid=True, griddash='3,2,3,2')),
    showlegend=True,
    legend=dict(y=1.2, orientation="h")
    )
st.plotly_chart(fig, use_container_width=True)