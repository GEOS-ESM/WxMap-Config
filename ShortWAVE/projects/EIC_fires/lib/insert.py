import io
import numpy as np
import matplotlib   
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

from PIL import Image
from fire_monitor import FireField

CO = dict(title='Carbon\nMonoxide\n(CO)', min=0, max=800)
NO2 = dict(title='Nitrogen\nDioxide\n(NO2)', min=0, max=50)
PM25 = dict(title='Particulate\nMatter\n(PM2.5)', min=0, max=100)
O3 = dict(title='Ozone\n(O3)', min=0, max=70)
T2M = dict(title='Temperature\n(T2m)', min=0, max=40)
W10M = dict(title='Wind Speed\n(W10m)', min=0, max=14)
SM = dict(title='Soil\nMoisture\n(SM)', min=0, max=1)
RH = dict(title='Relative\nHumidity\n(RH)', min=0, max=100)

def hgraph(*fields):

    categories = []
    values = []
    for field in fields:

        categories.append(field.title)
        values.append(field.value)

    bar_height = 0.75
    y_pos = np.arange(len(categories))

    fig, ax = plt.subplots()
    dpi = fig.get_dpi()
    fig.set_size_inches(1500/dpi,750/dpi)

    plt.tight_layout()
    plt.margins(y=0, tight=True)

    # Create the horizontal bar chart
    ax.barh(y_pos, 4*[100.2], height=bar_height, color='black',
            edgecolor='white', linewidth=3)
    ax.barh(y_pos, values, height=bar_height-0.02, color='red',
            edgecolor=(0,0,0,0))

    # Hide the spines
    ax.set_xlim(-0.2,100.2)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    levels = [0, 50, 100]
    labels = ['low', 'moderate', 'high']
    ax.set_xticks(levels)
    ax.set_xticklabels(labels, fontsize=16, color='white',
          fontfamily='sans-serif', fontweight='normal', fontstyle='normal')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(categories, fontsize=16, color='white',
          fontfamily='sans-serif', fontweight='normal', fontstyle='normal')

    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor=(0,0,0), dpi=dpi,
       transparent=True, bbox_inches='tight', pad_inches=0)

    buf.seek(0)
    img = Image.open(buf)
    img.save('test.png', "PNG")
    return img

co = FireField(CO, 400.0)
no2 = FireField(NO2, 40.0)
o3 = FireField(O3, 70.0)
pm = FireField(PM25, 100.0)

t2m = FireField(T2M, 20.0)
w10m = FireField(W10M, 10.0)
sm = FireField(SM, 0.0)
rh = FireField(RH, 100.0)

hgraph(pm, no2, o3, co)
#hgraph(sm, rh, w10m, t2m)
