import streamlit as st
import pandas
import datetime
import numpy
import plotly.graph_objects as go
import glob

start_time = datetime.datetime(2024,4,22,18,47).timestamp()
end_time = datetime.datetime(2024,4,22,19,0).timestamp()
time_step = 5
rolling_average = 1
time_range = numpy.linspace(start_time,end_time, num=int((end_time-start_time)/time_step))

dataframes = []
for file in glob.iglob('*.csv'):
    dataframes.append(pandas.read_csv(file))


options = st.container(border=True)
option_cols = options.columns(len(dataframes))
checks = pandas.DataFrame(columns=['dataframe_id', 'device', 'col_name', 'enabled'])
device_id = {0:'CPU', 1:'GPU'}
for index, (df, col) in enumerate(zip(dataframes, option_cols)):
    for header in df.columns:
        if header != 'time':
            check = col.checkbox(f'{device_id[index]} - {header}', key=f'{device_id[index]}{header}')
            checks.loc[len(checks)] = [index, device_id[index], header, check]

fig = go.Figure()
for index, row in checks.loc[checks['enabled']==True].iterrows():
    data = dataframes[checks.loc[index, 'dataframe_id']]
    col = checks.loc[index, 'col_name']
    dev = checks.loc[index, 'device']
    interp_data = numpy.interp(time_range, data['time'], data[col])
    interp_data = numpy.nan_to_num(interp_data)
    fig.add_trace(go.Scatter(x=time_range, y=interp_data, mode='lines', name=f'{dev}-{col}'))
yrange = [0,100]
st.title('Data')

fig.update_layout(
    xaxis=dict(range=[time_range[0],time_range[-1]], showgrid=True),
    yaxis=dict(range=yrange, showgrid=True, dtick=10, minor=dict(dtick=5, showgrid=True, griddash='3,2,3,2')),
    showlegend=True,
    legend=dict(y=-.2, orientation="h")
    )
st.plotly_chart(fig, use_container_width=True)