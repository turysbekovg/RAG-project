import matplotlib.pyplot as plt
import numpy as np

# Data
materials = ['AlSi10Mg', 'SS316L', 'Ti6Al4V']

data = {
    'aerospace_new': [247, 107, 309],
    'automotive_new': [323, 138, 297],
    'biomedical_new': [156, 64, 373]
}

max_value = max(max(values) for values in data.values())

# Plotting
x = np.arange(len(materials))
width = 0.2 

fig, ax = plt.subplots()

# naming the bars and filling with the values from the data
bars1 = ax.bar(x - width, data['aerospace_new'], width, label='aerospace')
bars2 = ax.bar(x, data['automotive_new'], width, label='automotive')
bars3 = ax.bar(x + width, data['biomedical_new'], width, label='biomedical')

# Add some text for labels, title, x-axis tick labels
ax.set_xlabel('Materials', fontsize=15)
ax.set_ylabel('Values', fontsize=15)
ax.set_title('Values by field and material', fontsize=15)

ax.set_xticks(x)
ax.set_xticklabels(materials, fontsize=13) 
ax.tick_params(axis='y', labelsize=13)     

ax.legend(fontsize=13)

#ax.set_xticks(x)
#ax.set_xticklabels(materials)
#ax.legend()

ax.set_ylim(0, max_value * 1.1)

# Attach a text label above each bar in bars, displaying its height
def autolabel(bars):
    for bar in bars:
        height = bar.get_height()
        ax.annotate('{}'.format(height),
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=14)

autolabel(bars1)
autolabel(bars2)
autolabel(bars3)

fig.tight_layout()

plt.savefig("instances_diagram.jpeg", format='jpeg', dpi=600)

plt.show()
