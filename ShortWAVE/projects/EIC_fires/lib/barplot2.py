import numpy as np
import matplotlib   
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

# Sample data
#categories = ['CO$\mu$ Carbon\nMonoxide', 'Nitrogen\nDioxide', 'Ozone', 'Particulate\nMatter 2.5']
categories = ['Carbon\nMonoxide', 'Nitrogen\nDioxide', 'Ozone', 'Particulate\nMatter 2.5']
values = [7, 2, 4, 10]
bar_height = 0.75
y_pos = np.arange(len(categories))

fig, ax = plt.subplots(figsize=(10, 5))
dpi = fig.get_dpi()

# Create the horizontal bar chart
ax.barh(y_pos, [10,10,10,10], height=bar_height, color='black', edgecolor='white', linewidth=2)
ax.barh(y_pos, values, height=bar_height-0.02, color='red', edgecolor=(0,0,0,0))

# Turn off the axes
#plt.axis('off')

# Hide the top and right spines
ax.set_xlim(-0.02,10.02)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
levels = [0, 5, 10]
labels = ['Low', 'Moderate', 'High']
ax.set_xticks(levels)
ax.set_xticklabels(labels, fontsize=14, color='white',
              fontfamily='sans-serif', fontweight='bold', fontstyle='normal')

ax.set_yticks(y_pos)
ax.set_yticklabels(categories, fontsize=14, color='white',
              fontfamily='sans-serif', fontweight='bold', fontstyle='normal')

plt.savefig('test.png', format='png', facecolor=(0,0,0), dpi=150,
           transparent=True, bbox_inches='tight', pad_inches=0.01)


# Display the plot
#plt.show()
