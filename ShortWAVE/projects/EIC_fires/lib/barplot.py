import matplotlib   
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

# Sample data
categories = ['Carbon\nMonoxide', 'Nitrogen\nDioxide', 'Ozone', 'Particulate\nMatter 2.5']
values = [7, 2, 4, 10]

fig, ax = plt.subplots()
dpi = fig.get_dpi()
fig.set_size_inches(1500.0/dpi, 750.0/dpi)

# Create the horizontal bar chart
ax.barh(categories, [10,10,10,10], width=0.5, color='black', edgecolor='white', linewidth=2)
ax.barh(categories, values, width=0.48, color='red', edgecolor=(0,0,0,0))

# Turn off the axes
#plt.axis('off')

# Hide the top and right spines
ax.set_xlim(-0.02,10.02)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
levels = [0, 5, 10]
labels = ['Low', 'Moderate', 'High']
ax.set_xticks(levels)
ax.set_xticklabels(labels, fontsize=14, color='white',
              fontfamily='sans-serif', fontweight='bold', fontstyle='normal')
ax.set_yticklabels(categories, fontsize=14, color='white',
              fontfamily='sans-serif', fontweight='bold', fontstyle='normal')

plt.savefig('test.png', format='png', facecolor=(0,0,0),
           transparent=True, bbox_inches='tight', pad_inches=0.01)


# Display the plot
#plt.show()
