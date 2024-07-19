import numpy as np
import matplotlib.pyplot as plt
import os
from fileOps import getFilePath, getCSVFiles
from updater import update_progress
import pandas as pd
from scipy.integrate import solve_ivp, odeint
from scipy import signal

# Constants for the model of the system
#Leak constants
kt = 0.001095878 * 0.85
#kt = 0.00052477*1.5
kb = 0.00013587
Pc = 2.1366 *1.1
Ps = 0.008
#Volume ratio calculation
vBall = 0.85 * (4 / 3) * (12 ** 3) * np.pi  # volume of the ball accounting for space taken up (in^3)
vTanks = 574 * 3 / 16.387  # volume of pressure tanks converted to (in^3)
vRatio = vTanks / vBall
#Control Constants
Pctank = 2.1366*1.1
Pcball = 0.0446
Pstank = 0.05791 * 1.3
Psball = 0.004943 / 3.6

C = np.array([[-kt, kt], [vRatio * kt, -vRatio * kt - kb]])  # Newly defined system
D = np.array([[Pctank, -Pstank], [-Pcball, Psball]])  #

# inital Conditions and integrating range
Pt_0 =100 # psi
Pb_0 =2.0  # psi
tend = 60 # seconds to run sim

class cooldown_states:
    def __init__(self):
        self.t_off = 99
        self.t_off_s = 0
        self.first_time = True
    def set_time(self, t):
        self.t_off = t
    def set_time_c(self, t):
        self.t_off_c = t
    def set_time(self):
        self.first_time = False

comp1 = cooldown_states()
t_off = 0
E = np.array([[1, 0], [0, Pt_0 - Pb_0]])
ICs = [Pt_0, Pb_0]
def align_yaxis(ax1, v1, ax2, v2):
    """adjust ax2 ylimit so that v2 in ax2 is aligned to v1 in ax1"""
    _, y1 = ax1.transData.transform((0, v1))
    _, y2 = ax2.transData.transform((0, v2))
    inv = ax2.transData.inverted()
    _, dy = inv.transform((0, 0)) - inv.transform((0, y1 - y2))
    miny, maxy = ax2.get_ylim()
    ax2.set_ylim(miny + dy, maxy + dy)


def control_input2(t, q, setpoint, comp_obj):
    tol = 0.0 # psi
    cooldown = 0 # sec
    out = np.array([[0], [0]])
    e = q[1] - setpoint
    # print("solenoid time", comp1.t_off_s)
    # print("solenoid time", comp1.t_off_c)
    if abs(comp_obj.t_off - t) > 5: # only make a control action every 5 seconds
        if e < 0 + tol:
            if q[1] < setpoint + tol:  # only turn on solenoid when pressure is less than required
                out = np.array([[0], [1]])

        elif e > 0 - tol:
            if q[1] > setpoint - tol:  # only turn on compressor when pressure is less than required
                out = np.array([[1], [0]])

        else:
            out = np.array([[0], [0]])
            comp_obj.t_off = t
    return out

def step_func(t):
    out = 0
    if t < int(0.4*tend):
        out = 3.2 # psi
    elif t < int(0.6*tend):
        out = 2.5 # psi
    else:
        out = 2.5 # psi

    return out
def newPressureSys(t, q, comp_obj):
    setpoint = step_func(t)
    u = control_input2(t, q, setpoint, comp_obj)
    q = np.reshape(q, (2, 1))
    diff = q[0] - q[1]
    # print("t:")
    # print(t)
    E[1][1] = diff[0]
    Bprime = np.matmul(D, E)  # augmented control matrix
    xdot = C @ q + Bprime @ u

    return xdot[0][0], xdot[1][0]

log_dir = getFilePath("Select Folder with the Logs to Plot")

os.chdir(log_dir)

filenames = getCSVFiles(log_dir)
prog = 0
for file in filenames:
    update_progress(f"Working on {file}", prog / len(filenames))
    prog += 1

    # just read the headers of each file
    headers = pd.read_csv(file, index_col=0, nrows=0).columns.tolist()

    simple_headers = [headers[i].replace("NT:/SmartDashboard/", "") for i in range(len(headers))]

    des_headers_drive = ['Ball Pressure (psi)', 'Tank Pressure (psi)', 'pressure setpoint']

    run_data = pd.read_csv(file, index_col=0)  # timestamp is the index
    # print("0")
    # print(run_data.index.values[0])
    # print("Length below")
    # print(len(run_data.index.values))
    # print("Last element")
    end = len(run_data.index.values)-1
    # print(run_data.index.values[end])

