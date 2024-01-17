from stackingPressures import stackPressures
import matplotlib.pyplot as plt
import numpy as np

def flat_model(psi):
    # i measured this from data we collected
    #return 0.1802*psi**2 - 1.7484*psi + 9.6473
    return np.sqrt(4*81.87/(np.pi*psi))

def find_risetime(data): # data is a list of form [data values, time]
    def find_nearest(array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx]
    
    t = list(data[1])
    x = list(data[0])
    end = t.index(find_nearest(t,15)) # crop data to ~15 seconds
    t = t[0:end]
    x = x[0:end]
    # find ss position of last ten values
    x0 = x[0]
    ss = np.average(x[-1])
    rise_val =  x0 - 0.95*(x0 - ss)
    
    
    rise_val = find_nearest(x, rise_val)
    return t[x.index(rise_val)]



data = stackPressures(True)

plt.figure(1)
ax = plt.axes()
colors = plt.cm.jet(np.linspace(0,1,len(data.keys())))
endpoints = []
flats = []
for i in range(len(data.keys())):
    n = list(data.keys())[i]
    t = data[n][1]
    endpoints.append(data[n][0][-1]/data[n][0][0] )
    
    plt.scatter(flat_model(float(n)), data[n][0][-1], color=colors[i])

plt.legend()
ax.set_facecolor('gray')
# ax.xaxis.set_major_formatter(lambda x, pos: str(x/200))
plt.ylabel("SS Error/Inital angle")
plt.title("Steady State Error vs. Flat Diameter")
plt.xlabel("Flat Diameter (in) ")
plt.grid()

plt.figure(2)
ax = plt.axes()

endpoints = []
flats = []
for i in range(len(data.keys())):
    n = list(data.keys())[i]
    t = find_risetime(data[n])
    
    
    plt.scatter(flat_model(float(n)), t, color=colors[i])

plt.legend()
ax.set_facecolor('gray')
# ax.xaxis.set_major_formatter(lambda x, pos: str(x/200))
plt.ylabel("95% Rise time (s)")
plt.title("Rise time v flat size")
plt.xlabel("Flat Diameter (in) ")
plt.grid()

plt.show()