import matplotlib.pyplot as plt
from Model_Pressure_System import plot_pressure_model
from Plot_pressure_control_data import pressure_control_data
from pressureSwapping import align_yaxis

ICs =[100,1.98]


fig, ax1, fig2, ax2 = pressure_control_data()

for i in range(len(fig)):

    fig[i], ax1[i], fig2[i], ax2[i] = plot_pressure_model(fig[i], ax1[i], fig2[i], ax2[i], ICs)

    ax1[i].legend()
    ax2[i].legend()


fig[3].show()
fig2[3].show()

# fig[4].show()
# fig2[4].show()

plt.show()