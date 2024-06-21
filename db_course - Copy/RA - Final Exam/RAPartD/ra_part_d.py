import numpy as np
import matplotlib.pyplot as plt 

team_names = ['Team 1', 'Team 2', 'Team 3', 'Team 4']
group1 = [20,35,25,30]
group2 = [15,28,22,18]

width = 0.2
x = np.arange(len(team_names))
fig, ax = plt.subplots()
bar_chart1 = ax.bar(x-width/2, group1, width, label='Group 1')
bar_chart2 = ax.bar(x+width/2, group2, width, label='Group 2')

ax.set_title('Comparing Goals')
ax.set_xlabel('Teams')
ax.set_ylabel('Total Goals')
ax.set_xticks(x)
ax.set_xticklabels(team_names)

ax.legend()
plt.show()