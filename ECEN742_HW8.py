import numpy as np
import matplotlib.pyplot as plt

# deifne the constants from data sheet
w_rated = 1750 # rpm
t_rated = 300 # ft-lb
kt = 0.885 # ftlb/A
kv = 1.27 # Vs/rad
Ra = 0.0099


# calculate stuff
ta_sols = []
wa_sols = []
tc_sols = []
wc_sols = []
td_sols = []
wd_sols = []
te_sols = []
we_sols = []

def prob2():

    def plot_curve(w, w_rated):
        if w <= w_rated*np.pi/30:
            return t_rated
        if w > w_rated*np.pi/30:
            t_weak = (kt*flux/Ra)*(Va - kv*flux*w)
            return t_weak
    flux = 1
    i_rated = t_rated / (kt*flux)
    Va = Ra*i_rated + kv*flux*(w_rated*np.pi/30)
    w_noload = Va / (kv*flux)

    global wa_sols
    wa_sols = np.linspace(0, w_noload, 1000)
    for w in wa_sols:
        ta_sols.append(plot_curve(w, w_rated))

    flux = 1
    i_rated = t_rated / (kt * flux)
    Va = Ra * i_rated + kv * flux*(w_rated * np.pi / 30)
    w_noload = Va / (2* kv * flux)
    global wc_sols
    wc_sols = np.linspace(0, w_noload, 1000)
    for w in wc_sols:
        tc_sols.append(plot_curve(w, w_rated))


    flux = 0.75
    i_rated = t_rated / (kt * flux)
    Va = Ra * i_rated + kv * flux*(w_rated * np.pi / 30)
    w_noload = Va / (kv * flux)
    global wd_sols
    wd_sols = np.linspace(0, w_noload, 1000)
    for w in wd_sols:
        td_sols.append(plot_curve(w, w_rated))

    flux = 0.5
    i_rated = t_rated / (kt * flux)
    Va = Ra * i_rated + kv * flux*(w_rated * np.pi / 30)
    w_noload = Va / (kv * flux)
    global we_sols
    we_sols = np.linspace(0, w_noload, 1000)
    for w in we_sols:
        te_sols.append(plot_curve(w, w_rated))

prob2()

plt.plot(wa_sols*30/np.pi, ta_sols, label='Rated Voltage, Full Flux')
plt.plot(wc_sols*30/np.pi, tc_sols, label='1/2 Rated Voltage, Full Flux')
plt.plot(wd_sols*30/np.pi, td_sols, label='Rated Voltage, 3/4 Flux')
plt.plot(we_sols*30/np.pi, te_sols, label='Rated Voltage, 1/2 Flux')
plt.xlabel('Speed (RPM)')
plt.ylabel('Torque (ft-lbs)')
plt.legend()
plt.grid()
plt.title('Different Operating Conditions for a 100hp Motor')
plt.show()