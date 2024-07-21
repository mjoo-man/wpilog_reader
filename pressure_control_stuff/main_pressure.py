import matplotlib.pyplot as plt
from Model_Pressure_System import plot_pressure_model
from Plot_pressure_control_data import pressure_control_data
from pressureSwapping import align_yaxis

ICs = [[95.3,2.2], [110, 3]]


fig, ax1, ax2 = pressure_control_data()

for i in range(len(fig)):
    fig[i], ax1[i], ax2[i] = plot_pressure_model(fig[i], ax1[i], ax2[i], ICs[i])

    ax1[i].legend()
    ax2[i].legend()

plt.show()