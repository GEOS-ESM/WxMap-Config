import os
import io
import glob
import csv
import numpy as np
from PIL import Image, ImageDraw

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class FireMonitor(object):

    def __init__(self, dpath, fire_id, fields, console=None):

        self.stats = {}
        self.fields = fields
        self.console = console

        listing = glob.glob(os.path.join(dpath, fire_id + '.*.stat'))

        for file in listing:

            field = os.path.basename(file).split('.')[1]

            buf = {}
            self.stats[field] = buf

            with open(file, 'r') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row in reader:
                    time = row[0]
                    buf[time] = [float(r) for r in row[1:]]

    def hgraph(self, *fields):
    
        categories = []
        values = []
        for field in fields:
    
            categories.append(field.title)
            values.append(field.value)
    
        bar_height = 0.75
        y_pos = np.arange(len(categories))
    
        fig, ax = plt.subplots()
        dpi = fig.get_dpi()
        fig.set_size_inches(1700/dpi,800/dpi)
        ax.set_facecolor('black')
    
        plt.tight_layout()
        plt.margins(y=0.01)
        plt.subplots_adjust(left=0.1)
    
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
        ax.set_xticklabels(labels, fontsize=18, color='white',
              fontfamily='sans-serif', fontweight='normal', fontstyle='normal')
    
        ax.set_yticks(y_pos)
        ax.set_yticklabels(categories, fontsize=18, color='white',
              fontfamily='sans-serif', fontweight='normal', fontstyle='normal')
    
        buf = io.BytesIO()
        plt.savefig(buf, format='png', facecolor=(0,0,0), dpi=dpi)
     #     transparent=True, bbox_inches='tight', pad_inches=0)

        plt.close()
    
        buf.seek(0)
        return Image.open(buf)

class FireMonitorClassic(FireMonitor):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if self.console:
            self.image = Image.open(self.console).convert("RGBA")
            self.handle = ImageDraw.Draw(self.image)

        w = 114
        h = 996
        bot = 1394

        c1 = (255,0,0)
        c2 = (255,0,0)
        c3 = (255,0,0)
        c4 = (255,0,0)
        c5 = (255,0,0)
        c6 = (255,0,0)

        self.t2m = FireMonitorDraw(self.handle, ( 496,bot,w,h), 10,  40, fgcolor=c1)
        self.w10m = FireMonitorDraw(self.handle, ( 696,bot,w,h),  0,  14, fgcolor=c1)
        self.rh = FireMonitorDraw(self.handle, ( 890,bot,w,h),  0,  100, fgcolor=c1)
        self.sm  = FireMonitorDraw(self.handle, (1092,bot,w,h),  0,   1, fgcolor=c2)
        self.co  = FireMonitorDraw(self.handle, (1828,bot,w,h),  0, 800, fgcolor=c3)
        self.no2 = FireMonitorDraw(self.handle, (2036,bot,w,h),  0,  50, fgcolor=c4)
        self.o3  = FireMonitorDraw(self.handle, (2256,bot,w,h),  0,  70, fgcolor=c5)
        self.pm  = FireMonitorDraw(self.handle, (2476,bot,w,h),  0, 100, fgcolor=c6)

    def draw(self, time_dt):

        t = time_dt.strftime("%Y%m%dT%H%M%S")

        t2m = self.stats['t2mmax'][t][1]
        w10m = self.stats['wind10m'][t][1]
        rh = self.stats['rhmin'][t][0]
        sm  = self.stats['gwettop'][t][0]
        co  = self.stats['cosfc'][t][1]
        no2 = self.stats['no2sfc'][t][1]
        o3  = self.stats['o3sfc'][t][1]
        pm  = self.stats['pm25sfc'][t][1]


        self.t2m.draw(t2m)
        self.w10m.draw(w10m)
        self.rh.draw(rh)
        self.sm.draw(sm)
        self.co.draw(co)
        self.no2.draw(no2)
        self.o3.draw(o3)
        self.pm.draw(pm)

        return self.image

class FireMonitorDraw(object):

    def __init__(self, draw_obj, bbox, rmin, rmax, bgcolor='black', fgcolor='white', reverse=False):

        self.handle = draw_obj
        self.rmin = float(rmin)
        self.rmax = float(rmax)
        self.range = self.rmax - self.rmin

        self.width = bbox[2]
        self.height = bbox[3]

        self.left = bbox[0]
        self.right = bbox[0] + bbox[2]
        self.bot = bbox[1]
        self.top = bbox[1] - bbox[3]

        self.bbox = ((self.left, self.top), (self.right, self.bot))

        self.fgcolor = fgcolor
        self.bgcolor = bgcolor
        self.reverse = reverse

    def draw(self, rval, rmin=None, rmax=None):

        if rmin == None:
            rmin = self.rmin
        if rmax == None:
            rmax = self.rmax

        range = rmax - rmin

        self.handle.rectangle(self.bbox, fill=self.bgcolor)

        rfactor = (rval - rmin) / (range)
        ytop = int(round(self.bot - rfactor * self.height))

        if self.reverse:
            ytop = int(round(self.top + rfactor * self.height))

        ytop = max(ytop, self.top)
        if ytop >= self.bot:
            return

        bbox = ((self.left, ytop), (self.right, self.bot))
        self.handle.rectangle(bbox, fill=self.fgcolor)

class FireMonitorAQ(FireMonitor):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

    def draw(self, time_dt):
        
        t = time_dt.strftime("%Y%m%dT%H%M%S")
        
        co = FireField(self.fields['CO'], self.stats['cosfc'][t][1])
        no2 = FireField(self.fields['NO2'], self.stats['no2sfc'][t][1])
        o3 = FireField(self.fields['O3'], self.stats['o3sfc'][t][1])
        pm = FireField(self.fields['PM25'], self.stats['pm25sfc'][t][1])

        return self.hgraph(pm, no2, o3, co)

class FireMonitorWX(FireMonitor):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

    def draw(self, time_dt):

        t = time_dt.strftime("%Y%m%dT%H%M%S")

        t2m = FireField(self.fields['T2M'], self.stats['t2mmax'][t][1])
        w10m = FireField(self.fields['W10M'], self.stats['wind10m'][t][1])
        rh = FireField(self.fields['RH'], self.stats['rhmin'][t][0])
        sm = FireField(self.fields['SM'], self.stats['gwettop'][t][0])

        return self.hgraph(sm, rh, w10m, t2m)

class FireField(object):

    def __init__(self, field, value):

        self.title = field['title']

        rmin = field['min']
        rmax = field['max']
        rval = (value-rmin)/(rmax-rmin)*100
        self.value = min(max(rval, 0), 100)
