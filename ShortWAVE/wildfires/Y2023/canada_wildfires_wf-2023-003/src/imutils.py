from PIL import Image, ImageDraw, ImageFont

def im_paste_file(bg, fname, xpos, ypos, xsize=None, ysize=None):

    img     = Image.open(fname)
    
    if xsize:
        ratio   = float(img.size[1]) / float(img.size[0])
        ysize   = int(xsize * ratio)
    
    elif ysize:
        ratio   = float(img.size[0]) / float(img.size[1])
        xsize   = int(ysize * ratio)
    
    if xsize and ysize:
        img = img.resize((xsize, ysize), Image.ANTIALIAS)

    xsize = img.size[0]
    ysize = img.size[1]
    
    bg.paste(img, (xpos, ypos), img)
    
    img.close()

    return (xsize, ysize)

class HersheyDraw(object):
    """
    Defines methods for drawing formatted text on an image.

    The methods in this class use the PIL library to draw text
    on an image. The text may contain format control characters
    as defined by the GrADS Hershey font for super- and sub-scripting.

    Requirements
    ------------
    from PIL import ImageDraw, ImageFont
    """

    def __init__(self, im, font, size, color, **kwargs):
        """
        Initializer

        Parameters
        ----------
        im : Image
            PIL image object.
        font : string
            Name of font file (Truetype etc.).
        size : integer
            Font size (pixels). Super and sub-scripting font size
            is set to size/2.
        color : tuple
            RGB(A) value for font color (R, G, B, A)

        Returns
        -------
        None
            No return value

        """

        self.color = color
        self.d     = ImageDraw.Draw(im)
        self.fn    = ImageFont.truetype(font, size)
        self.fs    = ImageFont.truetype(font, int(size/2))
        self.hn    = self.d.textsize('1', font=self.fn)[1]
        self.hs    = self.d.textsize('1', font=self.fs)[1]

    def text_size(self, text):
        """
        Returns the size of the text string in pixels.

        This method returns the size of the string in pixels after
        resolving the Hershey font control characters.

        Parameters
        ----------
        text : string
            Text string with or without Hershey control characters. Only
            superscripting (`a), subscripting (`b) and normal (`n) formatting
            sequences are recognized.

        Returns
        -------
        size : tuple
            width and height of the text string (w, h) where "h" is the
            maximum height of the string.

        """

        if not text: return (0, 0)

        words = text.split('`')
        if words[0]: words[0] = 'n' + words[0]

        nText, sText = ('', '')

        for s in words:

            if not s: continue
            if len(s) == 1: continue

            if s[0] == 'n':
                nText += s[1:]
            else:
                sText += s[1:]

        wn, hn, ws, hs = (0, 0, 0, 0)
        if nText: wn, hn = self.d.textsize(nText, font=self.fn)
        if sText: ws, hs = self.d.textsize(sText, font=self.fs)

        return (wn + ws, max(hn,hs))

    def draw_text(self, x, y, text):
        """
        Draws text on an image.

        This method uses the PIL library to draw text on the image.
        The text may contain format control characters as defined by
        the GrADS Hershey font for super- and sub-scripting.

        Parameters
        ----------
        x : integer
            Left pixel location of string.

        y : integer
            Top pixel location of string.

        text : string
            Text string with or without Hershey control characters. Only
            superscripting (`a), subscripting (`b) and normal (`n) formatting
            sequences are recognized.

        Returns
        -------
        None
            No return value

        """

        if not text: return

        words = text.split('`')
        if words[0]: words[0] = 'n' + words[0]
 
        for s in words:

            if not s: continue
            if len(s) == 1: continue

            if s[0] == 'n':
                self.d.text( (x, y), s[1:], font=self.fn, fill=self.color)
                w, h = self.d.textsize(s[1:], font=self.fn)
                x += w
            elif s[0] == 'a':
                self.d.text( (x, y), s[1:], font=self.fs,
                                                      fill=self.color)
                w, h = self.d.textsize(s[1:], font=self.fs)
                x += w
            elif s[0] == 'b':
                self.d.text( (x, y+self.hn-self.hs), s[1:], font=self.fs,
                                                      fill=self.color)
                w, h = self.d.textsize(s[1:], font=self.fs)
                x += w

def create_rounded_rectangle_mask(size, radius, alpha=255):
    factor = 5  # Factor to increase the image size that I can later antialiaze the corners
    radius = radius * factor
    image = Image.new('RGBA', (size[0] * factor, size[1] * factor), (0, 0, 0, 0))

    # create corner
    corner = Image.new('RGBA', (radius, radius), (0, 0, 0, 0))
    draw = ImageDraw.Draw(corner)
    # added the fill = .. you only drew a line, no fill
    draw.pieslice((0, 0, radius * 2, radius * 2), 180, 270, fill=(0, 0, 0, alpha + 64))

    # max_x, max_y
    mx, my = (size[0] * factor, size[1] * factor)

    # paste corner rotated as needed
    # use corners alpha channel as mask
#   image.paste(corner, (0, 0), corner)
#   image.paste(corner.rotate(90), (0, my - radius), corner.rotate(90))
#   image.paste(corner.rotate(180), (mx - radius, my - radius), corner.rotate(180))
    image.paste(corner.rotate(270), (mx - radius, 0), corner.rotate(270))

    # draw both inner rects
    draw = ImageDraw.Draw(image)
 #  draw.rectangle([(radius, 0), (mx - radius, my)], fill=(0, 0, 0, alpha))
 #  draw.rectangle([(0, radius), (mx, my - radius)], fill=(0, 0, 0, alpha))

    draw.rectangle([(0, 0), (mx - radius, my)], fill=(0, 0, 0, alpha))
    draw.rectangle([(0, radius), (mx, my)], fill=(0, 0, 0, alpha))
    image = image.resize(size, Image.ANTIALIAS)  # Smooth the corners

    return image
