#import random
import time

import os
import glob

import datetime as dt 
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import matplotlib.dates as mdates

#### Function for simulated temperature
#def get_temp(cur_temp):
#    #Eventually this will read temp from a probe
#    new_temp = cur_temp +  random.random() - 0.5
#    return new_temp

def get_temp():
     # Retrieve raw temperature output from device
     f = open(device_file, 'r')
     lines = f.readlines()
     f.close

     equals_pos = lines[1].find('t=')
     if equals_pos != -1:
         temp_string = lines[1][equals_pos+2:]
         temp_c = float(temp_string) / 1000.0

     return temp_c


def animate(i, t, temp):

    curr_temp = get_temp()
    curr_time = dt.datetime.now()
    
    if len(t) <= t_points:
        temp.append(curr_temp)
        t.append(curr_time)
  
    else:
         if (curr_time - t[-1]).total_seconds() > t_history/t_points:
             temp.append(curr_temp)
             t.append(curr_time)
         else:
             temp[-1] =  (temp[-1]+curr_temp)/2

    #Trim to correct length
    temp = temp[-t_points:]
    t = t[-t_points:]      

    #Plot temp data
    ax.clear()
    ax.plot(t,temp)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(left=0.15, right=0.95, bottom=0.20, top=0.95)
    plt.ylabel('Temperature (deg C)')
    #ax.xaxis.set_major_locator(mdates.HourLocator(byhour=[0,3,6,9,12,15,18,21]))  # SecondLocator(bysecond=[0,15,30,45]))        #Adjust from SecondLocator
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%I:%M %p'))                               #Adjust remove seconds
    plt.text(0.1,0.9,"Current Temp=" + str(round(curr_temp,1)) + " deg C",transform=ax.transAxes,fontweight='bold')
    plt.text(0.1,0.8,"High Temp    =" + str(round(max(temp),1)) + " deg C",transform=ax.transAxes)
    plt.text(0.1,0.7,"Low Temp     =" + str(round(min(temp),1)) + " deg C",transform=ax.transAxes)
   
    # Pause for time interval
    time.sleep(t_interval)


###### Set parameters   #######

# Time sampling interval (in sec)
t_interval = 2
# Time history to record (in sec)
t_history = 60*60*24
# Number of points to plot
t_points =  200

# Calculate (a) length of history vector and (b) how many measurements to skip before plotting a point
#t_len = int(t_history/t_interval)
#t_skip = (t_history/t_interval)/t_points
#if t_skip < 1:
#    t_skip = 1
#t_skip = int(t_skip)

# Setup OS to retrieve temperature from file
#### Set up temperature probe
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
fig.canvas.manager.full_screen_toggle()

# Initialize list with 2 points
temp = [get_temp()]
t = [dt.datetime.now()]
time.sleep(0.1)
temp.append(get_temp())
t.append(dt.datetime.now())

#try:
    # Set up plot to call animate() function periodically
#    print("starting plotting")
#    ani = animation.FuncAnimation(fig, animate, fargs=(t, temp))
#    plt.show()

#except:
#    plt.close()
    

print("starting plotting")
ani = animation.FuncAnimation(fig, animate, fargs=(t, temp))
plt.show()
    