# times = []
# for i in range(end):
#     times.append(run_data.index.values[i])
# tstart = times[0]
# tfinish = times[len(times)-1]

# sol = solve_ivp(newPressureSys,[tstart,tfinish], ICs, t_eval=times,max_step=0.1)

tspan = np.linspace(0, tend, 50)
sol = solve_ivp(newPressureSys,[0,tend], ICs, t_eval=tspan, max_step=0.1, args=(comp1,))
# print("solt")
# print(sol.t)
# print("soly")
# print(sol.y)
# print("soly0")
# print(sol.y[0])
# Plot the modeled data
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax2.plot(tspan, sol.y[0], color='blue', label='Tank Pressure (psi)')
ax1.plot(tspan, sol.y[1], color='black', label='Ball Pressure (psi)')
ax1.plot(tspan, [step_func(tspan[i]) for i in range(len(tspan))], '--', label='Control Input')
plt.title("Modeled System")
ax1.set_ylabel("Ball Pressure (psi)")
ax2.set_ylabel("Tank Pressure (psi)")
ax1.set_xlabel("time (s)")
plt.grid()
ax1.legend(loc=2)
ax2.legend(loc=1)
align_yaxis(ax1,10,ax2,10)
for ax, ylim in zip([ax1, ax2], [10, 110]):
    ax.set_ylim(0, ylim)
    ax.grid(True)

plt.figure(2)
plt.plot(tspan, [control_input2(tspan[i], [sol.y[0][i], sol.y[1][i]], step_func(tspan[i]), comp1)[1] for i in range(len(tspan))], label='solenoid state')
plt.plot(tspan, [control_input2(tspan[i], [sol.y[0][i], sol.y[1][i]], step_func(tspan[i]), comp1)[0] for i in range(len(tspan))], label='compressor state')
plt.title("Control States")
plt.legend()
plt.show()

#####################################
'''
fig, bx1 = plt.subplots()
bx2 = bx1.twinx()

# filter the tank pressure data
fs = 1000  # Sampling frequency
fc = 5  # Cut-off frequency of the filter
w = fc / (fs / 2)  # Normalize the frequency
b, a = signal.butter(5, w, 'low')
filt_tank = signal.filtfilt(b, a, run_data[headers[2]])
shell_press = run_data[headers[1]].values

bx1.plot(run_data.index.values, shell_press, 'b', label='Ball Pressure')
bx2.plot(run_data.index.values, filt_tank, 'k', label='Tank Pressure')  # from rad/s to mph
bx1.plot(times, sol.y[1], 'b--', label="Modeled Ball Pressure")
bx2.plot(times, sol.y[0], 'k--', label='Modeled Tank Pressure')
#############
plt.title("Recorded vs Modeled Pressure Data")
bx1.set_ylabel("Ball Pressure (psi)")
bx2.set_ylabel("Tank Pressure (psi)")
bx1.set_xlabel("time (s)")

plt.grid(axis="both")
bx1.legend(loc=1)
bx2.legend(loc=2)

for bx, ylim in zip([bx1, bx2], [10, 100]):
    bx.set_ylim(0, ylim)
    bx.grid(True)
#bx1.set_ylim(1.75,10)
#bx2.set_ylim(0,100)

plt.show()


fig, cx1 = plt.subplots()
percentTankError = []
percentBallError = []

for i in range(len(sol.y[1])):
    if shell_press[i] != 0:
        percentBallError.append(100*(sol.y[1][i]-shell_press[i])/(shell_press[i]))
    else:
        percentBallError.append(0)
    if filt_tank[i] != 0:
        percentTankError.append(100*(sol.y[0][i]-filt_tank[i])/(filt_tank[i]))
    else:
        percentTankError.append(0)

cx1.plot(times, percentBallError,'b', label="Ball Pressure Error")
cx1.plot(times, percentTankError, 'k', label="Tank Pressure Error")
#cx1.plot(times, sol.y[1]-shell_press[:-1], label="ball pressure error", color = "red")
#cx1.plot(times, sol.y[0]-filt_tank[:-1], label="tank pressure error", color="purple")

cx1.legend(loc=1)
plt.grid()
cx1.set_ylim(-100,100)
plt.title("Errors Between Model and Data")
cx1.set_xlabel("Time (s)")
cx1.set_ylabel("Pressure error (%)")

plt.show()
'''