class ImageMapper(object):

    def __init__(self, img, bbox):

        width = img.width
        height = img.height

        self.img = img
        self.bbox = tuple(bbox)
        self.x_factor = float(width-1) / (bbox[2] - bbox[0])
        self.y_factor = float(height-1) / (bbox[3] - bbox[1])

    def subset(self, bbox):

        x1 = int(round(float(bbox[0]-self.bbox[0]) * self.x_factor))
        y1 = int(round(float(bbox[1]-self.bbox[1]) * self.y_factor))
        x2 = int(round(float(bbox[2]-self.bbox[0]) * self.x_factor))
        y2 = int(round(float(bbox[3]-self.bbox[1]) * self.y_factor))

        return ImageMapper(self.img.crop((x1, y1, x2, y2)), bbox)

    def resize(self, bbox):
        return ImageMapper(self.img.resize(bbox, Image.ANTIALIAS), self.bbox)

    def to_pixel(self, bbox):

        obox = []

        for i in range(0, len(bbox), 2):
            lon = bbox[i]
            lat = bbox[i+1]
            x = int(round(float(lon - self.bbox[0]) * self.x_factor))
            y = int(round(float(lat - self.bbox[1]) * self.y_factor))
            obox.append(x)
            obox.append(self.img.height-y-1)

        return obox
