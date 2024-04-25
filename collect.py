import clr # the pythonnet module.
clr.AddReference(r'OpenHardwareMonitorLib') 
import datetime
from OpenHardwareMonitor.Hardware import Computer
import numpy
import pandas
import time

class NotAdministator(Exception):
    def __init__(self):
        print('Program unable to retrieve data')

class HWMonitor():
    def __init__(self):
        self.c = Computer() 
        self.c.GPUEnabled = True 
        self.c.CPUEnabled = True 
        self.c.Open()
    def cpu(self):
        self.c.Hardware[0].Update()
        ccd_temp = self.c.Hardware[0].Sensors[16].get_Value()
        package_temp = self.c.Hardware[0].Sensors[15].get_Value()
        load = self.c.Hardware[0].Sensors[6].get_Value()
        core_watts = self.c.Hardware[0].Sensors[23].get_Value()
        package_watts = self.c.Hardware[0].Sensors[7].get_Value()
        # for sensor in range(0, len(self.c.Hardware[0].Sensors)):
        #     print(f'{sensor} | {self.c.Hardware[0].Sensors[sensor].Name} | {self.c.Hardware[0].Sensors[sensor].get_Value()}')
        return ccd_temp, package_temp, load, core_watts, package_watts
    def gpu(self):
        self.c.Hardware[1].Update()
        temp = self.c.Hardware[1].Sensors[0].get_Value()
        load = self.c.Hardware[1].Sensors[4].get_Value()
        load_framebuf = self.c.Hardware[1].Sensors[5].get_Value()
        load_videngine = self.c.Hardware[1].Sensors[6].get_Value()
        load_bus = self.c.Hardware[1].Sensors[7].get_Value()
        watts = self.c.Hardware[1].Sensors[14].get_Value()
        return temp, load, load_framebuf, load_videngine, load_bus, watts
        # for sensor in range(0, len(self.c.Hardware[1].Sensors)):
        #     print(f'{sensor} | {self.c.Hardware[1].Sensors[sensor].Name} | {self.c.Hardware[1].Sensors[sensor].get_Value()}')
    def get_info(self):
        start_t = datetime.datetime.now()
        
        cpu_stats = numpy.zeros([100, 5], dtype=float)
        gpu_stats = numpy.zeros([100, 6], dtype=float)
        
        end_t = datetime.datetime.now()
        time_d = end_t-start_t
        ind = 0
        while time_d.seconds < 5:
            cpu_stats[ind] = self.cpu()
            gpu_stats[ind] = self.gpu()
            end_t = datetime.datetime.now()
            time_d = end_t-start_t
            ind += 1
            
        #Remove all zero rows from arrays
        cpu_stats = cpu_stats[~numpy.all(cpu_stats == 0, axis=1)]
        gpu_stats = gpu_stats[~numpy.all(gpu_stats == 0, axis=1)]
        
        #Filter values
        cpu_filt = numpy.zeros(cpu_stats.shape[1])
        for i in range(cpu_stats.shape[1]):
            cpu_filt[i] = numpy.average([item[i] for item in cpu_stats])
        gpu_filt = numpy.zeros(gpu_stats.shape[1])
        for i in range(gpu_stats.shape[1]):
            gpu_filt[i] = numpy.average([item[i] for item in gpu_stats])
        return cpu_filt.tolist(), gpu_filt.tolist()

mon = HWMonitor()
cpu = pandas.DataFrame(columns=['time', 'ccd_temp', 'package_temp', 'load', 'core_watts', 'package_watts'])
gpu = pandas.DataFrame(columns=['time', 'temp', 'load', 'load_framebuf', 'load_videngine', 'load_bus', 'watts'])
a = datetime.datetime.now()
for i in range (2880):
    stats = mon.get_info()
    current_time = time.time()
    cpu.loc[len(cpu)] = [current_time] + stats[0]
    gpu.loc[len(gpu)] = [current_time] + stats[1]
    print(i)
b = datetime.datetime.now()
c = b - a
print(f'{c}')
cpu.to_csv('test_cpu.csv', index=False)
gpu.to_csv('test_gpu.csv', index=False)